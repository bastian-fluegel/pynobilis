Hier ist die sauber formatierte Version der Dokumentation:

# pynobilis - Window Component Documentation

## Overview
The `Window` component (`components/window.py`) provides a high-level Pythonic wrapper around the native `NSWindow` class. It handles creation, styling, and coordinate management for macOS windows.

## The Coordinate System
By default, macOS (Cocoa) uses a Cartesian coordinate system where (0,0) is at the bottom-left of the screen. pynobilis "flips" this to the standard UI convention of (0,0) at the top-left.

### Desktop Positioning
To place a window at a specific top-left `y` coordinate on the desktop, pynobilis calculates the position relative to the screen height:

* **Formula**: `flipped_y = screen_height - y - window_height`

This calculation uses the dimensions of the `NSScreen.mainScreen()`.

### Internal Content Layout
Inside the window, the `ContentView` is configured to use a "flipped" coordinate system. This is achieved by:

1.  Defining a custom `FlippedView` class (subclass of `NSView`).
2.  Overriding the `isFlipped` method to return `True`.
3.  Setting this as the window's `contentView`.

This ensures that all sub-components (buttons, text, labels, etc.) added to the window are also positioned from the top-left corner.

## Usage
The `Window` constructor accepts the following parameters:

* `title`: The text displayed in the title bar.
* `x`, `y`: The top-left coordinates on the desktop.
* `width`, `height`: The dimensions of the window.

The window is automatically created with standard macOS decorations: Titled, Closable, Resizable, and Miniaturizable.

## References
1.  [components/window.py](uploaded:bastian-fluegel/pynobilis/pynobilis-a98a6d8500ba1679c3a1940b98c885026b8bf28c/components/window.py)