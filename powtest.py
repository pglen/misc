#!/usr/bin/env python

import sys, psutil, time, datetime

def printstat():

    sumx = ""
    for aa in psutil.process_iter():
        #if aa.status() == psutil.STATUS_SLEEPING:
        #    pass
        #print(dir(aa))

        try:
            #cc = aa.cpu_times()
            #print(aa._pid, cc.user, cc.system, aa.cpu_percent(), aa.exe())
            ppp = aa.cpu_percent()
            if  ppp > 5:
                dd = datetime.datetime.now()
                ddd = dd.strftime("%Y/%m/%d %H:%M:%S")
                #print(aa._pid, cc.user, cc.system, aa.cpu_percent(), aa.exe())
                sumx += "%s %5d %3d%% %s\n" % (ddd, aa._pid, ppp, aa.exe())
        except psutil.AccessDenied:
            pass
        except:
            print(sys.exc_info())
            pass
    print(sumx)


# Dump processes that are heavy consumers

def testpower():

    while True:
        cpu = psutil.cpu_percent(1)
        if cpu > 75:
            print("CPU", cpu)
            printstat()
        time.sleep(1)

if __name__ == "__main__":

    #print(dir(psutil))
    #sys.exit(0)
    testpower()

# EOF
