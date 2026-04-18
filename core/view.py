# core/view.py
# Copyright (c) 2026 Bastian Flügel. All rights reserved.

import AppKit

class NobilisView:
    def __init__(self):
        self.ns_view = None

    def width(self, w):
        if self.ns_view:
            f = self.ns_view.frame()
            f.size.width = w
            self.ns_view.setFrame_(f)
        return self

    def height(self, h):
        if self.ns_view:
            f = self.ns_view.frame()
            f.size.height = h
            self.ns_view.setFrame_(f)
        return self

    def opacity(self, alpha):
        if self.ns_view:
            self.ns_view.setAlphaValue_(alpha)
        return self

    def hidden(self, is_hidden=True):
        if self.ns_view:
            self.ns_view.setHidden_(is_hidden)
        return self