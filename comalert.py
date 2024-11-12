#!/usr/bin/env python

import os, sys, psutil, time, datetime, threading, argparse

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
except:
    print("No notify subsystem")

try:
    from playsound import playsound
except:
    pass
    def playsound(arg):
        print("Fake playsound")
        Gdk.beep()
        pass
    #print("No sound subsystem")

VERSION = "1.0.0"

def _asynsound():
    #print("Thread start")
    Gdk.beep()

    if args.filesound:
        playsound(args.filesound)
    else:
        playsound("/usr/share/sounds/freedesktop/stereo/complete.oga")
    #print("Thread end")

def play_sound():
    ttt = threading.Thread(None, _asynsound)
    ttt.start()

subids = []
subnames = []
sublines = []
subtimes = []

def _callback_func():
    pass
    print("Acknowledged")

def notify(alsub):

    try:
        Notify.init("Alert")
    except:
        print("Notify subsystem is not installed")
        return
    sss = alsub
    nnn = Notify.Notification.new(args.title, sss, "dialog-information")
    #nnn.add_action("action_click", "Acknowledge Alarm", _callback_func, None)
    nnn.set_timeout(args.timeout * 1000)
    nnn.show()

def mainloop():

    ''' Loop forever '''

    sumx = ""
    for aa in psutil.process_iter():
        #print("name", aa.name)
        if aa.name() == args.bshell:
            #print(dir(aa))
            if args.verbose > 3:
                print("lead:", aa.name(), aa.pid, aa.ppid(), aa.terminal())
            for bb in psutil.process_iter():
                #if aa.terminal() and aa.terminal() == bb.terminal():
                if aa.pid == bb.ppid():
                    #print(" sub:", bb.name(), bb.pid, bb.cmdline(), bb.name(), bb.terminal())
                    # Vanished, alert if appropriate
                    if bb.pid not in subids:
                        #print("create tme", bb.create_time())
                        subids.append(bb.pid)
                        subnames.append(bb.name())
                        sublines.append(bb.cmdline())
                        subtimes.append(bb.create_time())

    # See if it is still there
    testone()

def testone():
    subs  = []
    for cc in psutil.process_iter():
        subs.append(cc.pid)
    for cnt, dd in enumerate(subids):
        if dd in subs:
            continue

        if args.verbose:
            print("Terminated:", subids[cnt], sublines[cnt])

        tdiff = time.time() - subtimes[cnt]
        if tdiff < args.tminlen:
            if args.verbose > 1:
                print("Terminated before allocated time, no alert. "
                        "%.2f sec vs. %.2f sec" % (tdiff, args.tminlen))
        else:
            strx = ""
            for ee in sublines[cnt]:
                strx += ee + " "
            notify("%s\n%s" % (time.asctime(), strx) )
            if not args.nosound:
                play_sound()

        # Remove this process from alerts lists
        del subids[cnt]
        del subnames[cnt]
        del sublines[cnt]
        del subtimes[cnt]

def config_args():

    argparser = argparse.ArgumentParser(
        description="Monitor programs terminating in (bash) shell. Notify and play sound.")

    argparser.add_argument('argx', nargs='*', default=["Test Alert",],
                        help="Arguments, context dependent")

    argparser.add_argument('-v', '--verbose', action="count", default=0,
                        help='Show operational details. Add more -v for more details.')

    argparser.add_argument('-n', '--nosound', action="store_true",
                        help='Switch off sound alerts.')

    argparser.add_argument('-V', '--version', action="store_true",
                        help='Show version number.')

    argparser.add_argument('-f', '--filesound', action="store",
                        help='File name for sound. Default is "complete.oga"')

    argparser.add_argument('-o', '--timeout', action="store", type=int, default=10,
                        help='Notification window timeout in seconds. Zero for no timeout. '
                                'Default is 10 sec.')

    argparser.add_argument('-l', '--tminlen', action="store", type=int, default=30,
                        help='Time the program must be running (in seconds) for notify to kick in. '
                        'Default is 30 sec.')

    argparser.add_argument('-e', '--title', action="store", default="Done Program",
                        help='Title line of the notification field. Default: "Done Program" ' )

    argparser.add_argument('-b', '--bshell', action="store", default="bash",
                        help='Shell program to monitor. Default: "bash" ' )

    argparser.add_argument('-t', '--testalert', action="store_true",
                        help='Test notifier. Command line args are used as notification.')

    argparser.add_argument('-s', '--testsound', action="store_true",
                        help='Test sound.')

    argparser.add_argument('-p', '--sleep', action="store",  type=float, default=1.0,
                        help='Time between loop evalusations in seconds. Default: 1 sec.')

    return argparser

if __name__ == "__main__":

    argparser = config_args()
    args = argparser.parse_args()
    if args.verbose > 2:
        print (args)

    if args.version:
        print("Version: %s" % VERSION)
        sys.exit(0)

    if args.testalert:
        notify(" ".join(args.argx))
        sys.exit(0)

    if args.testsound:
        notify("Test sound and alert.")
        play_sound()
        sys.exit(0)

    if args.filesound:
        if not os.path.isfile(args.filesound):
            print("Sound file must exist.")
            playsound("/usr/share/sounds/freedesktop/stereo/complete.oga")
            sys.exit()

    # Contain value
    if args.sleep  < 0.1:
        args.sleep = 0.1

    maincnt = 0
    while True:
        maincnt += 1
        if args.verbose > 4:
            print("Evaluating mainloop:", maincnt)
        mainloop()
        time.sleep(args.sleep)

# EOF
