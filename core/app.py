# (c) 2024 Bastian Flügel. All rights reserved.
# core/app.py
import AppKit
from PyObjCTools import AppHelper
import sys

class NobilisAppDelegate(AppKit.NSObject):
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True # Dies ist der magische Schalter

class App:
    def __init__(self):
        self.ns_app = AppKit.NSApplication.sharedApplication()
        self.ns_app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        
        # Den Delegate setzen
        self.delegate = NobilisAppDelegate.alloc().init()
        self.ns_app.setDelegate_(self.delegate)
        
    def run(self):
        try:
            AppHelper.runEventLoop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("\nAdmin-Präsenz wird deaktiviert. System-Shutdown...")
        self.ns_app.terminate_(None)
        sys.exit(0)