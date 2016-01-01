# AWMtools

The beginnings of a new collection of window manager tools. A valiant effort to create cross-platform-style utilities that 'just work' with **both** *tiling* window managers and *floating* window managers. The goal being to make every thing as straight forward as possible. Working towards closing the gap that other tools leave behind.

We all know 'em, like 'em, and use 'em. Why not make more? There's always something you would like to be able to do but are otherwise limited by your window manager. Our aim is to deescalate the hostage situation that is DEs/WMs and us. Basic window managing shouldn't be left up to the user to script/write into their WM.

Proper window management *should* be provided by the window manager. Since it is often not -- at least not to the extent that we would like -- we are attempting to simplify and satisfy those requirements.

As of right now, we don't know what the future holds for us. We are contemplating writing a window manager. But starting with necessary utilities we are currently missing, or improving upon ones that didn't quite work out. So keep an eye out for future releases, but don't expect us to pump them out.

### Tools

* Task Switcher
* Window Mover

### Progress

* **Task Switcher**
  - [x] Select windows based on what humans perceive as closest
  - [x] Alter the way it selects to account for overlap
  - [x] Fix return routes selecting the same windows
  - [x] Set variables to deal with each window state
  - [ ] Correct more 'dead zones' in overlapping switching
  - [ ] Correct 'trapped' windows in certain tile layouts
  - [ ] Speed up performance


* **Window Mover**
  - [x] Make relative movements work despite window manager
  - [x] Solve drifting with each movement by decoration height
  - [ ] Correct misalignments due to window decorations
  - [ ] Speed up performance
