# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:32:18 2020

@author: redne
"""

from gtts import gTTS
import pygame
from io import BytesIO
import os

pygame.init()

def say(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
say("this is a test of Google Text-To-Speech integrated with pygame")