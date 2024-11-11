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


def testio():
    #print("IO select")
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    #print(old)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO
    new[3] = new[3] & ~termios.ICANON
    termios.tcsetattr(fd, termios.TCSANOW, new)
    old2 = termios.tcgetattr(fd)

    while True:
        ttt = time.time()
        #tty.setraw(sys.stdin, termios.TCSANOW,)
        termios.tcsetattr(fd, termios.TCSANOW, new)
        ret = select.select([sys.stdin,], [], [], .2)
        #print("ret:", ret)
        lag = time.time() - ttt
        if lag > .3:
            termios.tcsetattr(fd, termios.TCSANOW, old)
            dd = datetime.datetime.now()
            ddd = dd.strftime("%Y/%m/%d %H:%M:%S")
            print("Input lag at: %6s lag = %.3f" % (ddd, lag))
            printstat()

        #print("ttt %.3f" % )
        if ret[0]:
            chh = sys.stdin.read(1)
            if not chh:
                break
            print("read:", chh)
        #time.sleep(1)

if __name__ == "__main__":

    testio()

# EOF
