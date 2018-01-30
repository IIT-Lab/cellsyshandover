#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Variation of blocking probability with
#   available no. of channels
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import numpy as np
import pylab as pl
import sys
import random

# arrival rate parameter 1/second
lambd = 1.0
# leaving rate parameter 1/(120 seconds)
beta = 120.0

# duration for cell system simulation in secs
duration = float(sys.argv[1])
step = 0.2
nsteps = duration / step
nstepsCopy = nsteps

nchlist = range(80, 150, 10)
blockPr = []

for nch in nchlist:
    nblocks = 0
    narrivals = 0
    nused = 0
    while(nsteps > 0):
        arr = np.random.binomial(1, lambd * step)
        dep = np.random.binomial(1, nused * (1 / beta) * step)
        narrivals += arr
        nused -= dep

        if(nused < nch):
            nused += arr
        else:
            nblocks += arr

        nsteps -= 1
    print((narrivals, nblocks, (nblocks / narrivals)))
    blockPr.append(nblocks / narrivals)
    nsteps = nstepsCopy

pl.plot(nchlist, blockPr)
pl.xlabel('No. of Available Channels')
pl.ylabel('Blocking Probability')
pl.grid()
pl.show()
