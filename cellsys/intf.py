#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Interference functions
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import numpy as np

def s(theta):
        return np.sin(theta)
def c(theta):
        return np.cos(theta)

class intf(object):
    def __init__(self, radius, power):
        # doining nothing now
        self.ptransmit = power
        self.radius = radius
        self.redge = radius * c(np.pi / 6)

    # Computes interfernce at position 'v' in the center cell
    # from the interfering cell at (ii, jj)
    def getInterference(self, icell, p, ptdbm, gamma):
        ptmw = 10 ** (ptdbm / 10)
        ptw = ptmw / 1000.0
        x = icell[0] * c(np.pi / 6)
        y = icell[1] + (icell[0] * s(np.pi / 6))
        center = np.asarray([2 * self.redge * x, 2 * self.redge * y])
        dist = np.linalg.norm(center - p)
        interference = ptw / (dist ** gamma)
        return interference

    def getSIR(self, icells, p, gamma):
        interference = 0
        for cell in icells:
            if(cell == (0, 0)):
                continue
            else:
                # the third argument can be anything as the pt term
                # doesn't exist in the final SIR expression
                interference += self.getInterference(cell, p, 30, gamma)
        desiredPower = self.getInterference((0, 0), p, self.ptransmit, gamma)
        sir = desiredPower / interference
        return sir
