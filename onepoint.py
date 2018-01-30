#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Interference at one point
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import cellsys as cs
import sys
import numpy as np
import pylab as pl
import argparse

parser = argparse.ArgumentParser(description='Compute interference at one point.')
parser.add_argument('ntiers', type=int, help='no. of tiers around the reference cell to use')
parser.add_argument('freuse', type=int, help='reuse factor')
parser.add_argument('-s', action="store_true", help='enables sectoring; disabled by default')
args = parser.parse_args()

Rc = 1000.0 # meters
pt = 30 # dBm
gamma = 3.5

ntiers = args.ntiers
freuse = args.freuse

brush = cs.draw(Rc)
g = cs.geom(Rc)
intf = cs.intf(Rc, pt)

if(not args.s):
    print("No Sectoring")
    icells = g.reuseCells(ntiers, freuse)
else:
    print("120 degree Sectoring")
    icells = g.reuseCellsSectored(ntiers)

if(icells == []):
    print("No Interference !!!!!!!")
    sys.exit()
icellsxy = g.ijtoxy(icells)

# generating a random point in the
# reference cell at the center and computing SIR
if(not args.s):
    point = g.getRandomPointInHex()
else:
    point = g.getRandomPointInSector()

sir = intf.getSIR(icells, point, gamma)

fig = pl.figure()
if(not args.s):
    brush.drawLayout(ntiers, freuse, icells, fig)
else:
    sectorColorsLight = ["#ddddff", "#007777", "#ffff62"]
    sectorColorsDark = ["#8D8DA2", "#004C4C", "#A2A23E"]
    brush.drawTiersSectored(ntiers, (0, 0), fig, [sectorColorsDark, sectorColorsLight])

pl.scatter(point[0], point[1], color="#2222FF", s=30, zorder=2)
for cellxy in icellsxy:
    line = g.lineFromPoints(point, cellxy, 100)
    xx, yy = zip(*line)
    if(cellxy != (0, 0)):
        pl.plot(xx, yy, color="#222222", zorder = 100, linewidth=1)

ax = fig.gca()
pl.title("SIR = " + str(10 * np.log10(sir)) + " dB at \n" + str(point))
pl.show()
