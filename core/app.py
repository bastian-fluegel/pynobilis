# (c) 2024 Bastian Flügel. All rights reserved.
# core/app.py
import AppKit
from PyObjCTools import AppHelper
import sys
from core.splash import SplashScreen

class NobilisAppDelegate(AppKit.NSObject):
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True 

class App:
    def __init__(self, name="My PyNobilis App"):
        # Der Name wird hier für die gesamte App-Instanz gespeichert
        self.name = name
        
        self.ns_app = AppKit.NSApplication.sharedApplication()
        self.ns_app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        
        self.delegate = NobilisAppDelegate.alloc().init()
        self.ns_app.setDelegate_(self.delegate)
        
    def run(self, startup_callback=None):
        try:
            # Reiche den App-Namen an den Splash-Screen weiter
            SplashScreen.show(app_name=self.name)
            
            if startup_callback:
                startup_callback()
            
            AppHelper.runEventLoop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.ns_app.terminate_(None)
        sys.exit(0)