# (c) 2024 Bastian Flügel. All rights reserved.
# components/window.py
import AppKit
from Foundation import NSMakeRect

class Window:
    def __init__(self, 
        title="<window title>", 
        posX=100, 
        posY=100, 
        width=800, 
        height=600):
        
        # 1. Bildschirmsystem umrechnen (Top-Left Fix)
        screen_frame = AppKit.NSScreen.mainScreen().frame()
        screen_height = screen_frame.size.height
        
        # Cocoa y = Bildschirmhöhe - gewünschtes y - Fensterhöhe
        flipped_y = screen_height - posY - height
        
        rect = NSMakeRect(posX, flipped_y, width, height)
        
        style_mask = (
            AppKit.NSTitledWindowMask |
            AppKit.NSClosableWindowMask |
            AppKit.NSResizableWindowMask |
            AppKit.NSMiniaturizableWindowMask
        )
        
        self.ns_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect,
            style_mask,
            AppKit.NSBackingStoreBuffered,
            False
        )
        
        self.ns_window.setTitle_(title)
        
        # 2. Inhalts-Koordinatensystem umdrehen
        self._setup_flipped_content_view()
        
        self.ns_window.makeKeyAndOrderFront_(None)

    def _setup_flipped_content_view(self):
        """Setzt eine View als Content-View, die isFlipped=True zurückgibt."""
        class FlippedView(AppKit.NSView):
            def isFlipped(self):
                return True
        
        content_view = FlippedView.alloc().init()
        self.ns_window.setContentView_(content_view)