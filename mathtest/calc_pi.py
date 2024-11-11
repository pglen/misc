#!/usr/bin/env python

import os, sys, math, time

# ------------------------------------------------------------------------
# Optimized PI calc in py. Possibly the simplest function to get PI

def getpi(nn):

    nnn = nn * nn

    area = 0.00;  xx = 1.                       # init vars
    cx = 1.00 / nn;                             # integral delta coefficent
    while xx > 0:
        area += math.sqrt(1 - xx * xx)
        xx -= cx                                # accum instead of mult
    area /= cx * nnn                            # unroll from loop
    return 4.00 * area

if sys.version_info[0] < 3 or \
    (sys.version_info[0] == 3 and sys.version_info[1] < 3):
    timefunc = time.clock
else:
    timefunc = time.process_time

while 1:
    nnn = input("Enter number of iterations: (ctrl-c to stop) ")
    oldTime = timefunc()
    piCalc = getpi(int(nnn))
    newTime = timefunc()
    timeDiff = newTime - oldTime
    print (piCalc)
    print ("Calculation completed in %.3f" % (1000*timeDiff) + " ms of CPU time")



