from main.StartupCommand import StartupCommand
from notifications.notes import Notes

__author__ = 'cfe'

import puremvc.patterns.facade


class AppFacade(puremvc.patterns.facade.Facade):
    __started = False
    __instance = None

    # noinspection PyMethodOverriding
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = AppFacade()
        return cls.__instance

    def initializeFacade(self):
        super(AppFacade, self).initializeFacade()
        self.registerCommand(Notes.STARTUP_COMMAND, StartupCommand)

    def startup(self):
        if not self.__started:
            self.__started = True
            self.sendNotification(Notes.STARTUP_COMMAND)
