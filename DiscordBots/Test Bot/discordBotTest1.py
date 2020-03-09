# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 23:29:37 2020

@author: redne
"""

import discord

token = 'Njg2NDU2MzQ0MzQ1MzEzMjgx.XmXg0Q.Rzdec-3QZmrKwNREDJ_VRrwMDh0'
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('Njg2NDU2MzQ0MzQ1MzEzMjgx.XmXg0Q.Rzdec-3QZmrKwNREDJ_VRrwMDh0')