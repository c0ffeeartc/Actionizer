from PySide import QtGui
from PySide.QtCore import Qt, Signal

from options.OptionsVO import Options

__author__ = 'cfe'


class MainWindow(QtGui.QWidget):
    btn_play_pressed = Signal()
    btn_remove_pressed = Signal()
    btn_new_pressed = Signal()
    btn_save_pressed = Signal()

    def __init__(self, tree_view):
        super(MainWindow, self).__init__()
        self.tree = tree_view

        self.main_layout = QtGui.QVBoxLayout()
        self.btn_layout = QtGui.QHBoxLayout()

        self.act = QtGui.QAction(self)
        self.act.setShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_L))
        self.act.setShortcutContext(Qt.ApplicationShortcut)
        self.addAction(self.act)

        self.setWindowIcon(QtGui.QIcon(Options.assets_path + "flash_16x16.png"))
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(
            QtGui.QIcon(Options.assets_path + "flash_16x16.png"))
        self.tray_icon.show()

        self.setGeometry(700, 300, 400, 600)
        self.setWindowTitle('Actionizer')

        self.btn_save = QtGui.QPushButton(
            QtGui.QIcon(Options.assets_path + "save_16x16.png"), "")
        # noinspection PyUnresolvedReferences
        self.btn_save.clicked.connect(self.on_save_clicked)
        self.btn_layout.addWidget(self.btn_save)
        self.btn_layout.addStretch(2)
        self.btn_play = QtGui.QPushButton(
            QtGui.QIcon(Options.assets_path + "play_16x16.png"), "")
        self.btn_layout.addWidget(self.btn_play)
        # noinspection PyUnresolvedReferences
        self.btn_play.clicked.connect(self.on_play)

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
        self.main_layout.addWidget(self.tree)
        self.main_layout.addLayout(self.btn_layout)
        # self.add_action_group()
        self.show()

    # todo: move handling keys to mediator
    def handle_key(self, key_event):
        if key_event.Key == "P":
            self.on_play()
        elif key_event.Key == "Q":
            pass
        elif key_event.Key == "A":
            self.act.activate(QtGui.QAction.Trigger)
        print(key_event.Key + " " + key_event.MessageName)

    def on_play(self):
        self.btn_play_pressed.emit()

    def on_new_btn_clicked(self):
        self.btn_new_pressed.emit()

    def on_remove_clicked(self):
        self.btn_remove_pressed.emit()

    def on_save_clicked(self):
        self.btn_save_pressed.emit()
