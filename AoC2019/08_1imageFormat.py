# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 21:57:31 2019

@author: redne
"""

imgSize = (25, 6)
layerSize = imgSize[0] * imgSize[1]

class Layer:
    def __init__(self, aSize, aData):
        self.pixels = [[0] * aSize[0]] * aSize[1]
        self.fill(aData)
        
    def getNumVals(self, aVal):
        retVal = 0
        for row in self.pixels:
            for pix in row:
                if (pix == aVal):
                    retVal += 1
        return retVal
    
    def fill(self, aData):
        self.data = aData
        rows = [self.data[n*imgSize[0]:(n+1)*imgSize[0]] for n in range(imgSize[1])]
        for n in range(len(rows)):
            row = rows[n]
            self.pixels[n] = row 
                
            
image = input("Image is:\n")
image = [int(n) for n in image]

numLayers = int(len(image) / layerSize)
print(numLayers)
layers = [[Layer(imgSize,image[n*layerSize:(n+1)*layerSize]), None, None, None] for n in range(numLayers)]

for n in range(len(layers)):
    layer = layers[n]
    layers[n][1] = layers[n][0].getNumVals(0)
    layers[n][2] = layers[n][0].getNumVals(1) * layers[n][0].getNumVals(2)

#print(len(layers[0][0].pixels[0]))
    
sort = sorted(layers, key=lambda x: x[1])
print(sort[0])