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
npoints = 2000

# for progress bar
step = round(npoints / 50)

# read no. of tiers from stdin
ntiers = int(sys.argv[1])

# read reuse factor from stdin
freuse = int(sys.argv[2])

# initializing my drawing, geometry, interference classes
# respectively
brush = cs.draw(radius)
geome = cs.geom(radius)
intrf = cs.intf(radius, pt)

reusedCells = geome.reuseCells(ntiers, freuse)
if(len(reusedCells) == 1):
    print("No interference !!")
    sys.exit()

##############################################################
# Cell layout WITHOUT SECTORING
##############################################################

fig1 = pl.figure(1)
brush.drawLayout(ntiers, freuse, reusedCells, fig1)

##############################################################
# Interference WITHOUT SECTORING
##############################################################

precision = 3
pointsList = []
sirList = []
count = npoints
print("Without Sectoring: ", end='')
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

# Plot of random user points in the center hexagon
brush.drawPointsInHexagon(pointsList, (0, 0), radius, fig1)

cdfFig = pl.figure(2)
#pl.hist(sirList, 100, label="Reuse " + str(freuse) + ", No Sectoring")
srt = np.sort(sirList)
ff = np.array(range(2000)) / float(2000)
pl.plot(srt, ff, label="Reuse " + str(freuse) + ", No Sectoring")

##############################################################
# Cell layout WITH SECTORING
##############################################################

fig3 = pl.figure(3)
ax = fig3.gca()
figsz = math.ceil((3 * ntiers) * 0.8 * radius)
ax.set_xlim(-figsz, figsz)
ax.set_ylim(-figsz, figsz)
ax.set_aspect('equal')
sectorColorsLight = ["#ddddff", "#007777", "#ffff62"]
sectorColorsDark = ["#8D8DA2", "#004C4C", "#A2A23E"]
#brush.updateRadius(radius)
brush.drawTiersSectored(ntiers, (0, 0), fig3, [sectorColorsDark, sectorColorsLight])

##############################################################
# Interference WITH SECTORING
##############################################################
reusedCells = geome.reuseCellsSectored(ntiers)
if(len(reusedCells) == 1):
    print("No interference !!")
    sys.exit()

print("   With Sectoring: ", end='')
precision = 3
pointsListS = []
sirListS = []
while(npoints > 0):
    thePoint = geome.getRandomPointInSector()
    pointsListS.append(thePoint)
    sir = intrf.getSIR(reusedCells, thePoint, gamma)
    sirListS.append(10 * np.log10(sir))
    if(npoints % step == 0):
        print('#', end='')
        sys.stdout.flush()
    npoints -= 1
print(' done !')

# Plot of random user points in the center hexagon
#brush.drawPointsInHexagon(pointsListS, (0, 0), radius)

cdfFig = pl.figure(2)
#pl.hist(sirListS, 100, label="Reuse 1, 120 Sectoring")
srt = np.sort(sirListS)
ff = np.array(range(2000)) / float(2000)
pl.plot(srt, ff, label="Reuse 1, 120 Sectoring")
pl.grid()
pl.legend(loc='lower right')

pl.show()
