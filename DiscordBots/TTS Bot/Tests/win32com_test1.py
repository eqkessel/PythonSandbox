# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 21:58:19 2020

@author: redne
"""

# Python program to convert 
# text to speech 
  
# import the required module from text to speech conversion 
import win32com.client 
  
# Calling the Disptach method of the module which  
# interact with Microsoft Speech SDK to speak 
# the given input from the keyboard 
  
speaker = win32com.client.Dispatch("SAPI.SpVoice") 
  
while 1: 
    print("Enter the word you want to speak it out by computer") 
    s = input() 
    speaker.Speak(s) 
  
# To stop the program press 
# CTRL + Z 