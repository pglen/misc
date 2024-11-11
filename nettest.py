#!/usr/bin/env python

import sys, psutil, time, datetime

nio_prev = []

def netstat():

    global nio_prev
    nio = psutil.net_io_counters(True)
    if nio_prev:
        for aa in nio.keys():
            #print("%7d %7d %s" % (nio[aa][0] // 1024, nio[aa][1] // 1024, aa))
            upx     =  nio[aa][0] // 1024 - nio_prev[aa][0] // 1024
            downx   =  nio[aa][1] // 1024 - nio_prev[aa][1] // 1024
            if upx or downx:
                dd = datetime.datetime.now()
                ddd = dd.strftime("%Y/%m/%d %H:%M:%S")
                print("%s %6d %6d   %s" % (ddd, upx, downx, aa))
    nio_prev = nio

# Dump processes that are heavy consumers

def testnet():

    while True:
        cpu = psutil.cpu_percent(1)
        if 1: #cpu > 75:
            #print("CPU", cpu)
            netstat()
        time.sleep(1)

if __name__ == "__main__":

    #print(dir(psutil))
    #sys.exit(0)
    print("Date                  Sent    Rec   IF")
    testnet()

# EOF
