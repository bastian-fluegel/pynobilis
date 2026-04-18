# core/app.py
# Copyright (c) 2026 Bastian Flügel. All rights reserved.

import AppKit
from PyObjCTools import AppHelper
from core.splash import SplashScreen
from components.window import Window

class App:
    def __init__(self, name="pyNobilis App"):
        self.name = name
        self.ns_app = AppKit.NSApplication.sharedApplication()
        self.ns_app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        self._main_window = None

    # core/app.py
    def window(self):
        from components.window import Window
        self._main_window = Window()
        return self._main_window

    def run(self, startup_callback=None):
        # 1. Splash zeigen (blockiert)
        SplashScreen.show(app_name=self.name)
        
        # 2. Startup Logik (hier wird das Fenster konfiguriert)
        if startup_callback:
            startup_callback(self)
        
        # 3. App starten
        if self._main_window:
            self._main_window.show()
            
        AppHelper.runEventLoop()

    def stop(self, sender=None):
        print("Beende Anwendung...")
        AppKit.NSApp().terminate_(None)