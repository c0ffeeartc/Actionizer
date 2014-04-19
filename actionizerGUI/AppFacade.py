import Notes
from controller import StartupCommand

__author__ = 'cfe'

import puremvc.patterns.facade


class AppFacade(puremvc.patterns.facade.Facade):
    __inited = False
    __started = False

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeFacade(self):
        super(AppFacade, self).initializeFacade()
        self.__inited = True
        self.registerCommand(Notes.STARTUP_COMMAND, StartupCommand)

    def startup(self):
        if not self.__inited and not self.__started:
            self.__started = True
            self.sendNotification(Notes.STARTUP_COMMAND)
