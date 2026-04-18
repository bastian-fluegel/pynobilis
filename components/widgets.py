# components/widgets.py
import AppKit
from core.view import NobilisView

class Label(NobilisView):
    def __init__(self, text=""):
        super().__init__()
        self.ns_view = AppKit.NSTextField.labelWithString_(text)
        
    def font(self, size=13, weight="regular"):
        if weight == "bold":
            font = AppKit.NSFont.boldSystemFontOfSize_(size)
        else:
            font = AppKit.NSFont.systemFontOfSize_(size)
        self.ns_view.setFont_(font)
        return self

    def color(self, value):
        if not self.ns_view: return self
        
        # 1. Check auf semantische System-Farben
        system_colors = {
            "primary": AppKit.NSColor.labelColor(),          # Schwarz in Light, Weiß in Dark
            "secondary": AppKit.NSColor.secondaryLabelColor(), # Grau-Töne
            "tertiary": AppKit.NSColor.tertiaryLabelColor(),
            "white": AppKit.NSColor.whiteColor(),
            "black": AppKit.NSColor.blackColor()
        }
        
        if value in system_colors:
            self.ns_view.setTextColor_(system_colors[value])
        elif value.startswith("#"):
            # Hier könnte später dein Hex-Parser stehen
            # Für jetzt erzwingen wir Weiß nur, wenn der User es wirklich will
            pass 
            
        return self

class Button(NobilisView):
    def __init__(self, title="Button"):
        super().__init__()
        self.ns_view = AppKit.NSButton.buttonWithTitle_target_action_(
            title, None, None
        )
        self.ns_view.setBezelStyle_(AppKit.NSBezelStyleRounded)
        self._callback = None

    def action(self, func):
        self._callback = func
        self.ns_view.setTarget_(self)
        self.ns_view.setAction_(b"handleAction:")
        return self

    def handleAction_(self, sender):
        if self._callback:
            self._callback()

    def primary(self):
        self.ns_view.setKeyEquivalent_("\r") # Enter-Taste aktiviert diesen Button
        return self