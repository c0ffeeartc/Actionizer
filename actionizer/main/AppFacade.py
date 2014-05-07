from main import StartupCommand
from notifications import Notes

__author__ = 'cfe'

import puremvc.patterns.facade


class AppFacade(puremvc.patterns.facade.Facade):
    __started = False

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeFacade(self):
        super(AppFacade, self).initializeFacade()
        self.registerCommand(Notes.STARTUP_COMMAND, StartupCommand)

    def startup(self):
        if not self.__started:
            self.__started = True
            self.sendNotification(Notes.STARTUP_COMMAND)
