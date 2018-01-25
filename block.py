import numpy as np
import pylab as pl
import sys
import math
import random

def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

#np.random.poisson(1.0)
lambd = 1.0
#np.random.exponential(120.0)
beta = 120.0

# duration for cell system simulation in secs
nch = int(sys.argv[1])
duration = float(sys.argv[2])

arrAcc = 0
times = []

arrivals = []
departs = []

while(arrAcc < duration):
    # time until the next call
    tm = nextTime(1)
    #print(tm)

    # the time w.r.t t=0
    arrAcc += tm

    times.append((arrAcc, 'a', 'r'))
    arrivals.append(arrAcc)

    # possible call duration
    callDur = np.random.exponential(beta)
    #print(callDur)
    # mark the future call leaving time from call arrival time
    if((arrAcc + callDur) < duration):
        times.append((arrAcc + callDur, 'l', 'g'))
        departs.append(arrAcc + callDur)

times.sort()

colors = [item[2] for item in times]
tms = [item[0] for item in times]

yy = [1 for x in arrivals]
pl.scatter(arrivals, yy, color='#DB3236', s=0.5)
yy = [1.1 for x in departs]
pl.scatter(departs, yy, color='#32DB36', s=0.5)
#pl.plot(departs, color='#32DB36')
pl.show()

free = nch
nblocks = 0
narrivals = 0
blockedTimes = []

blockedTime = 0
blockedFlag = 0

for tm in times:
    if(tm[1] == 'l'):
        free += 1
        if(free == 1):
            blockedTime += (tm[0] - blockedFlag)
            blockedFlag = 0
        if(free >= nch):
            free = nch
    else:
        if(free > 0):
            free -= 1
            if(free == 0):
                blockedFlag = tm[0]

#print((narrivals, nblocks, (nblocks / narrivals)))

print((blockedTime, duration, (blockedTime / duration)))

#tms = [aa[0] for aa in times]
#pl.plot(tms)
#pl.show()
