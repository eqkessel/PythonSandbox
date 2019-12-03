# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:54:56 2019

@author: redne
"""

indata = input("Enter Input:\n")

wires = indata.split("\n")
segments = [n.split(",") for n in wires]

directions = {
        'R': (1,0),
        'L': (-1,0),
        'U': (0,1),
        'D': (0,-1)}

min_dist = 9999999999
intersections = []
num_intersections = 0

start_1 = [0,0]

for seg1 in segments[0]:
    dir_1 = directions[seg1[0]]
    dst_1 = int(seg1[1:])
    end_1 = [start_1[0] + (dst_1 * dir_1[0]), start_1[1] + (dst_1 * dir_1[1])]
    
    start_2 = [0,0]
    for seg2 in segments[1]:
        dir_2 = directions[seg2[0]]
        dst_2 = int(seg2[1:])
        end_2 = [start_2[0] + (dst_2 * dir_2[0]), start_2[1] + (dst_2 * dir_2[1])]
        
        if (((dir_1[0] * dir_2[0]) + (dir_1[1] * dir_2[1])) != 0):  # if not perpendicular
            start_2 = end_2
            continue    # don't bother!  
            
        if (dir_1[0] != 0):     # segment 1 horizontal, match y1 to x2
            y_1 = start_1[1]
            x_2 = start_2[0]
            xMax = max(start_1[0], end_1[0])
            xMin = min(start_1[0], end_1[0])
            yMax = max(start_2[1], end_2[1])
            yMin = min(start_2[1], end_2[1])
            # Check if the segments intersect
            if ((xMin < x_2 and x_2 < xMax) and (yMin < y_1 and y_1 < yMax)):
                print("Horizontal Intersection:", start_1, "->", end_1, "with", start_2, "->", end_2)
                intersections.append((x_2,y_1))
                num_intersections += 1
        else:   # segment 1 must be vertical, match x1 to y2
            x_1 = start_1[0]
            y_2 = start_2[1]
            xMax = max(start_2[0], end_2[0])
            xMin = min(start_2[0], end_2[0])
            yMax = max(start_1[1], end_1[1])
            yMin = min(start_1[1], end_1[1])
            # Check if the segments intersect
            if ((xMin < x_1 and x_1 < xMax) and (yMin < y_2 and y_2 < yMax)):
                print("Vertical Intersection:", start_1, "->", end_1, "with", start_2, "->", end_2)
                intersections.append((x_1,y_2))
                num_intersections += 1
        start_2 = end_2
    start_1 = end_1
    
for pt in intersections:
    dist = abs(pt[0]) + abs(pt[1])
    if dist < min_dist:
        min_dist = dist
        
print("\n\nMin Dist =", min_dist)