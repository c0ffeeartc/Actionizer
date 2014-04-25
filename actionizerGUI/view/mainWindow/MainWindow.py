from PySide import QtGui, QtCore
from PySide.QtCore import Qt, QEventLoop
from PySide.QtGui import QTreeWidgetItem

from Action import Action
import Notes
from StepCollection import StepCollection
from StepFactory import StepFactory, StepUids
from puremvc.patterns.facade import Facade


__author__ = 'cfe'


class UI(object):
    ACTION = "ACTION"
    ACTION_GROUP = "ACTION_GROUP"
    STEP = "STEP"


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
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        self.act = QtGui.QAction(self)
        self.act.setShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_L))
        self.act.setShortcutContext(Qt.ApplicationShortcut)
        self.act.triggered.connect(self.add_clicked)
        self.addAction(self.act)

        self.tree = QtGui.QTreeWidget()
        self.tree.setHeaderItem(QtGui.QTreeWidgetItem(None, ["Name", "TYPE_NAME"]))
        self.tree.setColumnCount(3)

        self.setGeometry(300, 300, 250, 450)
        self.setWindowTitle('Actionizer')

        self.btn_layout.addStretch(1)
        self.btn_play = QtGui.QPushButton(QtGui.QIcon("../assets/play_16x16.png"), "")
        self.btn_layout.addWidget(self.btn_play)
        self.btn_play.clicked.connect(self.play_selected_action)
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
            self.play_selected_action()
        elif (key_event.Key == "Q"):
            self.disable_global_hotkeys()
        elif (key_event.Key == "A"):
            self.act.activate(QtGui.QAction.Trigger)
        print(key_event.Key + " " + key_event.MessageName)

    def disable_global_hotkeys(self):
        Facade.getInstance().sendNotification(Notes.STOP_LISTEN_GLOBAL_HOTKEYS)

    def enable_global_hotkeys(self):
        Facade.getInstance().sendNotification(Notes.START_LISTEN_GLOBAL_HOTKEYS)

    def play_selected_action(self):
        print("playing")
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.STEP:
            step_uid = cur_item.text(2)
            a_step = StepFactory.new_step(step_uid)  # StepUids.TEST_STEP)
            step_col = StepCollection(a_step)
            action1 = Action()
            action1.add(step_col)
            action1.play()

    def add_clicked(self):
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION:
            self.add_step_to_action()
        elif cur_item.text(1) == UI.ACTION_GROUP:
            self.add_action_to_group()

    def add_action_to_group(self):
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION_GROUP:
            cur_item.setExpanded(True)
            new_action = QTreeWidgetItem(None, ["New Action", UI.ACTION])
            cur_item.addChild(new_action)

    def add_step_to_action(self):
        cur_item = self.tree.currentItem()
        if cur_item.text(1) == UI.ACTION:
            cur_item.setExpanded(True)
            test_step = QTreeWidgetItem(None, ["anyName2", UI.STEP, StepUids.TEST_STEP])
            cur_item.addChild(test_step)

    def remove_selected(self):
        cur_item = self.tree.currentItem()
        cur_item_type = cur_item.text(1)
        if cur_item_type == UI.ACTION or cur_item_type == UI.STEP:
            cur_item.parent().removeChild(cur_item)

    def add_action_group(self):
        action_group = QTreeWidgetItem(self.tree, ["ActionGroup", UI.ACTION_GROUP])
        self.tree.addTopLevelItem(action_group)
        action_group.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        action_group.setIcon(0, QtGui.QIcon("../assets/folder_16x16.png"))
