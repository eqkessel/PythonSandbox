# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:12:07 2020

@author: redne
"""

import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""


engine.setProperty('rate', 225)     # setting up new voice rate
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate


"""VOLUME"""

engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say('My current speaking rate is ' + str(rate))
engine.say('My current volume is ' + str(int(volume * 100)) + '%')
engine.runAndWait()
engine.stop()