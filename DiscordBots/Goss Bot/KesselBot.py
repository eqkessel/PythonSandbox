#   KesselBot.py
#   Custom General-Purpose Utility Discord Bot
#   Written by Ethan Kessel (c) 2020

import os
import sys
import importlib
import argparse
import json
import threading
import signal

import asyncio
import discord
import discord.ext.commands as commands
from discord.ext.commands import command, Bot, Cog, CommandNotFound

import PrinTee

VERSION = "0.3.1"

class KesselBot(Bot):
    #   Load .json file given a path and filename, used to get configs
    @staticmethod
    def load_json_from_path(path, filename):
        with open(os.path.join(path, filename)) as filepath:
            return json.load(filepath)

    #   Constructor: takes filenames for config and secret files, path to configs (defaults to local dir)
    def __init__(self, *args, configPath = None, config, secret, lives=0, **kwargs):
        print(f"Initializing KesselBot v{VERSION}")
        
        #   Asyncio creates its own console which means PrinTee doesn't tee off of it
        #   Save the right console to fix it.
        self._stdout = sys.stdout
        self._stderr = sys.stderr

        #   Register shutdown signal handlers
        signal.signal(signal.SIGTERM, self.stop)    #   Termination signal
        signal.signal(signal.SIGINT, self.stop)     #   Keyboard interrupt
                                                    #   Hangup signal (ssh disconnected)
        signal.signal(signal.SIGHUP, lambda : print(f"Ignoring Hangup Signal"))

        #   Flag to specify to try restarting or not
        self.do_not_revive = False
        self.lives = lives

        #   Save the local dir for future reference
        self.FILE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not configPath:
            self.configPath = self.FILE_DIR
        else:
            self.configPath = configPath
        
        print(f"Loading configs from {self.configPath}")
        self.config = self.load_json_from_path(self.configPath, config)
        self.secret = self.load_json_from_path(self.configPath, secret)

        print(f"Initializing bot component")
        #   Run parent class Bot constructor using options from config
        super(KesselBot, self).__init__(**self.config['bot_options'])

        #   Register methods to run pre/post any command
        self.before_invoke(self.__bot_before_invoke)

        #   Set up a private variable to monitor for shutdown
        self.__shutdown_flag = False

        print(f"Loading bot Cogs:")
        #   Load bot "Cogs" - contain grouped functionality
        self.add_cog(BaseFunctionalityCog(self))
        _cogs = self.config['enabled_cogs']
        for cog_name in _cogs:
            if (_cogs[cog_name]):
                try:
                    print(f"Attempting to load cog \'{cog_name}\'")
                    module = importlib.import_module(cog_name)
                    class_ = getattr(module, cog_name)
                    self.add_cog(class_(self))
                except ImportError as err:
                    print(f" Unable to load cog \'{cog_name}\': {err}")
                except:
                    raise
        
        print(f"Bot initialization complete - ready to start with start()")
        return

    async def on_ready(self):
        #   This is where sys.stdout is different, reasign it back to "normal" 
        sys.stdout = self._stdout
        sys.stderr = self._stderr

        #   Runs upon successful login and connection to Discord API
        print(f"Bot ready: signed in as {self.user} (id:{self.user.id})")
        #   Store the guild (server) specified in secret config
        self.guild = discord.utils.get(self.guilds, name=self.secret['GUILD'])
        print(f"    Connected to the following guild: {self.guild.name} (id: {self.guild.id})")

        #   Wait until the shutdown interrupt is recieved
        while not self.__shutdown_flag:
            await asyncio.sleep(0.2)  #   Wait 200ms between checks while letting other coroutines run

        #   Exit & shutdown code
        print(f"Initiating shutdown")
        await self.close()
        print(f"Bot successfully closed")

    #   Create a method to run before the invocation of any command
    async def __bot_before_invoke(self, ctx):
        print(f"User '{ctx.author}' triggered the command '{ctx.command}' with '{ctx.message.content}'")
    
    #   Wrap starting code in a single method
    def __start_async_operations(self):
        #   Start the bot by connecting it to the Discord API
        print(f"Connecting bot to Discord API...")
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.login(self.secret['TOKEN']))
        self.loop.run_until_complete(self.connect())    #   Blocks here until disconnected

    def start(self, *, block=False):
        self.__shutdown_flag = False
        
        self.thread = threading.Thread(target=self.__start_async_operations)

        self.thread.start()
        print(f" Bot thread successfully started in Thread {self.thread.ident}")

        if block:
            self.thread.join()

    def stop(self, signum=None, frame=None):
        #   Stop bot and disconnect
        if signum is not None:
            print(f"Bot shutdown triggered via signal {signum} ({signal.Signals(signum).name});\
                \nframe was {frame}")
            self.do_not_revive = True
        else:
            print(f"Bot shutdown triggered")
        
        self.__shutdown_flag = True

        if threading.current_thread() is not self.thread:   #   Prevent badness (?) if called from inside the thread
            self.thread.join(5.0)   #   Wait on the thread to finish up for a bit
            if self.thread.is_alive():
                print(f"Forcibly stopped the bot thread... Check on this maybe?")
                self.thread._stop() #   Stop the thread if it hasn't already
        else:
            print(f"Shutdown triggered from inside thread.")

        self.clear()    #   Clean up the bot

        print(f"Bot exiting")


class BaseFunctionalityCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shutdown_cmd_flag = False
        print(f"Cog \'BaseFunctionalityCog\' initialized")
        return

    @command(name='version', help="""Echos bot version info""")
    async def version(self, ctx):
        await ctx.send(f"Kessel Bot - v{VERSION}")

    @command(name='shutdown', help="""Used to trigger bot shutdown from Discord""")
    async def shutdown(self, ctx, mode=""):
        check_flag = False
        for role_id in self.bot.secret["ADMIN_ROLES"]:
            check_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if check_role in ctx.author.roles:
                check_flag = True
                break

        if not check_flag:
            await ctx.send(f"You do not have permission to run this command!")
            return

        if self.shutdown_cmd_flag:
            mode = mode.lower()
            if mode == "":
                await ctx.send(f"Shutting down.")
                self.bot.do_not_revive = True
                self.bot.stop()
            elif mode == "restart":
                if self.bot.lives == 0:
                    await ctx.send(f"Shutting down.")
                else:
                    await ctx.send(f"Restarting. {self.bot.lives - 1} restarts left.")
                self.bot.stop()
            elif mode == "cancel":
                self.shutdown_cmd_flag = False
                await ctx.send(f"Shutdown canceled.")
            else:
                self.shutdown_cmd_flag = False
                await ctx.send(f"Shutdown canceled.")
        else:
            self.shutdown_cmd_flag = True
            await ctx.send(f"Do you really want to shut down? Use `{ctx.prefix}shutdown` to confirm, `{ctx.prefix}shutdown restart` to try restarting ({self.bot.lives} automatic restarts left), `{ctx.prefix}shutdown cancel` to cancel")

if __name__ == '__main__':
    # Start our tee
    PrinTee.start_printee_logging()

    #   Set up argument parser for command line
    parser = argparse.ArgumentParser(description="Kessel Bot")

    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument('--cfgpath', dest='configPath', metavar='<path>',\
        help='Path to configuration files (defaults to %(prog)s folder if not specified).')
    parser.add_argument('--secretcfg', dest='secret', metavar='<filename>',\
        default='secretConfig.json', help='Filename of secret config with token data (default: %(default)s).')
    parser.add_argument('--config', dest='config', metavar='<filename>', default='botConfig.json',\
        help='Filename of bot config with general data (default: %(default)s).')
    parser.add_argument('--debug', dest='debug', action='store_true',\
        help='Fall out bottom of program to allow access with interactive console. LAUNCH CONSOLE WITH -i PARAMETER')

    args = parser.parse_args()

    botInstance = KesselBot(configPath=args.configPath, config=args.config, secret=args.secret)

    
    botInstance.start() #   Launch the bot by telling it to start it's thread 

    if not args.debug:
        botInstance.thread.join()