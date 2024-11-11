#!/usr/bin/env python

# Calculate the value of E

import sys, time

if sys.version_info[0] < 3 or \
    (sys.version_info[0] == 3 and sys.version_info[1] < 3):
    timefunc = time.clock
else:
    timefunc = time.process_time

def calce(iii):

    nn = 1. ; ff = 1.
    for aa in range(1, iii):
        # factorial
        ff *= aa
        #if aa % 100 == 0:
        #    print aa, nn, 1. / aa, ff
        # add reciproc
        nn += 1. / ff
    return nn

while 1:
    nnn = input("Enter number of iterations: (ctrl-c to stop) ")

    oldTime = timefunc()
    nn = calce(int(nnn))
    newTime = timefunc()
    timeDiff = newTime - oldTime
    print(nn)
    print ("Calculation completed in %.3f" % (1000*timeDiff) + " ms of CPU time")

# EOF
