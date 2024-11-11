#!/usr/bin/env python

import sys, select, time, datetime, termios, tty, psutil

#print(dir(termios))
#sys.exit(0)

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
            if  ppp > 2:
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

def testprint():

    fp = open("test.txt", "wt")

    while True:
        ttt = time.time()
        print("ret:" * 1000, file=fp)
        lag = (time.time() - ttt) * 1000
        #print("lag %.3f" % (lag))
        if lag > .05:
            print("lag %.3f" % (lag))
            printstat()
        fp.seek(0)
        time.sleep(1)
    fp.close()

if __name__ == "__main__":

    testprint()

# EOF
