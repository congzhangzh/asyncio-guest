# Implement asyncio guest mode and with sample code work with it

## Purpose

1. Make asyncio work with all GUI frameworks, sample code be implemented in tornado, pygame, tkinter, gtk, qt5, win32, pyside6
2. Make webview_python library support call async python from javascript
a. https://github.com/congzhangzh/webview_python
b. https://github.com/congzhangzh/webview_python/issues/1

### Status
| Framework | Windows | Linux | Mac |
|------|---------|-------|-----|
| tornado | ✅ | ✅ |❓|
| pygame | ✅ | ✅ | ❓|
| tkinter | ✅ | ✅ | ❓|
| gtk | ❓ | ✅ | ❓|
| qt5 | ✅ | ✅ | ❓|
| win32 | ✅ | ➖ | ➖ |
| pyside6 | ✅ | ✅ | ❓|

### Design:
./design_en.md

## Solution inspire by:
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
