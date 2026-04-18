# (c) 2026 Bastian Flügel. All rights reserved.
# components/window.py

import AppKit
import objc
from core.base import NobilisBase

# Delegate für das "X" (Traffic Light)
class NobilisWindowDelegate(AppKit.NSObject):
    def windowShouldClose_(self, window):
        if hasattr(self, "_py_window") and self._py_window._close_callback:
            self._py_window._close_callback()
            return False
        return True

class Window(NobilisBase):
    def __init__(self):
        super().__init__()
        
        # 1. Grund-Setup mit Standardwerten
        rect = AppKit.NSMakeRect(0, 0, 800, 600)
        style = (AppKit.NSWindowStyleMaskTitled | 
                 AppKit.NSWindowStyleMaskClosable | 
                 AppKit.NSWindowStyleMaskResizable |
                 AppKit.NSWindowStyleMaskMiniaturizable)
        
        self.ns_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, style, AppKit.NSBackingStoreBuffered, False
        )
        
        # Standard-Verhalten
        self.ns_window.center()
        self.ns_window.setOpaque_(False)
        self.ns_window.setBackgroundColor_(AppKit.NSColor.clearColor())
        
        # Close-Logic
        self._close_callback = lambda: AppKit.NSApp().terminate_(None)
        self._delegate = NobilisWindowDelegate.alloc().init()
        self._delegate._py_window = self
        self.ns_window.setDelegate_(self._delegate)
        
        self._noble_level = None
        self._noble_intensity = 1.0

    # --- Die neuen Chainable-Methoden ---

    def title(self, text):
        """Setzt den Fenstertitel."""
        self.ns_window.setTitle_(text)
        return self

    def size(self, width, height):
        """Setzt die Fenstergröße."""
        self.ns_window.setContentSize_((width, height))
        return self

    def on_close(self, func):
        """Eigene Logik für das rote X."""
        self._close_callback = func
        return self

    def make_noble(self, level="subtle", intensity=1.0):
        """Aktiviert den Frosted-Glass-Look."""
        self._noble_level = level
        self._noble_intensity = max(float(intensity), 1.0)
        return self

    def content(self, root_view):
        """Der rote Faden: Hier wird der Inhalt eingefügt."""
        container = AppKit.NSView.alloc().init()
        container.setWantsLayer_(True)
        self.ns_window.setContentView_(container)
        
        if self._noble_level:
            # Modernes Design (Inhalt unter Titlebar)
            self.ns_window.setTitlebarAppearsTransparent_(True)
            self.ns_window.setStyleMask_(self.ns_window.styleMask() | AppKit.NSWindowStyleMaskFullSizeContentView)
            self.ns_window.setTitleVisibility_(AppKit.NSWindowTitleHidden)
            
            # Blur-Layer (VEV)
            vev = AppKit.NSVisualEffectView.alloc().initWithFrame_(container.bounds())
            vev.setAutoresizingMask_(AppKit.NSViewWidthSizable | AppKit.NSViewHeightSizable)
            
            materials = {
                "subtle": AppKit.NSVisualEffectMaterialSidebar,
                "medium": AppKit.NSVisualEffectMaterialUnderWindowBackground,
                "heavy": AppKit.NSVisualEffectMaterialHUDWindow
            }
            
            vev.setMaterial_(materials.get(self._noble_level, 20))
            vev.setBlendingMode_(AppKit.NSVisualEffectBlendingModeBehindWindow)
            vev.setState_(AppKit.NSVisualEffectStateActive)
            vev.setAlphaValue_(1.0) # Echter Blur braucht 1.0
            container.addSubview_(vev)

            # Optionale Tönung für bessere Lesbarkeit
            if self._noble_intensity > 1.0:
                tint = AppKit.NSView.alloc().initWithFrame_(container.bounds())
                tint.setWantsLayer_(True)
                tint.setAutoresizingMask_(AppKit.NSViewWidthSizable | AppKit.NSViewHeightSizable)
                extra_opacity = (self._noble_intensity - 1.0) * 0.15
                tint.layer().setBackgroundColor_(AppKit.NSColor.colorWithWhite_alpha_(0.1, extra_opacity).CGColor())
                container.addSubview_(tint)

        # User UI einbetten
        user_ui = root_view.ns_view
        user_ui.setFrame_(container.bounds())
        user_ui.setAutoresizingMask_(AppKit.NSViewWidthSizable | AppKit.NSViewHeightSizable)
        container.addSubview_(user_ui)
        
        # Wasserzeichen stempeln
        self._add_watermark(container)
        return self

    def _add_watermark(self, container):
        if not getattr(self, "_is_licensed", False):
            label = AppKit.NSTextField.labelWithString_("unregistered version of pyNobilis\nplease contact your developer")
            label.setFont_(AppKit.NSFont.systemFontOfSize_(10))
            label.setTextColor_(AppKit.NSColor.secondaryLabelColor())
            label.setAlphaValue_(0.4)
            label.setTranslatesAutoresizingMaskIntoConstraints_(False)
            container.addSubview_(label)
            AppKit.NSLayoutConstraint.activateConstraints_([
                label.trailingAnchor().constraintEqualToAnchor_constant_(container.trailingAnchor(), -20.0),
                label.bottomAnchor().constraintEqualToAnchor_constant_(container.bottomAnchor(), -20.0)
            ])

    def show(self):
        self.ns_window.makeKeyAndOrderFront_(None)
        AppKit.NSApp().activateIgnoringOtherApps_(True)
        return self