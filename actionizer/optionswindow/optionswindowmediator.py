from notifications.notes import Notes
from optionswindow.view.optionswindow import OptionsWindow
from puremvc.patterns.mediator import Mediator

__author__ = 'c0ffee'


class OptionsWindowMediator(Mediator):
    NAME = "OptionsWindowMediator"

    def __init__(self):
        super(OptionsWindowMediator, self).__init__(OptionsWindowMediator.NAME, OptionsWindow())

    def listNotificationInterests(self):
        return [
            Notes.SHOW_OPTIONS_WINDOW
        ]

    def handleNotification(self, note):
        """
        :type note: Notification
        """
        if note.name == Notes.SHOW_OPTIONS_WINDOW:
            print(Notes.SHOW_OPTIONS_WINDOW)
