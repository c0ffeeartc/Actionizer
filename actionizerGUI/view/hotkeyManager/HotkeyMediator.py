from puremvc.patterns.mediator import Mediator
from view.hotkeyManager.Hotkey import Hotkey

__author__ = 'c0ffee'


class HotkeyMediator(Mediator):
        def onRegister(self):
            super(HotkeyMediator, self).onRegister()
            self.setViewComponent(Hotkey())
