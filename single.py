#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 2
#
#   Handoff analysis
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import cellsys as cs
import sys
import time
import numpy as np
import pylab as pl
import math
import random
import argparse
import matplotlib.patches as patches

#
# Argument 1: Hysterisis value
# Argument 2: Speed
# Argument 3: Random reflections [or] (i = r) reflections
#

startTime = time.time()

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
hexList = np.asarray(brush.drawTiersSimple(ntiers, fig1, "#EEEEEE"))
hexListxy = geometry.ijtoxy(hexList)
axis = fig1.gca()
axis.add_patch(patches.Circle((0, 0), bounceCircleRadius, fill=False, ec="#0000FF"))

# Mobile Unit
startPoint = geometry.getRandomPointInHex()
pl.scatter(startPoint[0], startPoint[1], s=20, linewidth=2, facecolors='none', color='#36DB32', zorder=400, label="Starting Point")
angle = 2 * np.pi * np.random.uniform()
directVector = np.asarray([np.cos(angle), np.sin(angle)])

# Origin
origin = np.asarray([0, 0])

# Hysterisis
H = int(sys.argv[1])
print("H = " + str(H))

# Time step
tstep = 0.05

# Moving average filter length
movAvN = 10

# Speed
speed = float(sys.argv[2]) * (5 / 18);
print("Speed: " + str(speed * 18 / 5) + " Kmph")

# Random reflection [or] i = r
randomReflection = int(sys.argv[3])

nhandoffs = 0
prevLoc = startPoint
movAvFullList = signal.getRSS(startPoint, hexListxy, 0, 1)
movAvValues = movAvFullList
movAvFullList = [[x[1], ([x[0]] * movAvN)] for x in movAvFullList]
currentCell = (0, 0)
pingPongCounter = 0
timeCounter = 0
lastHandoff = [(0, 0), (0, 0)]
lastReflection = startPoint
reflections = 0
while(nhandoffs < 200):
    newLoc = prevLoc + (speed * tstep * directVector)
    if(geometry.isContainedInCircle(newLoc, origin, bounceCircleRadius)):
        prevLoc = newLoc
    else:
        reflections += 1
        if(randomReflection):
            ang = (1 / 2) * np.pi * np.random.uniform()
            (xVector, poi) = geometry.changeDirection(startPoint, directVector, bounceCircleRadius, origin)
            directVector = np.dot(np.asarray([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]]), directVector)
        else:
            (directVector, poi) = geometry.changeDirection(startPoint, directVector, bounceCircleRadius, origin)

        line = geometry.lineFromPoints(poi, lastReflection, 50)
        xx, yy = zip(*line)
        pl.plot(xx, yy, color="#00EEEE", zorder = 300, linewidth=1)

        lastReflection = poi
        dist = np.linalg.norm(poi - prevLoc)
        diff = (speed * tstep) - dist
        newLoc = poi + (diff * directVector)
        prevLoc = newLoc
        startPoint = poi
    rssList = signal.getRSS(newLoc, hexListxy, 0, 1)
    for i in range(0, len(rssList)):
        movAvFullList[i][1].pop(0)
        movAvFullList[i][1].append(rssList[i][0])
        movAvValues[i][0] = np.mean(movAvFullList[i][1])
    v1 = max(movAvValues)
    currentCellRSS = [x[0] for x in movAvValues if (x[1] == currentCell)]
    currentCellRSS = currentCellRSS[0]
    if(v1[0] > (currentCellRSS + H)):
        if(v1[1] != currentCell):
            sys.stdout.write("\r")
            progress = int((nhandoffs / 200) * 100) + 1
            percent = "{:2}".format(progress)
            sys.stdout.write(" " + percent + " % ")
            [print("#", end="") for i in range(0, int(progress / 2))]
            sys.stdout.flush()
            currentHandoff = [currentCell, v1[1]]
            nhandoffs += 1
            if((lastHandoff[0] == currentHandoff[1]) and (lastHandoff[1] == currentHandoff[0])):
                if(timeCounter < 1):
                    pingPongCounter += 1
            lastHandoff = [currentCell, v1[1]]
            currentCell = v1[1]
            timeCounter = 0
            pl.scatter(newLoc[0], newLoc[1], s=5, facecolors='none', color='#DB3236', zorder=200)
    timeCounter += tstep

if(reflections == 0):
    line = geometry.lineFromPoints(newLoc, startPoint, 100)
else:
    line = geometry.lineFromPoints(newLoc, lastReflection, 100)
xx, yy = zip(*line)
pl.plot(xx, yy, color="#00EEEE", zorder = 300, linewidth=1)
print()
print(("PPR", pingPongCounter, nhandoffs))

axis = fig1.gca()
axis.legend(loc='upper right')
print("Time: " + str((time.time() - startTime)))
pl.show()
