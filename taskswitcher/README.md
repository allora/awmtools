# Task switcher

### Description

A VIM inspired task switcher, based off of window split navigation. We are using python's [EWMH] (http://standards.freedesktop.org/wm-spec/wm-spec-latest.html) library meaning it *should* work with any compliant WM. By default VIM uses Ctrl+W+(h,j,k,l) to navigate split windows. We took that idea and ran with it. Using cardinal movements; left, down, up, and right you can **choose** which window you want to raise and focus.

The days of Alt+Tab are over. No longer will you attempt to traverse your (possibly) obscene amount of windows via an arbitrary selection of your '*last active*' window. Only to find yourself tabbing one too many times... only to restart the entire endeavor.


### Information

Each movement is determined by what is closest to your currently active window. By design, it is workspace specific (as in *requires*  workspaces -- tags do not work), and it ignores minimized windows because it *only* interacts with windows that are **visible**. You will need an alternative method for those. It will also ignore programs that aren't in the tasklist e.g. pagers, docks, bars, etc.

Task Swithcer utilizes a buffer: a pixel based measurement around the window. This makes the windows near your active window (in the direction you've chosen) appear to be closer than they are, and as if they are overlapping. For movement: it measures the distance and angle from the center, and ranks adjacent windows as a higher priority in the list of possible selections. Obviously windows that overlap are closest.

With the buffer simulating adjacent status it can select windows we perceive as closest first. Thus providing an expected selection. You can also adjust the buffer size to fit your needs. It is designed to be as versatile as possible, allowing for various sizes, positions, and overlapping windows. If you have any difficulties -- resize/move the problematic window *slightly*.

It is still in early development, and hasn't been exhaustively tested with *every* window manager. But it has been tested with awesome in both tile/float modes, openbox, fluxbox, pekwm, and echinus. And the latter two with manual/automatic tiling in addition to floating. As it stands we have eliminated many issues with layouts causing it to become 'trapped' and unable to reach a window.

There will be limitations, windows might be ever-so-slightly out of the range. Hence the buffer size setting. Maximized windows sometime cause interesting reactions, but not unexpected. Always try another direction, at first it may not make sense. But often times it does after some pondering.

**Note**: Currently, it requires a focused window. If your window manager doesn't provide auto-focusing, or you've chosen not to utilize that feature. You will **need** to use whatever your usual method of focusing a window is before initiating the taskswitcher.

* Supported window states:
  * Maximized:
  * - Horizontal: Yes.
  * - Vertical: Yes.
  * - Full: Yes.
  * Ignored: Yes.
  * Sticky: Yes.
  * Shaded: Yes.
  * Raised: Yes.
  * Lowereed: Yes.
  * Unmapped: No.
  * Minimized: No.
  * Fullscreen: No.
  * Min: Systray: No.

**Notes**: For minimized windows: if you already use a bar, that works. You can script a simple switcher with [wmctrl] (https://github.com/geekless/wmctrl). For GUI you can use [rofi] (https://github.com/DaveDavenport/rofi), it includes all workspaces though. Or for fancier GUI you can use [skippy-xd] (https://github.com/richardgv/skippy-xd).

**Failed attempts**: Does not work with swm, fvwm, dwm, or with 2bwm out of the box. Upon modifying the source code in 2bwm to disable sloppy focus it can work.

### Usage

```
taskswitcher [-l] [-d] [-u] [-r] [-v] [-h] [-b]

 -l      moves left  "h"
 -d      moves down  "j"
 -u      moves up    "k"
 -r      moves right "l"

 -v      verbose mode
 -h      shows the usage information
 -b      sets buffer size (default 20)
```

Pretty simple huh?

#### Install/Dependencies

All you need to do to set this up is clone the git into the directory of your choice. Then bind convenient keys with the method of your choice.

**Requires**: python3.5, python-ewmh

### Demo

![Demo](https://github.com/allora/awmtools/raw/dev/taskswitcher/DEMO.gif)
HTML5 [video] (http://gfycat.com/SleepyAltruisticGoose)

### Examples

**Note**: "../" indicates the location of where you cloned the repo.

#### sxhkd

```
# Directional task switcher
super + ctrl + {h,j,k,l}
    ../taskswitcher -{l,d,u,r}
```

#### xbindkeys

```
# Focus window left of current
"../taskswitcher -l"
Mod4 + Control + h

# Focus window below current
"../taskswitcher -d"
Mod4 + Control + j

# Focus window above current
"../taskswitcher -u"
Mod4 + Control + k

# Focus window right of current
"../taskswitcher -r"
Mod4 + Control + l
```

#### openbox

```
<keybind key="W-C-h">
    <action name="Execute">
        <command>../taskswitcher -l</command>
    </action>
</keybind>

<keybind key="W-C-j">
    <action name="Execute">
        <command>../taskswitcher -d</command>
    </action>
</keybind>

<keybind key="W-C-k">
    <action name="Execute">
        <command>../taskswitcher -u</command>
    </action>
</keybind>

<keybind key="W-C-l">
    <action name="Execute">
        <command>../taskswitcher -r</command>
    </action>
</keybind>
```

#### fluxbox

```
# Directional task switcher
Mod4 Control H :Exec ../taskswitcher -l
Mod4 Control J :Exec ../taskswitcher -d
Mod4 Control K :Exec ../taskswitcher -u
Mod4 Control L :Exec ../taskswitcher -r
```
