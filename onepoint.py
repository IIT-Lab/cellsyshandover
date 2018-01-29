# interference at one point

import cellsys as cs
import sys
import numpy as np
import pylab as pl

Rc = 1000.0 # meters
pt = 30 # dBm
gamma = 3.5

ntiers = int(sys.argv[1])
freuse = int(sys.argv[2])

brush = cs.draw(Rc)
g = cs.geom(Rc)
intf = cs.intf(Rc, pt)

icells = g.reuseCells(ntiers, freuse)
#icells = g.reuseCellsSectored(ntiers)
icellsxy = g.ijtoxy(icells)

# generating a random point in the
# reference cell at the center
point = g.getRandomPointInHex()
#point = (30, 30)

sir = intf.getSIR(icells, point, gamma)

#print(sir, end="")
#print(" at ", end="")
print(10 * np.log10(sir), end="")
print(" dB at ", end="")
print(point)

#sectorColorsLight = ["#ddddff", "#007777", "#ffff62"]
#sectorColorsDark = ["#8D8DA2", "#004C4C", "#A2A23E"]
fig = pl.figure()
#brush.drawTiersSectored(ntiers, (0, 0), fig, [sectorColorsDark, sectorColorsLight])
brush.drawLayout(ntiers, freuse, icells, fig)
pl.scatter(point[0], point[1], color="#2222FF", s=30, zorder=2)
for cellxy in icellsxy:
    line = g.lineFromPoints(point, cellxy, 100)
    xx, yy = zip(*line)
    if(cellxy != (0, 0)):
        pl.plot(xx, yy, color="#222222", zorder = 100, linewidth=1)

ax = fig.gca()
#ax.annotate('P', xy=point, zorder=200, color="#DB3236", fontsize=20)
pl.show()
