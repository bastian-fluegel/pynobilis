# (c) 2026 Bastian Flügel. All rights reserved.
# components/window.py
import AppKit
from core.base import NobilisBase

class Window(NobilisBase):
    def __init__(self, title, width, height):
        super().__init__()
        # 1. Natives Fenster erstellen
        rect = AppKit.NSMakeRect(0, 0, width, height)
        style = (AppKit.NSWindowStyleMaskTitled | 
                 AppKit.NSWindowStyleMaskClosable | 
                 AppKit.NSWindowStyleMaskResizable |
                 AppKit.NSWindowStyleMaskMiniaturizable)
        
        self.ns_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, style, AppKit.NSBackingStoreBuffered, False
        )
        self.ns_window.setTitle_(title)
        self.ns_window.center()
        
    # In components/window.py innerhalb von _create_watermark

    def _create_watermark(self):
        text = "unregistered version of pyNobilis\nplease contact your developer"
        
        label = AppKit.NSTextField.alloc().init()
        label.setStringValue_(text)
        label.setEditable_(False)
        label.setSelectable_(False)
        label.setDrawsBackground_(False)
        label.setBordered_(False)
        
        # HIER DIE KORREKTUR:
        # Wir müssen das 'cell()' Objekt ansprechen
        label.cell().setWraps_(True) 
        
        # Styling
        label.setFont_(AppKit.NSFont.systemFontOfSize_(10))
        label.setTextColor_(AppKit.NSColor.secondaryLabelColor())
        label.setAlignment_(AppKit.NSRightTextAlignment)
        label.setAlphaValue_(0.6)
        
        return label

    def content(self, root_view):
        """Setzt das Haupt-Layout UND stempelt das Wasserzeichen oben drauf."""
        
        # A. User Inhalt setzen (dein VStack/Stack)
        # Wir setzen es direkt als contentView, da pynobilis auf NSStackView basiert.
        self.ns_window.setContentView_(root_view.ns_view)
        
        # B. Lizenz-Check (Platzhalter aus core/base.py)
        if hasattr(NobilisBase, '_is_licensed') and NobilisBase._is_licensed:
             # Wenn lizenziert, nichts tun
             return self
        
        # C. Wasserzeichen "oben drauf stempeln"
        watermark = self._create_watermark()
        
        # 1. WICHTIG: Übersetzungs-Automatik für Resizing-Masken ausschalten.
        # Sonst funktionieren die Auto-Layout-Constraints nicht.
        watermark.setTranslatesAutoresizingMaskIntoConstraints_(False)
        
        # 2. Wir fügen es als Subview in die gerade gesetzte ContentView hinzu.
        # Da es nach dem User-Inhalt hinzugefügt wird, liegt es Z-technisch oben.
        content_view = self.ns_window.contentView()
        content_view.addSubview_(watermark)
        
        # 3. Positionierung per Auto-Layout (Constraints)
        # Wir pinnen es an die untere rechte Ecke mit 10px Abstand.
        AppKit.NSLayoutConstraint.activateConstraints_([
            watermark.trailingAnchor().constraintEqualToAnchor_constant_(content_view.trailingAnchor(), -10.0),
            watermark.bottomAnchor().constraintEqualToAnchor_constant_(content_view.bottomAnchor(), -10.0)
        ])

        return self

    def show(self):
        self.ns_window.makeKeyAndOrderFront_(None)
        AppKit.NSApp().activateIgnoringOtherApps_(True)
        return self