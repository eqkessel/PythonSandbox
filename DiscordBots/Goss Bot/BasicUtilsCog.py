#   BasicUtilsCog.py
#   Contains utility commands for KesselBot
#   Written by Ethan Kessel (c) 2020

import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import command, Bot, Cog, CommandNotFound

class BasicUtilsCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"Cog \'{__name__}\' initialized")
        return

    #   Check run for all commands in this cog
    async def cog_check(self, ctx):
        required_role = discord.utils.get(ctx.guild.roles, name=self.bot.config['trusted_role'])
        print(f"Checking role {required_role} against user's roles.")
        if required_role in ctx.author.roles:
            return True
        else:
            raise commands.MissingRole(required_role)
            return False

    @command(name='role', help='Grants or removes vanity roles.')
    # @commands.has_role(bot.config['trusted_role'])
    async def role(self, ctx, mode, *roles):
        print(f"Command 'role' triggered by {ctx.author}")
        # print(f"{ctx.author.roles}")
        # if self.bot.config['trusted_role'] not in ctx.author.roles:
        #     await ctx.send(f'You are not authorized to use this command {ctx.author.mention}')
        #     return
        await ctx.send(f'Sorry, not implemented yet {ctx.author.mention}!')