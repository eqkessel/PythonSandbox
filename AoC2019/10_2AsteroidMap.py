# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 21:56:03 2019

@author: redne
"""

from fractions import Fraction
from tqdm import tqdm
import math

rawMap = input("Map Data:")

mapGrid = rawMap.split("\n")
mapSize = (len(mapGrid[0]),len(mapGrid))
mapList = []

def getAngle(origin, target):
    #print(origin, '/', target)
    delX = target[0]-origin[0]
    delY = target[1]-origin[1]
    #print(delX,delY)
    ang = math.pi - math.atan2(delX, delY)
    if (ang < 0):
        #print(ang)
        ang += math.pi * 2
        #print("   ",ang)
    return ang

def getRange(origin, target):
    delX = target[0]-origin[0]
    delY = target[1]-origin[1]
    dist = math.sqrt(delX ** 2 + delY ** 2)
    return dist

astId = 0
for row in range(len(mapGrid)):
    currRow = mapGrid[row]
    for col in range(len(currRow)):
        currTile = currRow[col]
        if (currTile == '#' or currTile == 'X'):
            mapList.append({'coords':(col, row), 'id':astId}) 
            astId += 1

for origin in tqdm(mapList):
    origin['targets'] = []
    origin['angles'] = []
    origin['seen'] = 0
    originCoords = origin['coords']
    for target in mapList:
        targetCoords = target['coords']
        
#        if (originCoords == targetCoords):
#            #print(originCoords,targetCoords)
#            break
        targetAng  = getAngle(originCoords,targetCoords)
        targetDist = getRange(originCoords,targetCoords)
        if (originCoords != targetCoords):
            origin['targets'].append((targetAng, targetDist, targetCoords))
        if (targetAng not in origin['angles']):
            origin['angles'].append(targetAng)
            origin['seen'] += 1

sortList = sorted(mapList, key = lambda x: x['seen'])

station = sortList[-1]

print("\nAsteroid",station['coords'],"sees",station['seen'],"asteroids.")

newGrid = [['-'] * mapSize[0] for n in range(mapSize[1])]
for ast in sortList:
    row = ast['coords'][1]
    col = ast['coords'][0]
    newGrid[row][col] = 'o'
    
newGrid[station['coords'][1]][station['coords'][0]] = 'X'

xAxis = 'X: ' + ''.join([str(int(n/10)) for n in range(mapSize[0])]) + '\n   ' + ''.join([str(int(n%10)) for n in range(mapSize[0])]) + '\nY:'
print(xAxis)
for y in range(len(newGrid)):
    row = '{:0>2} '.format(y) + ''.join(newGrid[y])
    print(row)

targets = sorted(station['targets'])

killList = []
checkCount = len(targets)
killed = 0

print("Checking...", end='')
while (killed < checkCount):
    lastAng = None
    for n in range(len(targets)):
        trg = targets[n]
        if (trg == None):
            continue
        if (trg[0] == lastAng):
            continue
        lastAng = trg[0]
        
        killList.append(trg)
        targets[n] = None   # Pew pew!
        killed += 1
        
        #print(trg,killed,checkCount)

print("Done!")

#for n in range(len(killList)):
#    item = killList[n]
#    value = item[2][0] * 100 + item[2][1]
#    print("#{:0>3}: {:0>4} from point".format(n+1, value), item[2])

item = killList[199]
value = item[2][0] * 100 + item[2][1]
print("\n#200: {:0>4} from point".format(value), item[2])