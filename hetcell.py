#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Cell layout and CDF for Reuse > 1 with 120 degrees Sectoring
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

parser = argparse.ArgumentParser(description="Compute interference at one point.")
parser.add_argument("ntiers", type=int, help="no. of tiers around the reference cell to use")
parser.add_argument("freuse", type=int, help="reuse factor")
parser.add_argument("-s", action="store_true", help="enables sectoring; disabled by default")
args = parser.parse_args()

# cell radius (from center to either of the corners)
radius = 1000

# gamma
gamma = 3.5

# transmit power of base station (dBm)
pt = 30

# no. of random users in the center cell
npoints = 2000
npointsToShow = 50

# for progress bar
step = round(npoints / 50)

# read no. of tiers from stdin
ntiers = int(args.ntiers)

# read reuse factor from stdin
freuse = int(args.freuse)

# initializing my drawing, geometry, interference classes
# respectively
brush = cs.draw(radius)
geome = cs.geom(radius)
intrf = cs.intf(radius, pt)

reusedCells = geome.reuseCells(ntiers, freuse)
reusedCellsS = geome.reuseCellsSectored(ntiers)

both = [cell for cell in reusedCells if cell in reusedCellsS]

##############################################################
# Cell Layout
##############################################################
fig1 = pl.figure(1)
sectorColorsLight = ["#ddddff", "#007777", "#ffff62"]
sectorColorsDark = ["#8D8DA2", "#004C4C", "#A2A23E"]
brush.drawTiersSectoredHet(ntiers, both, (0, 0), fig1, [sectorColorsDark, sectorColorsLight])
##############################################################
# Interference
##############################################################
precision = 3
pointsList = []
sirList = []
count = npoints
print("Reuse " + str(freuse) + ", 120 degrees Sectoring: ", end='')
while(count > 0):
    thePoint = geome.getRandomPointInSector()
    pointsList.append(thePoint)
    sir = intrf.getSIR(both, thePoint, gamma)
    sirList.append(10 * np.log10(sir))
    if(count % step == 0):
        print("#", end="")
        sys.stdout.flush()
    count -= 1
print(" done !")

# Plot of random user points in the center hexagon
pointsListReduced = [pointsList[i] for i in range(0, npoints, int(npoints / npointsToShow))]
brush.drawPointsInHexagon(pointsListReduced, (0, 0), radius, fig1)
pl.title("Cell layout for Reuse " + str(freuse) + ", 120 degrees Sectoring")

fig2 = pl.figure(2)
srt = np.sort(sirList)
ff = np.array(range(npoints)) / float(npoints)
sectString = ", Reuse " + str(freuse) + ", 120 degrees Sectoring"
pl.plot(srt, ff, label="Reuse " + str(freuse) + ", 120 degrees Sectoring")
pl.title("CDF of SIRs for " + str(npoints) +" Users" + sectString)
pl.xlabel("SIR in dB")
pl.ylabel("Probability")
pl.grid()
pl.legend()

pl.show()
