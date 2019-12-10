# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 21:56:03 2019

@author: redne
"""

from fractions import Fraction
from tqdm import tqdm
import math

rawMap = input("Enter map: ")

mapGrid = rawMap.split("\n")
mapList = []

def getAngle(origin, target):
    #print(origin, '/', target)
    delX = target[0]-origin[0]
    delY = target[1]-origin[1]
    #print(delX,delY)
    ang = math.atan2(delY, delX)
#    if (delX < 0):
#        ang += math.pi * 2
    return ang

astId = 0
for row in range(len(mapGrid)):
    currRow = mapGrid[row]
    for col in range(len(currRow)):
        currTile = currRow[col]
        if (currTile == '#'):
            mapList.append({'coords':(col, row), 'id':astId}) 
            astId += 1

for origin in tqdm(mapList):
    origin['angles'] = []
    origin['seen'] = 0
    for target in mapList:
        if (target == origin):
            pass
        targetAng = getAngle(origin['coords'],target['coords'])
        if (targetAng not in origin['angles']):
            origin['angles'].append(targetAng)
            origin['seen'] += 1

sortList = sorted(mapList, key = lambda x: x['seen'])

print(sortList[-1]['seen'],sortList[-1]['coords'])
    