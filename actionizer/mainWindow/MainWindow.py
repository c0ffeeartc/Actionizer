from PySide import QtGui

from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidgetItem

from actionTree.model.UI import UI
from mainWindow.NewTreeElementCommand import NewTreeElementCommand
from options.OptionsVO import Options
from actionTree.model.Action import Action
from notifications.notes import Notes
from puremvc.patterns.facade import Facade
from stepPool.model.StepFactory import StepUids


__author__ = 'cfe'


class MainWindow(QtGui.QWidget):
    main_layout = QtGui.QVBoxLayout()
    tree = None
    btn_layout = QtGui.QHBoxLayout()
    btn_play = None
    btn_new = None
    btn_remove = None
    play_hotkey = None
    timer = None
    act = None

    def __init__(self, treeView):
        super(MainWindow, self).__init__()

        self.act = QtGui.QAction(self)
        self.act.setShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_L))
        self.act.setShortcutContext(Qt.ApplicationShortcut)
        self.addAction(self.act)

        self.tree = treeView

        self.setWindowIcon(QtGui.QIcon(Options.assets_path + "flash_16x16.png"))
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(
            QtGui.QIcon(Options.assets_path + "flash_16x16.png"))
        self.tray_icon.show()

        self.setGeometry(700, 300, 400, 600)
        self.setWindowTitle('Actionizer')

        self.btn_save = QtGui.QPushButton(
            QtGui.QIcon(Options.assets_path + "play_16x16.png"), "")
        # noinspection PyUnresolvedReferences
        self.btn_save.clicked.connect(self.on_save_clicked)
        self.btn_layout.addWidget(self.btn_save)
        self.btn_layout.addStretch(2)
        self.btn_play = QtGui.QPushButton(
            QtGui.QIcon(Options.assets_path + "play_16x16.png"), "")
        self.btn_layout.addWidget(self.btn_play)
        # noinspection PyUnresolvedReferences
        self.btn_play.clicked.connect(self.play_action)
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
        self.add_action_group()
        self.show()

    def on_save_clicked(self):
        Facade.getInstance().sendNotification(Notes.TREE_MODEL_SAVE)

    def handle_key(self, key_event):
        if key_event.Key == "P":
            self.play_action()
        elif key_event.Key == "Q":
            self.disable_global_hotkeys()
        elif key_event.Key == "A":
            self.act.activate(QtGui.QAction.Trigger)
        print(key_event.Key + " " + key_event.MessageName)

    def disable_global_hotkeys(self):
        Facade.getInstance().sendNotification(Notes.STOP_LISTEN_GLOBAL_HOTKEYS)

    def enable_global_hotkeys(self):
        Facade.getInstance().sendNotification(Notes.START_LISTEN_GLOBAL_HOTKEYS)

    def play_action(self, start_index=0):
        print("playing")
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION or cur_item.text(1) == UI.STEP:
            gui_action = None
            if cur_item.text(1) == UI.ACTION:
                gui_action = cur_item
            elif cur_item.text(1) == UI.STEP:
                gui_action = cur_item.parent()
                start_index = cur_item.parent().indexOfChild(cur_item)
            action = Action()
            for i in xrange(gui_action.childCount()):
                step_uid = gui_action.child(i).text(2)
                # actionTree.play(start_index)

    def on_new_btn_clicked(self):
        Facade.getInstance().sendNotification(
            NewTreeElementCommand.NAME,
            {"child": None, "indexes": None},
        )

    def on_remove_clicked(self):
        Facade.getInstance().sendNotification(Notes.TREE_MODEL_REMOVE)

    def add_action_to_group(self):
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION_GROUP:
            cur_item.setExpanded(True)
            new_action = QTreeWidgetItem(None, ["New Action", UI.ACTION])
            cur_item.addChild(new_action)

    def add_step(self, step_uid=StepUids.NULL_STEP, parent=None, index=0):
        """
        :type parent:QTreeWidgetItem
        """
        step_item = QTreeWidgetItem(None, ["Step", UI.STEP, step_uid])
        if parent:
            if parent.text(1) != UI.ACTION:
                print("Can't add step to not actionTree")
                return
            print("index == " + str(index))
            parent.insertChild(index, step_item)
        else:
            cur_item = self.tree.currentItem()
            parent = cur_item.parent()
            if cur_item.text(1) == UI.ACTION:
                cur_item.setExpanded(True)
                cur_item.insertChild(0, step_item)
            if cur_item.text(1) == UI.STEP:
                cur_index = parent.indexOfChild(cur_item)
                cur_item.parent().insertChild(cur_index + 1, step_item)

    def add_action_group(self):
        action_group = QTreeWidgetItem(self.tree,
                                       ["ActionGroup", UI.ACTION_GROUP])
        self.tree.invisibleRootItem().addChild(action_group)
        action_group.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        action_group.setIcon(0, QtGui.QIcon(
            Options.assets_path + "folder_16x16.png"))
