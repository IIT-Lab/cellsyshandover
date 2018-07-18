Simulation of a Cellular System With Handovers and Ping-Pong Rate Computation

1. The simulation is written completely in Python 3

2. The following python packages are used:

      (a) matplotlib (containes numpy, pylab)

        -> To install, type sudo pip3 install matplotlib

      (b) sys, math, random

        -> No installation needed.

3. A new custom python package called cellsys was created by me for this simulation
and it has 3 classes:

     i. draw : for drawing/visualization

     ii. geom : for geometrical operations on cells and cell layouts

    iii. intf : for interference, SIR computations

4. The whole simulation is generalized i.e. the code can be used to draw layouts
or compute SIRs for any reasonable reuse factor and any reasonable no. of tiers.
