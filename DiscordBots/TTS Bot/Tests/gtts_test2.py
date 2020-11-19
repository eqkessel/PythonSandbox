# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:18:45 2020

@author: redne
"""

"""
from gtts import gTTS
from io import BytesIO

mp3_fp = BytesIO()
tts = gTTS('hello', lang='en')
tts.write_to_fp(mp3_fp)
"""

from gtts import gTTS
from time import sleep
import os
import pyglet

tts = gTTS(text='Hello World', lang='en')
filename = 'temp.mp3'
tts.save(filename)

music = pyglet.media.load(filename, streaming=False)
music.play()

sleep(music.duration) #prevent from killing
os.remove(filename) #remove temperory file