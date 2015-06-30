#!/usr/bin/python

import sys, getopt, math
from gi.repository import Gtk, Wnck, GdkX11, Gdk

VERSION = "0.0.1-1"

def printHelp():
    print( "taskswitcher v",VERSION )
    print( "taskswitcher help:\n\
      -h: this help\n\
      -u: select window above\n\
      -d: select window below\n\
      -l: select window to the left\n\
      -r: select window to the right\n\
      -b: enlarge the buffer space for window picking\n\
            Example: taskswitcher -b 20" )

def getDistBetweenWindows( window1, window2 ):
    x1,y1,width1,height1 = window1.get_geometry()
    x2,y2,width2,height2 = window2.get_geometry()

    x1Adjusted = x1 + ( width1/2 )
    x2Adjusted = x2 + ( width2/2 )

    y1Adjusted = y1 + ( height1/2 )
    y2Adjusted = y2 + ( height2/2 )

    dist = math.hypot( x2Adjusted - x1Adjusted, y2Adjusted - y1Adjusted )

    return dist

def findWindow( direction, window_list, workspace_id, active_window, buff ):
    actx, acty, actwidth, actheight = active_window.get_geometry()
    act_abs_width = actx + actwidth
    act_abs_height = acty + actheight

    adjustedActX = actx + ( actwidth/2 )
    adjustedActY = acty + ( actheight/2 )

    dest_window = None

    valid_destinations = []

    for window in window_list:
        if window.is_skip_tasklist() == True:
            continue

        window_workspaceid = window.get_workspace().get_number()
        if window_workspaceid == workspace_id:
            if window != active_window:

                winx, winy, winwidth, winheight = window.get_geometry()

                adjustedWinX = winx + ( winwidth/2 )
                adjustedWinY = winy + ( winheight/2 )

                if direction == "UP":
                    if adjustedWinY < adjustedActY - buff:
                        valid_destinations.extend( [window] )
                elif direction == "DOWN":
                    if adjustedWinY > ( act_abs_height/2 ) + buff:
                        valid_destinations.extend( [window] )
                elif direction == "RIGHT":
                    if adjustedWinX > ( act_abs_width/2 ) + buff:
                        valid_destinations.extend( [window] )
                elif direction == "LEFT":
                    if adjustedWinX < adjustedActX - buff:
                        valid_destinations.extend( [window] )

    closestDistance = -1.0
    for window in valid_destinations:
        curDist = getDistBetweenWindows( window, active_window )

        if closestDistance == -1.0:
            closestDistance = curDist
            dest_window = window
            continue

        if curDist < closestDistance:
            closestDistance = curDist
            dest_window = window

    return dest_window


def main(argv):

    # No arg list, pass out help
    if len(argv) == 0:
        printHelp()
        sys.exit(2)

    buff = 10

    try:
        opts, args = getopt.getopt(argv,"hudlrb:")
    except getopt.GetoptError as err:
        printHelp()
        sys.exit(2)

    direction = ""

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

    # Grab window list and geo
    Gtk.init([])  # necessary if not using a Gtk.main() loop
    screen = Wnck.Screen.get_default()
    screen.force_update()  # recommended per Wnck documentation

    window_list = screen.get_windows()
    active_window = screen.get_active_window()

    workspace_id = screen.get_active_workspace().get_number()

    if len(window_list) > 0:
        window = findWindow( direction, window_list, workspace_id, active_window, buff )
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
