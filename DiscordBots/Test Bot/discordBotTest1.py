# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 23:29:37 2020

@author: redne
"""

import discord

token = 'Njg2NDU2MzQ0MzQ1MzEzMjgx.XmXmoA.ROvkeLojSRmo_7KWyhWQCRpJPzU'
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    welcome_channel_target = None
    for chnl in client.get_all_channels():
        print('Channel \'{0}\' is {1}'.format(chnl, type(chnl)))
        if (chnl.type == discord.ChannelType.text):
            if (chnl.position == 0):
                welcome_channel_target = chnl

    client.get_channel
    await welcome_channel_target.send('{0.user}: Logged on.'.format(client), tts=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)