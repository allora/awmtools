#!/usr/bin/python

import sys, getopt
from gi.repository import Gtk, Wnck

VERSION = "0.0.1-1"

def printHelp():
    print( "Help stuff!" )

def main(argv):

    # No arg list, pass out help and quit
    if len(argv) == 0:
        printHelp()
        sys.exit(2)

    try:
        opts, args = getopt.getopt( argv,"ax:y:" )
    except getopt.GetoptError as err:
        printHelp()
        sys.exit(2)

    absolute = False
    xpos = 0.0
    ypos = 0.0

    for opt, arg in opts:
        if opt == "-a":
            absolute = True
        elif opt == "-h":
            printHelp()
            sys.exit()
        elif opt == "-x":
            xpos = float(arg)
        elif opt == "-y":
            ypos = float(arg)

    # Grab window list
    Gtk.init([])
    screen = Wnck.Screen.get_default()
    screen.force_update()

    active_window = screen.get_active_window()

    x,y,width,height = active_window.get_geometry()

    if absolute == True:
        newx = xpos
        newy = ypos
    else:
        newx = x+xpos
        newy = y+ypos
    
    moveMask = Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y 
    active_window.set_geometry( 0, moveMask, newx, newy, width, height )

if __name__ == "__main__":
    main(sys.argv[1:])
