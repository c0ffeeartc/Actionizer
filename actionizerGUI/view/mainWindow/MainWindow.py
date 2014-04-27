from PySide import QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidgetItem, QCursor

from Action import Action
import Notes
from StepFactory import StepUids
from model.UI import UI
from model.stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade
from view.actionTree.ActionTree import ActionTree

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

    def __init__(self):
        super(MainWindow, self).__init__()

        self.act = QtGui.QAction(self)
        self.act.setShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_L))
        self.act.setShortcutContext(Qt.ApplicationShortcut)
        self.act.triggered.connect(self.print_step_files)
        self.addAction(self.act)

        self.tree = ActionTree()

        self.setWindowIcon(QtGui.QIcon("../assets/flash_16x16.png"))
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(QtGui.QIcon("../assets/flash_16x16.png"))
        self.tray_icon.show()

        self.setGeometry(300, 300, 250, 450)
        self.setWindowTitle('Actionizer')

        self.btn_layout.addStretch(1)
        self.btn_play = QtGui.QPushButton(QtGui.QIcon("../assets/play_16x16.png"), "")
        self.btn_layout.addWidget(self.btn_play)
        self.btn_play.clicked.connect(self.play_action)
        self.btn_new = QtGui.QPushButton(QtGui.QIcon("../assets/new_file_16x16.png"), "")
        self.btn_new.clicked.connect(self.add_clicked)
        self.btn_layout.addWidget(self.btn_new)
        self.btn_remove = QtGui.QPushButton(QtGui.QIcon("../assets/trash_16x16.png"), "")
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_layout.addWidget(self.btn_remove)

        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.tree)
        self.main_layout.addLayout(self.btn_layout)
        self.add_action_group()
        self.show()

    def handle_key(self, key_event):
        if (key_event.Key == "P"):
            self.play_action()
        elif (key_event.Key == "Q"):
            self.disable_global_hotkeys()
        elif (key_event.Key == "A"):
            self.act.activate(QtGui.QAction.Trigger)
        print(key_event.Key + " " + key_event.MessageName)

    def disable_global_hotkeys(self):
        Facade.getInstance().sendNotification(Notes.STOP_LISTEN_GLOBAL_HOTKEYS)

    def enable_global_hotkeys(self):
        Facade.getInstance().sendNotification(Notes.START_LISTEN_GLOBAL_HOTKEYS)

    def print_step_files(self):
        print(Facade.getInstance().retrieveProxy(StepPoolProxy.NAME).data.step_files)

    def play_action(self, start_index=0):
        print("playing")
        step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
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
                action.add(step_pool_proxy.get_step(step_uid))
            action.play(start_index)

    def add_clicked(self):
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION or cur_item.text(1) == UI.STEP:
            self.add_step()
        elif cur_item.text(1) == UI.ACTION_GROUP:
            self.add_action_to_group()

    def add_action_to_group(self):
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION_GROUP:
            cur_item.setExpanded(True)
            new_action = QTreeWidgetItem(None, ["New Action", UI.ACTION])
            cur_item.addChild(new_action)

    def add_step(self, step_uid=StepUids.NULL_STEP, parent=None, index=0):
        step_item = QTreeWidgetItem(None, ["Step", UI.STEP, step_uid])
        if parent:
            if parent.text(1) != UI.ACTION:
                print("Can't add step to not action")
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

    def remove_selected(self):
        cur_item = self.tree.currentItem()
        cur_item_type = cur_item.text(1)
        if cur_item_type == UI.ACTION or cur_item_type == UI.STEP:
            cur_item.parent().removeChild(cur_item)

    def add_action_group(self):
        action_group = QTreeWidgetItem(self.tree, ["ActionGroup", UI.ACTION_GROUP])
        self.tree.invisibleRootItem().addChild(action_group)
        action_group.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        action_group.setIcon(0, QtGui.QIcon("../assets/folder_16x16.png"))
