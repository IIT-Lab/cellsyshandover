import numpy as np
import pylab as pl
import sys
import math
import random

#np.random.poisson(1.0)
lambd = 1.0
#np.random.exponential(120.0)
beta = 120.0

# duration for cell system simulation in secs
#nch = int(sys.argv[1])
duration = float(sys.argv[1])
step = 0.5
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
            if(arr):
                nused += arr
        else:
            if(arr):
                nblocks += 1
        nsteps -= 1
    print((narrivals, nblocks, (nblocks / narrivals)))
    blockPr.append(nblocks / narrivals)
    nsteps = nstepsCopy

pl.plot(nchlist, blockPr)
pl.xlabel('No. of Available Channels')
pl.ylabel('Blocking Probability')
pl.grid()
pl.show()
