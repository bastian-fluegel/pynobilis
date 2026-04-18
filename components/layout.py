# components/layout.py
# Copyright (c) 2026 Bastian Flügel. All rights reserved.

import AppKit
from core.view import NobilisView

class Stack(NobilisView):
    def __init__(self, spacing=10, padding=0):
        super().__init__()
        self.ns_view = AppKit.NSStackView.stackViewWithViews_([])
        self.ns_view.setSpacing_(spacing)
        # Padding (EdgeInsets)
        edge = (padding, padding, padding, padding)
        self.ns_view.setEdgeInsets_(edge)

    def children(self, *args):
        for child in args:
            if hasattr(child, 'ns_view'):
                self.ns_view.addArrangedSubview_(child.ns_view)
            else:
                self.ns_view.addArrangedSubview_(child)
        return self

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