#!/usr/bin/python

import sys, getopt
from math import atan2, degrees, pi, hypot
from gi.repository import Gtk, Wnck, GdkX11, Gdk

VERSION = "0.0.1-5"

def printHelp():
    print( "taskswitcher v",VERSION )
    print( "taskswitcher help:\n\
      -h: this help\n\
      -u: select window above\n\
      -d: select window below\n\
      -l: select window to the left\n\
      -r: select window to the right\n\
      -b: buffer around active window to pick adjacent windows\n\
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

    dx = ( x2 + ( w2/2 ) ) - ( x1 + ( w1/2 ) )
    dy = ( y2 + ( h2/2 ) ) - ( y1 + ( h1/2 ) )

    rads = atan2(dy,dx)

    return degrees(rads)

def compareAngles( a1, a2, desiredAngle ):
    a1Delta = desiredAngle - a1
    a2Delta = desiredAngle - a2

    return abs( a1Delta ) <= abs( a2Delta )

def isOverlapped( sxl, sxr, syt, syb, x, y, w, h ):
    # Check top left coordinate
    isValidXT = sxl <= x and sxr >= x
    isValidYT = syt <= y and syb >= y

    #check bot right coordinates
    isValidXB = sxl <= x+w and sxr >= x+w
    isValidYB = syt <= y+h and syb >= y+h

    return ( isValidXB or isValidXT ) and ( isValidYB or isValidYT )

def isInValidDirection( direction, windowDirection, delta ):
    if direction == "UP":
        return windowDirection <= ( -90 + delta ) and windowDirection >= ( -90 - delta )

    if direction == "DOWN":
        return windowDirection <= ( 90 + delta ) and windowDirection >= ( 90 - delta )

    if direction == "RIGHT":
        return windowDirection <= ( 0 + delta ) and windowDirection >= ( 0 - delta )

    if direction == "LEFT":
        isLeft = windowDirection <= ( -180 + delta ) and windowDirection >= -180
        isLeft = isLeft or ( windowDirection >= ( 180 - delta ) and windowDirection <= 180 )
        return isLeft

def isInCardinalDirection( direction, ax, ay, aw, ah, x, y, w, h ):
    # Vertical
    if direction == "UP" or direction == "DOWN":
        isValidXL = ax <= x and ax+aw >= x
        isValidXR = ax <= x+w and ax+aw >= x+w
        return isValidXL or isValidXR
    if direction == "LEFT" or direction == "RIGHT":
        isValidYT = ay <= y and ay+ah >= y
        isValidYB = ay <= y+h and ay+ah >= y+h
        return isValidYT or isValidYB


def findWindow( direction, window_list, workspace_id, active_window, buff, verbose ):
    actx, acty, actwidth, actheight = active_window.get_geometry()
    act_abs_width = actx + actwidth
    act_abs_height = acty + actheight

    actCenterX = actx + ( actwidth / 2 )
    actCenterY = acty + ( actheight / 2 )

    dest_window = None

    valid_destinations = []

    # Do a quick filter of all windows in the desired direction
    for window in window_list:
        if window.is_skip_tasklist() == True:
            continue

        window_workspaceid = window.get_workspace().get_number()
        if window_workspaceid == workspace_id:
            if window != active_window:

                winx, winy, winwidth, winheight = window.get_geometry()
                winCenterX = winx + ( winwidth / 2 )
                winCenterY = winy + ( winheight / 2 )

                if direction == "UP":
                    if winCenterY < actCenterY:
                        valid_destinations.extend( [window] )
                elif direction == "DOWN":
                    if winCenterY > actCenterY:
                        valid_destinations.extend( [window] )
                elif direction == "RIGHT":
                    if winCenterX > actCenterX:
                        valid_destinations.extend( [window] )
                elif direction == "LEFT":
                    if winCenterX < actCenterX:
                        valid_destinations.extend( [window] )


    # Find adjacent windows
    selectXLeft = actCenterX - actwidth - buff
    selectXRight = actCenterX + actwidth + buff
    selectYTop = actCenterY - actheight - buff
    selectYBot = actCenterY + actheight + buff

    adjacent_windows = []
    nonadjacent_windows = []
    for window in valid_destinations:
        x,y,w,h = window.get_geometry()

        if isOverlapped( selectXLeft, selectXRight, selectYTop, selectYBot, x, y, w, h ):
            adjacent_windows.extend( [window] )
        else:
            nonadjacent_windows.extend( [window] )

    selectable_windows = []
    if len(adjacent_windows) > 0:
        selectable_windows.extend( adjacent_windows )
        if verbose:
            print( "There are adjacent windows!" )

    selectable_windows.extend( nonadjacent_windows )

    # Find the best window
    closestDistance = -1.0
    closestAngle = -360.0
    for window in selectable_windows:
        curDist = getDistBetweenWindows( active_window, window )
        curAngle = getAngleBetweenWindows( active_window, window )

        if verbose:
            print( "************************************************" )
            print( "Testing Window:",window.get_name() )
            print( "CurAngle:", curAngle )
            print( "ClosestAngle:", closestAngle )
            print( "CurDist:", curDist )
            print( "ClosestDist:", closestDistance )

        # Filter out windows that are too far out of angle
        if not isInValidDirection( direction, curAngle, 50 ):
            if verbose:
                print( "Angle is outside of filter" )
            continue

        # Reduce distance based on angle correctness
        x,y,w,h = window.get_geometry()
        if isInValidDirection( direction, curAngle, 5 ):
            if verbose:
                print( "Angle is in the right direction treat it 70% closer" )
            curDist = curDist * 0.3
        elif isInValidDirection( direction, curAngle, 20 ):
            if verbose:
                print( "Angle is in the right direction treat it 50% closer" )
            curDist = curDist * 0.5
        elif isInValidDirection( direction, curAngle, 30 ):
            if verbose:
                print( "Angle is in the right direction treat it 20% closer" )
            curDist = curDist * 0.8

        # Bonus reduciton if in cardinal direction
        if isInCardinalDirection( direction, actx, acty, actwidth, actheight, x, y, w, h ):
            if verbose:
                print( "Window in cardinal direction, treat it 50% closer" )
            curDist = curDist * 0.5

        # Bonus reduction if in adjacent list
        if window in adjacent_windows:
            if verbose:
                print( "Window is part of adjacent list, treat it 90% closer" )
            curDist = curDist * 0.1

        if closestDistance == -1.0:
            closestDistance = curDist
            closestAngle = curAngle
            if verbose:
                print( "Window picked:", window.get_name() )
            dest_window = window
            continue

        if closestDistance > curDist:
            #if compareAngles( curAngle, closestAngle, -90.0 ):
            closestDistance = curDist
            closestAngle = curAngle
            if verbose:
                print( "Picked:", window.get_name() )
            dest_window = window

    return dest_window


def main(argv):

    # No arg list, pass out help
    if len(argv) == 0:
        printHelp()
        sys.exit(2)

    buff = 20

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
