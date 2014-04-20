from PySide import QtGui
from PySide.QtGui import QTreeWidgetItem
from Action import Action
from StepCollection import StepCollection
from StepFactory import StepFactory, StepUids

__author__ = 'cfe'


class MainWindow(QtGui.QWidget):

    main_layout = QtGui.QVBoxLayout()
    tree = None
    btn_layout = QtGui.QHBoxLayout()
    btn_quit = None
    btn_play = None
    btn_new = None
    btn_remove = None

    def __init__(self):
        super(MainWindow, self).__init__()
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        self.tree = QtGui.QTreeWidget()
        self.tree.setHeaderItem(QtGui.QTreeWidgetItem(None, ["Name"]))
        self.tree.setColumnCount(1)
        self.tree.addTopLevelItem(QTreeWidgetItem(None, ["anyName", StepUids.NULL_STEP]))
        self.tree.addTopLevelItem(QTreeWidgetItem(None, ["anyName2", StepUids.TEST_STEP]))
        # self.tree.childAt(0).setData()

        self.setGeometry(300, 300, 250, 450)
        self.setWindowTitle('Actionizer')


        self.btn_quit = QtGui.QPushButton("Quit")
        self.btn_layout.addWidget(self.btn_quit)
        self.btn_play = QtGui.QPushButton("Play")
        self.btn_layout.addWidget(self.btn_play)
        self.btn_play.clicked.connect(self.playSelectedAction)
        self.btn_new = QtGui.QPushButton("New")
        self.btn_layout.addWidget(self.btn_new)
        self.btn_remove = QtGui.QPushButton("Remove")
        self.btn_layout.addWidget(self.btn_remove)

        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.tree)
        self.main_layout.addLayout(self.btn_layout)
        self.show()

    def playSelectedAction(self):
        i = 0
        while i < self.tree.topLevelItemCount():
            step_uid = self.tree.topLevelItem(i).text(1)
            a_step = StepFactory.new_step(step_uid)  # StepUids.TEST_STEP)
            stepCol = StepCollection(a_step)
            action1 = Action()
            action1.add(stepCol)
            action1.play()
            i += 1
