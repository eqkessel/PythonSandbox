# bot.py
import os
import logging
import logging.config
import json

import discord
from dotenv import load_dotenv

class GossBot(discord.Client):
    def __init__(self, *args, bot_env = None, **kwargs):
        if (bot_env):
            self.bot_env = bot_env
        else:
            load_dotenv()
            self.bot_env = {
                'TOKEN': os.getenv('BOT_TOKEN'),
                'GUILD': os.getenv('BOT_GUILD')}

        # logging.config.fileConfig('logging.cfg')
        # self.log = log.getLogger(__name__)
        # self.log.setLevel(log.DEBUG)

        # streamLog = log.StreamHandler()
        # fileLog = log.


        super().__init__(**kwargs)
        
        return

    def run(self):
        super().run(self.bot_env['TOKEN'])

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, name=self.bot_env['GUILD'])
        print(
            f'{self.user} is connected to the following guild:\n'
            f'{self.guild.name}(id: {self.guild.id})'
        )

        members = '\n - '.join([member.name for member in self.guild.members])
        print(f'Guild Members:\n - {members}')

bot = GossBot()
bot.run()
