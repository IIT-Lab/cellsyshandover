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
import time
import numpy as np
import pylab as pl
import math
import random
import argparse
import matplotlib.patches as patches

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
startPointCopy = startPoint
pl.scatter(startPoint[0], startPoint[1], s=5, color='#DB3236', zorder=101)
angle = 2 * np.pi * np.random.uniform()
directVector = np.asarray([np.cos(angle), np.sin(angle)])

speed1 = 3 * 5 / 18
speed2 = 30 * 5 / 18
speed3 = 120 * 5 / 18
speedList = [speed1, speed2, speed3]

# Origin
origin = np.asarray([0, 0])
# Hysterisis
H = 0
# Time step
tstep = 0.05
# Moving average filter length
movAvN = 10

fig2 = pl.figure(2)
for speed in speedList:
    print("Speed: " + str(speed * 18 / 5) + " Kmph")
    pprList = []
    for H in range(0, 5):
        print("H = " + str(H))
        startPoint = startPointCopy
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
        while(nhandoffs < 200):
            newLoc = prevLoc + (speed * tstep * directVector)
            if(geometry.isContainedInCircle(newLoc, origin, bounceCircleRadius)):
                prevLoc = newLoc
            else:
                (directVector, poi) = geometry.changeDirection(startPoint, directVector, bounceCircleRadius, origin)
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
            timeCounter += tstep
        print()
        print(("PPR", pingPongCounter, nhandoffs))
        pprList.append(pingPongCounter / nhandoffs)
    pl.plot(pprList, label=str(speed * 18 / 5))

axis = fig2.gca()
axis.legend(loc='upper right')
pl.grid()
pl.show()
print("Time: " + str((time.time() - startTime)))
