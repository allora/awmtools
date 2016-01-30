#!/usr/bin/python

import sys, getopt
from ewmh import EWMH

ewmh = EWMH()
VERSION = "0.0.1-3"

def printHelp():
    print( "Help stuff!" )

def main(argv):

    # No arg list, pass out help and quit
    if len(argv) == 0:
        printHelp()
        sys.exit(2)

    try:
        opts, args = getopt.getopt( argv,"ax:y:v" )
    except getopt.GetoptError as err:
        printHelp()
        sys.exit(2)

    absolute = False
    verbose = False
    xpos = 0
    ypos = 0

    for opt, arg in opts:
        if opt == "-a":
            absolute = True
        elif opt == "-h":
            printHelp()
            sys.exit()
        elif opt == "-x":
            xpos = int(arg)
        elif opt == "-y":
            ypos = int(arg)
        elif opt == "-v":
            verbose = True

    # Grab active window
    ewmh.display.flush()
    window = ewmh.getActiveWindow()

    active_window = window
    while active_window.query_tree().parent != ewmh.root:
        active_window = active_window.query_tree().parent

    wininfo = active_window.get_geometry()

    if verbose == True:
        print( "Window Info: X:", wininfo.x, "Y:", wininfo.y, "W:", wininfo.width, "H:", wininfo.height )

    newx = 0
    newy = 0

    if absolute == True:
        newx = xpos
        newy = ypos
    else:
        newx = wininfo.x + xpos
        newy = wininfo.y + ypos

    if verbose == True:
        print( "Calculated X:", newx )
        print( "Calculated Y:", newy )

    #moveMask = Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y
    if newx < 0:
        newx = 0
    if newy < 0:
        newy = 0

    if verbose == True:
        print( "Old X:", wininfo.x, "New X:", newx )
        print( "Old Y:", wininfo.y, "New Y:", newy )

    ewmh.setMoveResizeWindow(active_window, 0, newx, newy, wininfo.width, wininfo.height)
    #active_window.set_geometry( Wnck.WindowGravity.NORTHWEST, moveMask, newx, newy, width, height )
    ewmh.display.flush()

if __name__ == "__main__":
    main(sys.argv[1:])
