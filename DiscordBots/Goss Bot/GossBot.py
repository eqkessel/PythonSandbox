# GossBot.py
import os
import argparse
import json

import asyncio
import discord
from discord.ext.commands import command, Bot, Cog, CommandNotFound

# PWD = os.path.dirname(os.path.abspath(__file__))

# SECRET_FILE = "secretConfig.json"
# CONFIG_FILE = "botConfig.json"

class GossBot(Bot):
    def load_config_file(self, file):
        with open(os.path.join(self.configPath, file)) as path:
            return json.load(path)

    def __init__(self, *args, secretConfig, config, configPath = None, **kwargs):
        print("Initializing Goss Bot...")

        self.FILE_DIR = os.path.dirname(os.path.abspath(__file__))

        if (not configPath):
            self.configPath = self.FILE_DIR
        else:
            self.configPath = configPath

        self.secretConfig = self.load_config_file(secretConfig)
        self.config = self.load_config_file(config)

        super(GossBot, self).__init__(**self.config['bot_options'])

        self.add_cog(FunCommands(self))

        # if (runMode == 'run'):
        #     #   Run and block
        #     self.run()
        # elif (runMode == 'start'):
        #     #   Start and pass
        #     await self.start()
        # else:
        return

    def run(self):
        try:
            self.start()
        except KeyboardInterrupt:
            print('KeyboardInterrupt recieved; stopping.')
            self.loop.run_until_complete(logout())
        finally:
            print('Closing loop.')
            loop.close()

    def start(self):
        print('Starting bot.')
        # try:
        #     await super(GossBot, self).start(self.secretConfig['TOKEN'])
        # except KeyboardInterrupt:
        #     print('KeyboardInterrupt recieved; stopping.')
        #     await self.stop()
        
        self.loop.run_until_complete(self.login(self.secretConfig['TOKEN']))
        self.loop.run_until_complete(self.connect())

    def stop(self):
        print('Stopping bot.')
        self.loop.run_until_complete(self.close())
        self.loop.close()

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, name=self.secretConfig['GUILD'])
        print(f'{self.user} connected to the following guild: {self.guild.name} (id: {self.guild.id})')

class FunCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @command()
    async def boilerup(self, ctx):
        await ctx.send(f'Hammer Down, {ctx.author.mention}!')

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Goss Scholars Discord Bot")

    parser.add_argument('--cfgpath', dest='configPath', metavar='<path>',\
        help='Path to configuration files (defaults to %(prog)s folder if not specified).')
    parser.add_argument('--secretcfg', dest='secretConfig', metavar='<filename>',\
        default='secretConfig.json', help='Filename of secret config with token data (default: %(default)s).')
    parser.add_argument('--config', dest='config', metavar='<filename>', default='botConfig.json',\
        help='Filename of bot config with general data (default: %(default)s).')

    mutexGroup0 = parser.add_mutually_exclusive_group()
    mutexGroup0.add_argument('-r, --run', action='store_true', dest='run', help='Run bot and block.')
    mutexGroup0.add_argument('-s, --start', action='store_true', dest='start', help='Start bot and pass.')

    arguments = parser.parse_args()
    #print(arguments)
    # mode = None
    # if(arguments.run):
    #     mode = 'run'
    # elif(arguments.start):
    #     mode = 'start'

    botInstance = GossBot(configPath=arguments.configPath, secretConfig=arguments.secretConfig,\
        config=arguments.config)

    botLoop = botInstance.loop

    botLoop.run_in_executor(None, botInstance.start())

    # if (arguments.start):
    #     #print(botInstance.loop)
    #     botInstance.loop.create_task(botInstance.start())
    #     # botInstance.loop.run_until_complete(botInstance.start())

# bot = GossBot()
# bot.run()