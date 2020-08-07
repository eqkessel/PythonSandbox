#   ErrorHandlingCog.py
#   Contains general command error handling for KesselBot
#   Written by Ethan Kessel (c) 2020

import traceback
import sys
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import command, Bot, Cog, CommandNotFound

class ErrorHandlingCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"Cog \'{__name__}\' initialized")
        return

    #   Error Handler - See link below for original idea
    #   https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    @Cog.listener()
    async def on_command_error(self, ctx, error):
        #   First thing: pipe all errors to the console for logging using traceback
        print(f"Handling exception in command {ctx.command}", file=sys.stderr)
        # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        #   Prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        #   Prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        #   Check for original exceptions raised and sent to CommandInvokeError.
        #   If nothing is found, keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            print(f"Ignoring exception:\n{error}")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing arguments: <{error.param}>")

        elif isinstance(error, commands.MissingRole):
            await ctx.send(f"You require the role '{error.missing_role.name}' to run this command.")

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        #   Ethan here, I have no idea what this does
        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')
            else:
                await ctx.send(error)
            # elif error.message != None:
            #     await ctx.send(error.message)
            # else:
            #     print(f"Encountered BadArgument exception with no message!")
            #     traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(f"Exception unhandled, ignoring")
            # print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)