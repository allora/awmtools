#!/usr/bin/python

import sys, getopt
from gi.repository import Gtk, Wnck, GdkX11, Gdk

def printHelp():
    print( "taskswitcher help:\n\
      -h: this help\n\
      -u: select window above\n\
      -d: select window below\n\
      -l: select window to the left\n\
      -r: select window to the right\n\
      -b: enlarge the buffer space for window picking\n\
            Example: taskswitcher -b 20" )

def findWindow( direction, window_list, workspace_id, active_window, buff ):
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
                    if winy < acty:
                        print( "Adding up windows" )
                        valid_destinations.extend( [window] )
                elif direction == "DOWN":
                    if winy > act_abs_height:
                        print( "Adding down windows" )
                        valid_destinations.extend( [window] )
                elif direction == "RIGHT":
                    if winx > act_abs_width:
                        print( "Adding right windows" )
                        valid_destinations.extend( [window] )
                elif direction == "LEFT":
                    if winx < actx:
                        print( "Adding left windows" )
                        valid_destinations.extend( [window] )

    initial = True
    nearestY = -1
    nearestX = -1
    xDelta = -1
    yDelta = -1
    print( "Number of windows:", len( valid_destinations ) )
    for window in valid_destinations:
        winx, winy, winwidth, winheight = window.get_geometry()
        curYDelta = abs( ( acty ) - ( winy ) )
        curXDelta = abs( ( actx ) - ( winx ) )

        if direction == "UP":
            if initial == True:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window
                initial = False
                continue

            if curXDelta <= xDelta and curYDelta < yDelta:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window


        if direction == "DOWN":
            print( "******", window.get_name() )
            print( nearestY, winy, curYDelta, curXDelta )
            if initial == True:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window
                initial = False
                continue

            if curXDelta <= xDelta and curYDelta < yDelta:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window


        if direction == "RIGHT":
            if initial == True:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window
                initial = False
                continue

            if curYDelta <= yDelta and curXDelta > xDelta:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window

        if direction == "LEFT":
            if initial == True:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
                dest_window = window
                initial = False
                continue

            if curYDelta <= yDelta and curXDelta < xDelta:
                print( "set a window" )
                xDelta = curXDelta
                yDelta = curYDelta
                nearestY = winy
                nearestX = winx
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
