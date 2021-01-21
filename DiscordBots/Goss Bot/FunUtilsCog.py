#   FunUtilsCog.py
#   Contains fun utility commands for KesselBot
#   Written by Ethan Kessel (c) 2020

import asyncio
import discord
from discord.ext.commands import command, Bot, Cog, CommandNotFound

class FunUtilsCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"Cog '{__name__}' initialized")
        return

    @command()
    async def boilerup(self, ctx):
        print(f"Command '!boilerup' triggered by {ctx.author}")
        await ctx.send(f'Hammer Down, {ctx.author.mention}!')