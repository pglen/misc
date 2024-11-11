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
        #print(dir(aa))
        #print("name", aa.name)
        if aa.name() == "bash":
            #print(dir(aa))
            #print("lead:", aa.name(), aa.pid, aa.ppid(), aa.terminal())
            for bb in psutil.process_iter():
                #if aa.terminal() and aa.terminal() == bb.terminal():
                if aa.pid == bb.ppid():
                    #print(" sub:", bb.name(), bb.pid, bb.cmdline(), bb.name(), bb.terminal())
                    if bb.pid not in subids:
                        #print(dir(bb))
                        #print("tmie", bb.create_time())
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

    argparser.add_argument('argx', nargs='*', help="Arguments", default=["Test Alert",])

    argparser.add_argument('-v', '--verbose', action="count", default=0,
                                                help='Show operational details.')

    argparser.add_argument('-n', '--nosound', action="store_true",
                                                help='Switch off sound alerts.')

    argparser.add_argument('-f', '--filesound', action="store",
                        help='File name for sound. Default is "complete.oga"')

    argparser.add_argument('-o', '--timeout', action="store", type=int, default=10,
                        help='Notification window timeout in seconds. Zero for no timeout'
                                'Default is 10 sec.')

    argparser.add_argument('-l', '--tminlen', action="store", type=int, default=30,
                        help='Time the program must be running (in seconds) for notify to kick in. '
                        'Default is 30 sec.')

    argparser.add_argument('-e', '--title', action="store", default="Done Program",
                        help='Title line of the notification field. Default: "Done Program"'
                        'Default is 30 sec.')

    argparser.add_argument('-t', '--testalert', action="store_true",
                                                help='Test notifier.')

    argparser.add_argument('-s', '--testsound', action="store_true",
                                                help='Test sound.')

    return argparser

if __name__ == "__main__":

    argparser = config_args()
    args = argparser.parse_args()
    if args.verbose > 2:
        print (args)

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

    while True:
        mainloop()
        time.sleep(2)

# EOF
