# components/layout.py
# Copyright (c) 2026 Bastian Flügel. All rights reserved.

import AppKit
from core.view import NobilisView

class Stack(NobilisView):
    def __init__(self, spacing=10, padding=0):
        super().__init__()
        self.ns_view = AppKit.NSStackView.stackViewWithViews_([])
        self.ns_view.setSpacing_(spacing)
        self.ns_view.setEdgeInsets_((padding, padding, padding, padding))

    def content(self, *args):
        """Der einheitliche Weg, Elemente hinzuzufügen."""
        for child in args:
            # Falls der User eine Liste oder ein Tupel übergibt
            if isinstance(child, (list, tuple)):
                for item in child:
                    self._add_single_child(item)
            else:
                self._add_single_child(child)
        return self

    def _add_single_child(self, child):
        view = child.ns_view if hasattr(child, 'ns_view') else child
        self.ns_view.addArrangedSubview_(view)

class VStack(Stack):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ns_view.setOrientation_(1) # 1 = Vertical
        self.ns_view.setAlignment_(1)    # 1 = CenterX

class HStack(Stack):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ns_view.setOrientation_(0) # 0 = Horizontal
        self.ns_view.setAlignment_(3)    # 3 = CenterY

class Spacer(NobilisView):
    def __init__(self):
        super().__init__()
        # Ein Spacer ist eine leere View, die sich maximal ausdehnt
        self.ns_view = AppKit.NSView.alloc().init()
        # Hugging Priority auf 1 setzen (sehr niedrig), damit er wächst
        self.ns_view.setContentHuggingPriority_forOrientation_(1, 0)
        self.ns_view.setContentHuggingPriority_forOrientation_(1, 1)

# components/layout.py (Erweiterung)

class Box(NobilisView):
    def __init__(self, padding=0):
        super().__init__()
        # Die Box ist eine leere Basis-View
        self.ns_view = AppKit.NSView.alloc().init()
        self.ns_view.setWantsLayer_(True) # Ermöglicht Farben & Ecken
        
        # Interner Stack für das Layout in der Box
        self._layout = AppKit.NSStackView.stackViewWithViews_([])
        self._layout.setEdgeInsets_((padding, padding, padding, padding))
        self.ns_view.addSubview_(self._layout)
        
        # Constraints: Der Stack füllt die Box immer aus
        self._layout.setTranslatesAutoresizingMaskIntoConstraints_(False)
        AppKit.NSLayoutConstraint.activateConstraints_([
            self._layout.leadingAnchor().constraintEqualToAnchor_(self.ns_view.leadingAnchor()),
            self._layout.trailingAnchor().constraintEqualToAnchor_(self.ns_view.trailingAnchor()),
            self._layout.topAnchor().constraintEqualToAnchor_(self.ns_view.topAnchor()),
            self._layout.bottomAnchor().constraintEqualToAnchor_(self.ns_view.bottomAnchor()),
        ])

    def background(self, color_value, alpha=1.0):
        """Unterstützt 'black', 'white' und HEX-Codes wie '#123456'."""
        if color_value.startswith("#"):
            # HEX zu NSColor Konvertierung
            hex_str = color_value.lstrip('#')
            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0
            color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, alpha)
        elif color_value == "black":
            color = AppKit.NSColor.blackColor().colorWithAlphaComponent_(alpha)
        else:
            color = AppKit.NSColor.whiteColor().colorWithAlphaComponent_(alpha)
            
        self.ns_view.layer().setBackgroundColor_(color.CGColor())
        return self

    def corner_radius(self, radius):
        """Rundet die Ecken der Box ab."""
        self.ns_view.layer().setCornerRadius_(radius)
        return self

    def content(self, *args):
        """Fügt Elemente in die Box ein (Roter Faden!)."""
        for child in args:
            view = child.ns_view if hasattr(child, 'ns_view') else child
            self._layout.addArrangedSubview_(view)
        return self