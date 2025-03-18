# Implement asyncio guest mode and with sample code work with it

## Purpose

1. Make asyncio work with all GUI frameworks, sample code be implemented in tornado, pygame, tkinter, gtk, qt5, win32, pyside6
2. Make webview_python library support call async python from javascript
a. https://github.com/congzhangzh/webview_python
b. https://github.com/congzhangzh/webview_python/issues/1


## Core implement part

Design: ./design_en.md

1. guest mode implemented here: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_run.py
2. python stdlib patch here: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/patches/base_events.diff

## GUI support status

|Framework|Windows|Linux|Mac|
|---|---|---|---|
|Tkinter|✅|✅|❓|
|Win32|✅|➖|➖|
|GTK|❓|✅|❓|
|QT|✅|✅|❓|
|PySide6|✅|✅|❓|
|Pygame|✅|✅|❓|
|Tornado|✅|✅|❓|

## Sample reference
1. Tkinter: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_tkinter.py
2. Win32: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_win32.py
3. GTK: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_gtk.py
4. QT: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_qt5.py
5. PySide6: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_pyside6.py
6. Pygame: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_pygame.py
7. Tornado: https://github.com/congzhangzh/asyncio-guest/blob/master/asyncio_guest/asyncio_guest_tornado.py

## Solution inspired by:
1. https://www.electronjs.org/blog/electron-internals-node-integration
2. https://trio.readthedocs.io/en/stable/reference-lowlevel.html#using-guest-mode-to-run-trio-on-top-of-other-event-loops
3. https://github.com/sunoru/Webviews.jl/blob/main/src/platforms/windows/Impl.jl#L59

## Samples inspire by
1. https://github.com/richardsheridan/trio-guest

## Discuss with other guys
1. https://discuss.python.org/t/connecting-asyncio-and-tkinter-event-loops/14722/33
2. https://github.com/congzhangzh/webview_python/issues/1
3. https://github.com/webview/webview_deno/issues/185

## Some early attempts:
1. https://github.com/congzhangzh/python_gui_with_asyncio
2. Where all important iteration happend: https://github.com/congzhangzh/asyncio_guest_run/tree/main/v2
