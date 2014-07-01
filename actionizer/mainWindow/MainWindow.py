from PySide import QtGui
from PySide.QtCore import Signal, QEvent, QObject

from options.OptionsVO import Options

__author__ = 'cfe'


class MainWindow(QtGui.QWidget):
    btn_play_pressed = Signal()
    btn_remove_pressed = Signal()
    btn_new_pressed = Signal()
    btn_menu_pressed = Signal()
    btn_save_pressed = Signal()
    activated = Signal()
    deactivated = Signal()

    def __init__(self, tree_view):
        super(MainWindow, self).__init__()
        self.tree = tree_view

        self.menu_btn_layout = QtGui.QHBoxLayout()
        self.main_layout = QtGui.QVBoxLayout()
        self.btn_layout = QtGui.QHBoxLayout()

        self.setWindowIcon(QtGui.QIcon(Options.assets_path + "flash_16x16.png"))
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(QtGui.QIcon(Options.assets_path + "flash_16x16.png"))
        self.tray_icon.show()

        self.setGeometry(700, 300, 400, 600)
        self.setWindowTitle('Actionizer')


        self.btn_save = QtGui.QPushButton(QtGui.QIcon(Options.assets_path + "save_16x16.png"), "")
        # noinspection PyUnresolvedReferences
        self.btn_save.clicked.connect(self.on_save_clicked)
        self.menu_btn_layout.addWidget(self.btn_save)
        self.menu_btn_layout.addStretch(2)

        self.btn_layout.addStretch(0)
        self.btn_play = QtGui.QPushButton(QtGui.QIcon(Options.assets_path + "play_16x16.png"), "")
        self.btn_layout.addWidget(self.btn_play)
        # noinspection PyUnresolvedReferences
        self.btn_play.clicked.connect(self.on_play)

        self.btn_menu = QtGui.QPushButton(QtGui.QIcon(Options.assets_path + "tune_16x16.png"), "")
        # noinspection PyUnresolvedReferences
        self.btn_menu.clicked.connect(self.on_btn_menu_clicked)
        self.menu_btn_layout.addWidget(self.btn_menu)

        self.btn_new = QtGui.QPushButton(
            QtGui.QIcon(Options.assets_path + "new_file_16x16.png"), "")
        # noinspection PyUnresolvedReferences
        self.btn_new.clicked.connect(self.on_new_btn_clicked)
        self.btn_layout.addWidget(self.btn_new)
        self.btn_remove = QtGui.QPushButton(
            QtGui.QIcon(Options.assets_path + "trash_16x16.png"), "")
        # noinspection PyUnresolvedReferences
        self.btn_remove.clicked.connect(self.on_remove_clicked)
        self.btn_layout.addWidget(self.btn_remove)

        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.menu_btn_layout)
        self.main_layout.addWidget(self.tree)
        self.main_layout.addLayout(self.btn_layout)
        self.show()

        self.installEventFilter(self)

    def on_play(self):
        self.btn_play_pressed.emit()

    def on_new_btn_clicked(self):
        self.btn_new_pressed.emit()

    def on_remove_clicked(self):
        self.btn_remove_pressed.emit()

    def on_save_clicked(self):
        self.btn_save_pressed.emit()

    def on_btn_menu_clicked(self):
        self.btn_menu_pressed.emit()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowActivate:
            self.activated.emit()
            return True
        elif event.type() == QEvent.WindowDeactivate:
            self.deactivated.emit()
            return True
        else:
            # standard event processing
            return QObject.eventFilter(self, obj, event)
