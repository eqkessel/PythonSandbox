# GossBot.py
import os
import json

import discord
from discord.ext.commands import command, Bot, Cog, CommandNotFound

PWD = os.path.dirname(os.path.abspath(__file__))

SECRET_FILE = "secretConfig.json"
CONFIG_FILE = "botConfig.json"

def load_json_filepath(file):
    with open(os.path.join(PWD, file)) as path:
        return json.load(path)

class GossBot(Bot):
    def __init__(self, *args, **kwargs):
        self.secretConfig = load_json_filepath(SECRET_FILE)
        self.config = load_json_filepath(CONFIG_FILE)

        print("Initializing Goss Bot...")

        super(GossBot, self).__init__(**self.config['bot_options'])

        self.add_cog(FunCommands(self))
        return

    def run(self):
        super(GossBot, self).run(self.secretConfig['TOKEN'])

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, name=self.secretConfig['GUILD'])
        print(f'{self.user} connected to the following guild: {self.guild.name} (id: {self.guild.id})')

class FunCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @command()
    async def boilerup(self, ctx, *, member: discord.Member = None):
        await ctx.send(f'Hammer Down, {ctx.author.mention}!')

bot = GossBot()
bot.run()