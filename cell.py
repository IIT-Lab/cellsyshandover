#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Cell layout and CDF for a configuration
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import cellsys as cs
import sys
import numpy as np
import pylab as pl
import math
import random
import argparse
import matplotlib.patches as patches

# cell radius (from center to either of the corners)
radius = 250

# bouncing circle radius
bounceCircleRadius = 3.12 * radius

# transmit power of base station (dBm)
pt = 30

# 2 tiers
ntiers = 2

# initializing my drawing, geometry, interference classes
# respectively
brush = cs.draw(radius)
geometry = cs.geom(radius)
signal = cs.intf(radius, pt)

##############################################################
# Cell Layout
##############################################################
fig1 = pl.figure(1)
hexList = brush.drawTiersSimple(ntiers, fig1, "#EEEEEE")
axis = fig1.gca()
axis.add_patch(patches.Circle((0, 0), bounceCircleRadius, fill=False, ec="#0000FF"))
# Mobile Unit
startPoint = geometry.getRandomPointInHex()
pl.scatter(startPoint[0], startPoint[1], s=5, color='#DB3236', zorder=101)
speed = 3 * 5 / 18
angle = 2 * np.pi * np.random.uniform()
directVector = np.asarray([np.cos(angle), np.sin(angle)])

speed1 = speed
speed2 = 30 * 5 / 18
speed3 = 120 * 5 / 18

# Hysterisis in dB
H = 2

nhandoffs = 0
# t in ms
# 50ms is the time resolution for computing RSS
t = 0
#tstep = 4000 * 0.05
tstep = 0.05
prevLoc = startPoint
k = 0

movAvN = 1
movAvFullList = signal.getRSS(startPoint, hexList)
movAvValues = movAvFullList
# Assume last value is the latest
movAvFullList = [[x[1], ([x[0]] * movAvN)] for x in movAvFullList]
currentCell = (0, 0)
#while(k <= 5):
pingPongCounter = 0
timeCounter = 0
lastHandoff = [(0, 0), (0, 0)]
while(nhandoffs < 200):
    newLoc = prevLoc + (speed3 * tstep * directVector)
    if(geometry.isContainedInCircle(newLoc, (0, 0), bounceCircleRadius)):
        prevLoc = newLoc
    else:
        #print("reflection")
        (directVector, poi) = geometry.changeDirection(startPoint, directVector, bounceCircleRadius, np.asarray([0, 0]))
        dist = np.linalg.norm(poi - prevLoc)
        diff = (speed * tstep) - dist
        newLoc = poi + (diff * directVector)
        prevLoc = newLoc
        startPoint = poi
    pl.scatter(newLoc[0], newLoc[1], s=0.1, color='#00FF00', zorder=100)
    rssList = signal.getRSS(newLoc, hexList)
    #print([x[1] for x in rssList])
    # Updating the rss moving average values

    for cell in rssList:
        [x[1].pop(0) for x in movAvFullList if (x[0] == cell[1])]
        [x[1].append(cell[0]) for x in movAvFullList if (x[0] == cell[1])]
        newAv = np.mean([x[1] for x in movAvFullList if (x[0] == cell[1])])
        index = [i for i in range(0, len(movAvValues)) if (movAvValues[i][1] == cell[1])]
        movAvValues[index[0]][0] = newAv
    """
    for i in range(0, len(movAvValues)):
        movAvFullList[i][1].pop(0)
        movAvFullList[i][1].append(rssList[i][0])
        movAvValues[i][0] = np.mean(movAvFullList[i][1])
    """
    movAvValues.sort()
    rev = movAvValues
    rev.reverse()
    v1 = rev[0]
    v2 = rev[1]
    currentCellRSS = [x[0] for x in movAvValues if (x[1] == currentCell)]
    currentCellRSS = currentCellRSS[0]
    if(v1[0] > (currentCellRSS + H)):
    #if(v1[0] > (v2[0] + H)):
        if(v1[1] != currentCell):
            # perform handoff !!
            #print("Handoff !! " + str(currentCell) + " -> " + str(v1[1]))
            #sys.stdout.write("\033[K")
            sys.stdout.write("\r")
            progress = int((nhandoffs / 200) * 100) + 1
            percent = "{:2}".format(progress)
            sys.stdout.write(" " + percent + " % ")
            [print("#", end="") for i in range(0, int(progress / 2))]
            #print(percent + " %")
            sys.stdout.flush()
            currentHandoff = [currentCell, v1[1]]
            nhandoffs += 1
            if((lastHandoff[0] == currentHandoff[1]) and (lastHandoff[1] == currentHandoff[0])):
                # ping pong !!
                if(timeCounter < 1):
                    pingPongCounter += 1
            lastHandoff = [currentCell, v1[1]]
            currentCell = v1[1]
            timeCounter = 0
            #pl.scatter(newLoc[0], newLoc[1], s=5, color='#00FF00', zorder=102)
            pl.scatter(newLoc[0], newLoc[1], s=10, facecolors='none', color='#DB3236', zorder=200)
    timeCounter += tstep
    k += 1

print()
print(("PPR", pingPongCounter, nhandoffs))
pl.show()
