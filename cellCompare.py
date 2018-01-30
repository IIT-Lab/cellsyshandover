import cellsys as cs
import sys
import numpy as np
import pylab as pl
import math
import random

# cell radius (from center to either of the corners)
radius = 1000

# gamma
gamma = 3.5

# transmit power of base station (dBm)
pt = 30

# no. of random users in the center cell
npoints = 8000
# for progress bar
step = round(npoints / 50)

# initializing my drawing, geometry, interference classes
# respectively
brush = cs.draw(radius)
geome = cs.geom(radius)
intrf = cs.intf(radius, pt)

ntiers = 7

##############################################################
#  REUSE 3
##############################################################
reusedCells = geome.reuseCells(ntiers, 3)
if(len(reusedCells) == 1):
    print("No interference !!")
    sys.exit()
##############################################################
# Cell layout WITHOUT SECTORING
##############################################################
fig1 = pl.figure(1)
brush.drawLayout(ntiers, 3, reusedCells, fig1)
##############################################################
# Interference WITHOUT SECTORING Reuse 3
##############################################################
precision = 3
pointsList = []
sirList = []
count = npoints
print("  No Sectoring, Reuse 3: ", end='')
while(count > 0):
    thePoint = geome.getRandomPointInHex()
    pointsList.append(thePoint)
    sir = intrf.getSIR(reusedCells, thePoint, gamma)
    sirList.append(10 * np.log10(sir))
    if(count % step == 0):
        print('#', end='')
        sys.stdout.flush()
    count -= 1
print(' done !')

cdfFig = pl.figure(2)
srt = np.sort(sirList)
ff = np.array(range(npoints)) / float(npoints)
pl.plot(srt, ff, label="Reuse 3, No Sectoring")

##############################################################
#  REUSE 7
##############################################################
reusedCells = geome.reuseCells(ntiers, 7)
if(len(reusedCells) == 1):
    print("No interference !!")
    sys.exit()
##############################################################
# Cell layout WITHOUT SECTORING Reuse 7
##############################################################
fig3 = pl.figure(3)
brush.drawLayout(ntiers, 7, reusedCells, fig3)
##############################################################
# Interference WITHOUT SECTORING Reuse 7
##############################################################
precision = 3
pointsList = []
sirList = []
count = npoints
print("  No Sectoring, Reuse 7: ", end='')
while(count > 0):
    thePoint = geome.getRandomPointInHex()
    pointsList.append(thePoint)
    sir = intrf.getSIR(reusedCells, thePoint, gamma)
    sirList.append(10 * np.log10(sir))
    if(count % step == 0):
        print('#', end='')
        sys.stdout.flush()
    count -= 1
print(' done !')

cdfFig = pl.figure(2)
srt = np.sort(sirList)
ff = np.array(range(npoints)) / float(npoints)
pl.plot(srt, ff, label="Reuse 7, No Sectoring")

##############################################################
# Cell layout WITH SECTORING
##############################################################
fig4 = pl.figure(4)
ax = fig4.gca()
figsz = math.ceil((7 * np.exp(1.0)) * 0.75 * radius)
ax.set_xlim(-figsz, figsz)
ax.set_ylim(-figsz, figsz)
ax.set_aspect('equal')
sectorColorsLight = ["#ddddff", "#007777", "#ffff62"]
sectorColorsDark = ["#8D8DA2", "#004C4C", "#A2A23E"]
brush.drawTiersSectored(ntiers, (0, 0), fig4, [sectorColorsDark, sectorColorsLight])
##############################################################
# Interference WITH SECTORING
##############################################################
reusedCells = geome.reuseCellsSectored(ntiers)
if(len(reusedCells) == 1):
    print("No interference !!")
    sys.exit()

print("With Sectoring, Reuse 1: ", end='')
precision = 3
pointsListS = []
sirListS = []
count = npoints
while(count > 0):
    thePoint = geome.getRandomPointInSector()
    pointsListS.append(thePoint)
    sir = intrf.getSIR(reusedCells, thePoint, gamma)
    sirListS.append(10 * np.log10(sir))
    if(count % step == 0):
        print('#', end='')
        sys.stdout.flush()
    count -= 1
print(' done !')

cdfFig = pl.figure(2)
srt = np.sort(sirListS)
ff = np.array(range(npoints)) / float(npoints)
pl.plot(srt, ff, label="Reuse 1, 120 Sectoring")
pl.xlabel('SIR in dB')
pl.ylabel('Probability')
pl.grid()
pl.legend()

pl.show()
