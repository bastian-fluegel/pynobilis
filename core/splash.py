# (c) 2024 Bastian Flügel. All rights reserved.
# core/splash.py
import AppKit
import objc
from Foundation import NSDate, NSObject, NSMutableAttributedString
from core.base import NobilisBase

class SplashDelegate(NSObject):
    def init(self):
        self = objc.super(SplashDelegate, self).init()
        if self:
            self.is_done = False
        return self

    @objc.python_method
    def wait_until_done(self):
        """Verarbeitet Events, damit Buttons klickbar bleiben."""
        while not self.is_done:
            event = AppKit.NSApp().nextEventMatchingMask_untilDate_inMode_dequeue_(
                AppKit.NSAnyEventMask,
                NSDate.dateWithTimeIntervalSinceNow_(0.1),
                AppKit.NSDefaultRunLoopMode,
                True
            )
            if event:
                AppKit.NSApp().sendEvent_(event)

    def onOkClick_(self, sender):
        self.is_done = True

    def onQuitClick_(self, sender):
        AppKit.NSApp().terminate_(None)

class SplashScreen:
    @staticmethod
    def show(app_name="Untitled App"):
        if NobilisBase._is_licensed:
            return

        # 1. Fenster-Setup (Höhe auf 320 erhöht für besseres Spacing)
        win_w, win_h = 460, 320
        rect = AppKit.NSMakeRect(0, 0, win_w, win_h)
        
        style = AppKit.NSWindowStyleMaskTitled | AppKit.NSWindowStyleMaskFullSizeContentView
        banner = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, style, AppKit.NSBackingStoreBuffered, False
        )
        
        banner.setTitle_("")
        banner.setTitlebarAppearsTransparent_(True)
        banner.setBackgroundColor_(AppKit.NSColor.blackColor())
        banner.center()
        banner.setHasShadow_(True)
        
        # 2. Typografie & Farben
        para = AppKit.NSMutableParagraphStyle.alloc().init()
        para.setAlignment_(AppKit.NSTextAlignmentCenter)
        full_text = NSMutableAttributedString.alloc().init()

        # App Name (Groß, Weiß, Fokus)
        attr_app = {
            AppKit.NSFontAttributeName: AppKit.NSFont.boldSystemFontOfSize_(32.0),
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.whiteColor(),
            AppKit.NSParagraphStyleAttributeName: para
        }
        full_text.appendAttributedString_(NSMutableAttributedString.alloc().initWithString_attributes_(f"{app_name}\n\n", attr_app))

        # "created with" (Dezent)
        attr_small = {
            AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(14.0),
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.lightGrayColor(),
            AppKit.NSParagraphStyleAttributeName: para
        }
        full_text.appendAttributedString_(NSMutableAttributedString.alloc().initWithString_attributes_("created with\n", attr_small))

        # "pyNobilis" (Branding)
        attr_pynobilis = {
            AppKit.NSFontAttributeName: AppKit.NSFont.boldSystemFontOfSize_(28.0),
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.whiteColor(),
            AppKit.NSParagraphStyleAttributeName: para
        }
        full_text.appendAttributedString_(NSMutableAttributedString.alloc().initWithString_attributes_("pyNobilis", attr_pynobilis))

        # Copyright (Lesbarer gemacht)
        attr_copy = {
            AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(11.0),
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.grayColor(),
            AppKit.NSParagraphStyleAttributeName: para
        }
        full_text.appendAttributedString_(NSMutableAttributedString.alloc().initWithString_attributes_("\n\n© 2026 Bastian Flügel", attr_copy))

        # Version (Etwas größer für Lesbarkeit)
        attr_version = {
            AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(10.0),
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.darkGrayColor(),
            AppKit.NSParagraphStyleAttributeName: para
        }
        full_text.appendAttributedString_(NSMutableAttributedString.alloc().initWithString_attributes_("\nversion 0.1 alpha", attr_version))

        # 3. Label Positionierung
        label = AppKit.NSTextField.labelWithAttributedString_(full_text)
        # y-Position auf 80 erhöht, Höhe auf 200 angepasst
        label.setFrame_(AppKit.NSMakeRect(20, 80, win_w - 40, 210))
        banner.contentView().addSubview_(label)

        # 4. Buttons & Delegate
        delegate = SplashDelegate.alloc().init()
        
        # Start App Button (Tiefer gesetzt auf y=20)
        btn = AppKit.NSButton.alloc().initWithFrame_(
            AppKit.NSMakeRect((win_w - 140) / 2, 20, 140, 32)
        )
        btn.setTitle_("Start App")
        btn.setBezelStyle_(AppKit.NSBezelStyleRounded)
        btn.setKeyEquivalent_("\r") # Enter-Taste
        btn.setTarget_(delegate)
        btn.setAction_("onOkClick:")
        banner.contentView().addSubview_(btn)

        # 'x' Button oben rechts
        close_btn = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(win_w - 35, win_h - 35, 25, 25))
        close_title = NSMutableAttributedString.alloc().initWithString_attributes_("✕", {
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.darkGrayColor(),
            AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(16.0)
        })
        close_btn.setAttributedTitle_(close_title)
        close_btn.setBordered_(False)
        close_btn.setTarget_(delegate)
        close_btn.setAction_("onQuitClick:")
        banner.contentView().addSubview_(close_btn)
        
        # 5. Anzeigen & Fokus
        banner.makeKeyAndOrderFront_(None)
        AppKit.NSApp().activateIgnoringOtherApps_(True)

        # Terminal Log
        print(f"\n[PyNobilis] Launching Environment for: {app_name}")
        print("Copyright © 2026, Bastian Flügel | Version 0.1 alpha\n")

        delegate.wait_until_done()
        banner.close()