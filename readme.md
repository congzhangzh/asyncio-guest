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

## This project inspired by 
### ElectronJS (main: this teach me most)
1. https://www.electronjs.org/blog/electron-internals-node-integration
### V8 embed (main: JS is really ugly, but once some rich one keep use and improve it, it will be wonderful )
1. https://v8.dev/docs/embed
### Trio ( Their passion and example really help:\) ) 
1. https://trio.readthedocs.io/en/stable/reference-lowlevel.html#using-guest-mode-to-run-trio-on-top-of-other-event-loops
2. https://github.com/richardsheridan/trio-guest
### Julia WebView ( Julia's thread mode and await is really ugly? )
#### Period yield to julia schedule
1. Trigger by timer: https://github.com/sunoru/Webviews.jl/blob/b28fb63300ac68a8f1a098e53237f1af46f99133/src/platforms/windows/Impl.jl#L58
2. Trigger by timer: https://github.com/sunoru/Webviews.jl/blob/b28fb63300ac68a8f1a098e53237f1af46f99133/src/platforms/windows/Impl.jl#L59
3. Impl: https://github.com/sunoru/Webviews.jl/blob/b28fb63300ac68a8f1a098e53237f1af46f99133/src/platforms/common.jl#L16
#### Custom message loop to support peried trigger (maybe a hidden window and custom wndproc is better?)
1. https://github.com/sunoru/Webviews.jl/blob/b28fb63300ac68a8f1a098e53237f1af46f99133/src/platforms/windows/Impl.jl#L74
2. https://github.com/sunoru/Webviews.jl/blob/b28fb63300ac68a8f1a098e53237f1af46f99133/src/platforms/windows/Impl.jl#L83
### Julia Makie (Julia's thread mode and await is really ugly? )
1. https://github.com/MakieOrg/Makie.jl (after some crash of Makie, I understand how julia thread model works)
### Qt for Python (Offical, wait for many years, but still partial)
1. [qtforpython](https://doc.qt.io/qtforpython-6/PySide6/QtAsyncio/index.html)
2. https://doc.qt.io/qtforpython-6/examples/example_async_minimal.html
### Some other gusy attempts (pool based, not so good)
1. https://github.com/gmarull/asyncqt
2. https://github.com/harvimt/quamash
3. https://github.com/CabbageDevelopment/qasync

## Discuss with other guys
1. https://discuss.python.org/t/connecting-asyncio-and-tkinter-event-loops/14722/33
2. https://github.com/congzhangzh/webview_python/issues/1
3. https://github.com/webview/webview_deno/issues/185

## Some early attempts:
1. https://github.com/congzhangzh/python_gui_with_asyncio
2. Where all important iteration happend: https://github.com/congzhangzh/asyncio_guest_run/tree/main/v2

## Others fields maybe help
### Deno JavaScript runtime & Tokio & V8
1. https://github.com/denoland/deno/pull/3844
2. https://choubey.gitbook.io/internals-of-deno/threading-model/default-threads
3. https://docs.rs/tokio/latest/tokio/runtime/index.html#current-thread-runtime-behavior-at-the-time-of-writing
4. https://questions.deno.com/m/1247553728001609729
5. https://www.reddit.com/r/rust/comments/tln9nu/what_is_the_difference_between_tokio_singlethread/
