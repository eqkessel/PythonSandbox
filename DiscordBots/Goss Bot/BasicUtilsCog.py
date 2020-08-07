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

    @command(name='role', help="""Grants or removes vanity roles.\n\
        modes: 'list' - list valid role options\n\
               'add' - adds specified roles separated with spaces\n\
               'remove' - removes specified roles separated with spaces""")
    # @commands.has_role(bot.config['trusted_role'])
    async def role(self, ctx, mode: str, *roles):
        print(f"Command 'role' triggered by {ctx.author}")

        role_dict = self.bot.config['vanity_roles']
        print(f"User passed in these parameters: mode={mode}, roles={roles}")

        mode = mode.lower()
        
        if mode == 'list':
            print(f"User requested a list of valid roles")
            #   Assemble a message listing every vanity role found in the configs
            start = "Valid options for roles are:\n```"
            middle = '\n'.join([f"{i!r:<11} = {ctx.guild.get_role(role_dict[i])}" for i in role_dict])
            end = "\n```"
            await ctx.send(start + middle + end)

        elif mode == 'add':
            if len(roles) == 0:
                await ctx.send(f"Please specify one or more roles!")
                return
            lines = []
            for wanted_role in roles:
                print(f"Working on role '{wanted_role}'")
                #   Check to see if its a valid role
                try:
                    role_id = role_dict[wanted_role.lower()]
                except KeyError as e:
                    lines.append(f"Role alias '{e}' is not valid. See {ctx.prefix}role list for help.")
                    continue
                except:
                    raise
                #   Check to see if user already has role
                role_ref = ctx.guild.get_role(role_id)
                if role_ref in ctx.author.roles:
                    lines.append(f"You already have the role '{role_ref}'")
                    continue
                else:
                    lines.append(f"Gave you the role '{role_ref}'")
                    await ctx.author.add_roles(role_ref)
            
            await ctx.send("Command diagnositics:\n - " + '\n - '.join(lines))

        elif mode == 'remove':
            if len(roles) == 0:
                await ctx.send(f"Please specify one or more roles!")
                return
            lines = []
            for wanted_role in roles:
                print(f"Working on role '{wanted_role}'")
                #   Check to see if its a valid role
                try:
                    role_id = role_dict[wanted_role.lower()]
                except KeyError as e:
                    lines.append(f"Role alias '{e}' is not valid. See {ctx.prefix}role list for help.")
                    continue
                except:
                    raise
                #   Check to see if user has role
                role_ref = ctx.guild.get_role(role_id)
                if role_ref not in ctx.author.roles:
                    lines.append(f"You don't have the role '{role_ref}'")
                    continue
                else:
                    lines.append(f"Removed your role '{role_ref}'")
                    await ctx.author.remove_roles(role_ref)
            
            await ctx.send("Command diagnositics:\n - " + '\n - '.join(lines))
            
        else:
            raise commands.BadArgument(message=f"Invalid mode passed. Please refrence {ctx.prefix}help role")

        # await ctx.send(f'Sorry, not implemented yet {ctx.author.name}!')