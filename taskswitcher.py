#!/usr/bin/python

import sys, getopt
from math import atan2, degrees, pi, hypot
from gi.repository import Gtk, Wnck, GdkX11, Gdk

VERSION = "0.0.1-3"

def printHelp():
    print( "taskswitcher v",VERSION )
    print( "taskswitcher help:\n\
      -h: this help\n\
      -u: select window above\n\
      -d: select window below\n\
      -l: select window to the left\n\
      -r: select window to the right\n\
      -v: verbose mode" )

def getDistBetweenWindows( window1, window2 ):
    x1,y1,width1,height1 = window1.get_geometry()
    x2,y2,width2,height2 = window2.get_geometry()

    x1Adjusted = x1 + ( width1/2 )
    x2Adjusted = x2 + ( width2/2 )

    y1Adjusted = y1 + ( height1/2 )
    y2Adjusted = y2 + ( height2/2 )

    dist = hypot( x2Adjusted - x1Adjusted, y2Adjusted - y1Adjusted )

    return dist

def getAngleBetweenWindows( window1, window2 ):
    x1,y1,w1,h1 = window1.get_geometry()
    x2,y2,w2,h2 = window2.get_geometry()

    dx = x2 - x1
    dy = y2 - y1

    rads = atan2(dy,dx)

    return degrees(rads)

def compareAngles( a1, a2, desiredAngle ):
    a1Delta = desiredAngle - a1
    a2Delta = desiredAngle - a2

    return abs( a1Delta ) <= abs( a2Delta )

def findWindow( direction, window_list, workspace_id, active_window, buff, verbose ):
    actx, acty, actwidth, actheight = active_window.get_geometry()
    act_abs_width = actx + actwidth
    act_abs_height = acty + actheight

    dest_window = None

    valid_destinations = []

    for window in window_list:
        if window.is_skip_tasklist() == True:
            continue

        window_workspaceid = window.get_workspace().get_number()
        if window_workspaceid == workspace_id:
            if window != active_window:

                winx, winy, winwidth, winheight = window.get_geometry()

                if direction == "UP":
                    if winy < acty - buff:
                        valid_destinations.extend( [window] )
                elif direction == "DOWN":
                    if winy > act_abs_height + buff:
                        valid_destinations.extend( [window] )
                elif direction == "RIGHT":
                    if winx > act_abs_width + buff:
                        valid_destinations.extend( [window] )
                elif direction == "LEFT":
                    if winx < actx - buff:
                        valid_destinations.extend( [window] )

    closestDistance = -1.0
    closestAngle = -360.0
    for window in valid_destinations:
        curDist = getDistBetweenWindows( active_window, window )
        curAngle = getAngleBetweenWindows( active_window, window )

        if verbose:
            print( "************************************************" )
            print( "Testing Window:",window.get_name() )
            print( "CurAngle:", curAngle )
            print( "ClosestAngle:", closestAngle )
            print( "CurDist:", curDist )
            print( "ClosestDist:", closestDistance )

        if closestDistance == -1.0:
            closestDistance = curDist
            closestAngle = curAngle
            dest_window = window
            continue

        if curDist < closestDistance:
            if direction == "UP":
                if compareAngles( curAngle, closestAngle, -90.0 ):
                    if closestDistance > curDist:
                        closestDistance = curDist
                        closestAngle = curAngle
                        dest_window = window
            if direction == "DOWN":
                if compareAngles( curAngle, closestAngle, 90.0 ):
                    closestDistance = curDist
                    closestAngle = curAngle
                    dest_window = window
            if direction == "RIGHT":
                if compareAngles( curAngle, closestAngle, 0.0 ):
                    closestDistance = curDist
                    closestAngle = curAngle
                    dest_window = window
            if direction == "LEFT":
                if compareAngles( abs( curAngle ), abs( closestAngle ), 180.0 ):
                    closestDistance = curDist
                    closestAngle = curAngle
                    dest_window = window

    return dest_window


def main(argv):

    # No arg list, pass out help
    if len(argv) == 0:
        printHelp()
        sys.exit(2)

    buff = 0

    try:
        opts, args = getopt.getopt(argv,"hudlrb:v")
    except getopt.GetoptError as err:
        printHelp()
        sys.exit(2)

    direction = ""
    verbose = False

    for opt, arg in opts:
        if opt == "-h":
            printHelp()
            sys.exit()
        elif opt == "-u":
            direction = "UP"
        elif opt == "-d":
            direction = "DOWN"
        elif opt == "-l":
            direction = "LEFT"
        elif opt == "-r":
            direction = "RIGHT"
        elif opt == "-b":
            buff = int(arg)
        elif opt == "-v":
            verbose = True

    # Grab window list and geo
    Gtk.init([])  # necessary if not using a Gtk.main() loop
    screen = Wnck.Screen.get_default()
    screen.force_update()  # recommended per Wnck documentation

    window_list = screen.get_windows()
    active_window = screen.get_active_window()

    workspace_id = screen.get_active_workspace().get_number()

    if len(window_list) > 0:
        window = findWindow( direction, window_list, workspace_id, active_window, buff, verbose )
    else:
        print( "Empty window list!" )
        sys.exit(2)

    if window != None:
        now = GdkX11.x11_get_server_time(Gdk.get_default_root_window())
        window.activate(now)

    window = None
    screen = None
    Wnck.shutdown()

if __name__ == "__main__":
    main(sys.argv[1:])
