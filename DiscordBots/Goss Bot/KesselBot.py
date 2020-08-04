#   KesselBot.py v0.1
#   Custom General-Purpose Utility Discord Bot
#   Written by Ethan Kessel (c) 2020

import os
import sys
import importlib
import argparse
import json
import threading
# from threading import Thread
import signal

import asyncio
import discord
from discord.ext.commands import command, Bot, Cog, CommandNotFound

import PrinTee

VERSION = "0.2.2"

class KesselBot(Bot):
    #   Load .json file given a path and filename, used to get configs
    @staticmethod
    def load_json_from_path(path, filename):
        with open(os.path.join(path, filename)) as filepath:
            return json.load(filepath)

    #   Constructor: takes filenames for config and secret files, path to configs (defaults to local dir)
    def __init__(self, *args, configPath = None, config, secret, **kwargs):
        print(f"Initializing KesselBot v{VERSION}")
        
        #   Asyncio creates its own console which means PrinTee doesn't tee off of it
        #   Save the right console to fix it.
        # print(f"sys.stdout is {sys.stdout} : {repr(sys.stdout)} : {type(sys.stdout)}")
        self._stdout = sys.stdout
        self._stderr = sys.stderr

        #   Save the local dir for future reference
        self.FILE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not configPath:
            self.configPath = self.FILE_DIR
        else:
            self.configPath = configPath
        
        print(f"Loading configs from {self.configPath}")
        self.config = self.load_json_from_path(self.configPath, config)
        self.secret = self.load_json_from_path(self.configPath, secret)

        # print(f"Initializing thread component")
        # #   Class extends threading.Thread, need to initialize thread
        # threading.Thread.__init__(self)

        print(f"Initializing bot component")
        #   Run parent class Bot constructor using options from config
        super(KesselBot, self).__init__(**self.config['bot_options'])

        #   Set up a private variable to monitor for shutdown
        self.__shutdown_flag = False
        #   Set up a thread Event object to watch for shutdown
        # self.__shutdown_event = threading.Event()

        print(f"Loading bot Cogs:")
        #   Load bot "Cogs" - contain grouped functionality
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
        # print(f" BEFORE : sys.stdout is {sys.stdout} : {repr(sys.stdout)} : {type(sys.stdout)}")
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        # print(f"  AFTER : sys.stdout is {sys.stdout} : {repr(sys.stdout)} : {type(sys.stdout)}")

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

    # class BotStopInterrupt(Exception):
    #     pass

    def start(self):
        self.__shutdown_flag = False
        # #   Overload of threading.Thread; call with start()
        # print(f"Bot started in Thread {self.ident}")

        #   Start the bot by connecting it to the Discord API
        print(f"Connecting bot to Discord API...")
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.login(self.secret['TOKEN']))
        self.loop.run_until_complete(self.connect())    #   Blocks here until disconnected

        self.clear()

        print(f"Bot exiting")

        # #   Should run on successful bot exit
        # printf(f"Stopping Thread {self.ident}")

    # def start(self):
    #     #   Start the bot by connecting it to the Discord API
    #     print(f"Connecting bot to Discord API")
    #     try:
    #         asyncio.set_event_loop(self.loop)
    #         self.loop.run_until_complete(self.login(self.secret['TOKEN']))
    #         self.loop.run_until_complete(self.connect())
    #     except KeyboardInterrupt:
    #         print("KeyboardInterrupt recieved")
    #     except KesselBot.BotStopInterrupt:
    #         print("BotStopInterrupt recieved")
    #     finally:
    #         self.stop()
    #         # self.loop.run_until_complete(self.close())
    #         # self.loop.close()

    def stop(self, signum = None, frame = None):
        #   Stop bot and disconnect
        if not signum:
            print(f"Bot shutdown triggered, stopping")
        else:
            print(f"Bot shutdown triggered via {signum}, stopping")
        self.__shutdown_flag = True
        #raise KesselBot.BotStopInterrupt
        # self.loop.close()
        # self.loop.run_until_complete(self.close())
        # self.loop.close()

if __name__ == '__main__':
    # print(f"sys.stdout is {sys.stdout} : {repr(sys.stdout)} : {type(sys.stdout)}")
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

    # def spawn_bot(*args, **kwargs):
    #     botInstance = KesselBot(*args, **kwargs)
    #     botInstance.start()

    # botThread = threading.Thread(target=spawn_bot, )

    botInstance = KesselBot(configPath=args.configPath, config=args.config, secret=args.secret)

    # botInstance.start()
    botThread = threading.Thread(target=botInstance.start)

    def kill(*args):
        botInstance.stop(*args)
        botThread.join(0.2)
        try:
            botThread._stop()
        except:
            pass
        quit()

    #   Register shutdown signal handlers
    signal.signal(signal.SIGTERM, kill)
    signal.signal(signal.SIGINT, kill)

    botThread.start()
    # botInstance.Thread.start()
    print(f" Bot thread successfully started")

    if not args.debug:
        while True:
            botThread.join(0.2)
    # try:
    #     botThread = threading.Thread(target=botInstance.start)
    #     timer = threading.Timer(30.0, botInstance.stop)
    #     botThread.start()
    #     print(f"Bot thread successfully started")

    #     # timer.start()
    #     # timer.join()
    #     # print(f"Timer expired")

    #     quit()
    # finally:
    #     print(f"Exiting")
    #     botThread._stop()