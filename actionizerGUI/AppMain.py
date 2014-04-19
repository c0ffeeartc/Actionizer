from AppFacade import AppFacade

__author__ = 'cfe'


class AppMain():
    def __init__(self):
        pass

    @staticmethod
    def main():
        facade = AppFacade.getInstance()
        facade.startup()

if __name__ == "__main__":
    AppMain.main()
