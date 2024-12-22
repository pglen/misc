#!/usr/bin/env python3

import  os, sys, getopt, signal, select, socket, time, struct
import  random, stat, os.path, datetime, threading, subprocess
import  struct, io, traceback, hashlib, traceback, argparse

try:
    import fcntl
except:
    fcntl = None

base = os.path.dirname(os.path.realpath(__file__))

'''
 String triplet per test.  Input format is array of data.

 Format of data:

   Context string  Send string  Expect string
   --------------  -----------  -------------
'''

#print("testdrive")

def strdiff(expectx, actualx):
    strx = ""
    for cnt, bb in enumerate(expectx):
        #print("cnt", cnt, bb)
        if bb != actualx[cnt]:
            strx = "At pos: %d  [%s]" % (cnt,
                            str(expectx[cnt:cnt+5]))
            break
    return strx

def xdiff(actualx, expectx, findflag):

    ''' Compare values, display string in Color
        Sensitive to find flag.
    '''

    if findflag:
        #print("Find", str(expectx), str(actualx))
        if str(expectx) in str(actualx):
            return "\033[32;1mOK\033[0m"
        else:
            return"\033[31;1mERR\033[0m"

    else:
        if expectx == actualx:
            return "\033[32;1mOK\033[0m"
        else:
            return"\033[31;1mERR\033[0m"

def obtain(cmd):

    ''' Get output from command '''

    comm = [0,]
    exec = cmd.split()
    if args.debug > 1:
        print("exec:", exec)

    try:
        ret = subprocess.Popen(exec, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        comm = ret.communicate()
    except:
        print("Cannot communicate in:", exec)
        #sys.exc_info())

    return comm[0]

def send_expect(context, sendx, expectx, findflag):

    ''' evaluate SEND -- EXPECT sequence '''

    ret = obtain(sendx)
    if args.debug > 2:
        print("\033[32;1mGot: ", ret, "\033[0m")

    err = xdiff(ret, expectx, findflag)

    # If no context, we do not want any printing
    if context:
        print(context, "\t", err)

    if args.verbose:
        # On error tell us the expected result
        if ret != expectx:
            print("\033[34;1mGot:\033[0m\n", ret)

    if args.verbose > 1:
        if ret != expectx:
            print("\033[34;1mExpected:\033[0m\n", expectx)

    if args.verbose > 2:
        if ret != expectx:
            print("\033[34;1mDiff:\033[0m\n",
                strdiff(ret, expectx))

def mainloop():

    if args.test_cases:
        for fff in args.test_cases:
            try:
                with open(fff) as fp:
                    testx = fp.read()
            except:
                print("Cannot open file", "'" + fff  + "'")
                sys.exit()

            #print("testx", testx)

            test_case = eval(testx)
            for aa in test_case:
                send_expect(aa[0], aa[1], aa[2], aa[3])

version = "1.0.0"

def mainfunct():

    global args

    parser = argparse.ArgumentParser(\
            description='Test send/expect by executing sub commands')
    parser.add_argument("-v", '--verbose', dest='verbose',
                        default=0,  action='count',
                        help='verbocity on (default: off)')
    parser.add_argument("-d", '--debug', dest='debug',
                        default=0,  type=int, action='store',
                        help='Debug level')
    parser.add_argument("test_cases", nargs= "+",
                        help = "Test cases to execute")

    args = parser.parse_args()
    #print(args)
    mainloop()

if __name__ == "__main__":
    mainfunct()

# EOF
