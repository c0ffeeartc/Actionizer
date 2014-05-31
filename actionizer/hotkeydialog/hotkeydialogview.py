from PySide.QtCore import Qt, QEvent
from PySide.QtGui import QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QKeySequence
from puremvc.patterns.facade import Facade

__author__ = 'c0ffee'


class HotkeyDialogView(QDialog):
    HOTKEY_DIALOG_OK = "HOTKEY_DIALOG_OK"
    HOTKEY_DIALOG_CANCEL = "HOTKEY_DIALOG_CANCEL"

    def __init__(self, *args, **kwargs):
        super(HotkeyDialogView, self).__init__(*args, **kwargs)
        self.setWindowTitle("Set Hotkey")
        self.edit_line = QLineEdit()
        self.edit_line.setEnabled(False)
        self.installEventFilter(self)

        self.ok_btn = QPushButton("&Ok")
        # noinspection PyUnresolvedReferences
        self.ok_btn.clicked.connect(self.accept)

        self.control_check = QCheckBox()
        self.control_label = QLabel("CTRL")
        self.shift_check = QCheckBox()
        self.shift_label = QLabel("SHIFT")
        self.alt_check = QCheckBox()
        self.alt_label = QLabel("ALT")

        self.cancel_btn = QPushButton("&Cancel")
        # noinspection PyUnresolvedReferences
        self.cancel_btn.clicked.connect(self.reject)

        self.h_keys_layout = QHBoxLayout()
        self.h_btn_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h_btn_layout.addStretch(0)
        self.h_btn_layout.addWidget(self.ok_btn)
        self.h_btn_layout.addWidget(self.cancel_btn)

        self.h_keys_layout.addWidget(self.control_check)
        self.h_keys_layout.addWidget(self.control_label)
        self.h_keys_layout.addWidget(self.shift_check)
        self.h_keys_layout.addWidget(self.shift_label)
        self.h_keys_layout.addWidget(self.alt_check)
        self.h_keys_layout.addWidget(self.alt_label)
        self.h_keys_layout.addWidget(self.edit_line)
        self.v_layout.addLayout(self.h_keys_layout)
        self.v_layout.addLayout(self.h_btn_layout)
        self.setLayout(self.v_layout)

    def eventFilter(self, source, event):
        """
        @type event: QEvent.QEvent
        @return:
        """
        if event.type() == QEvent.KeyPress:
            event = event
            """:type :QKeyEvent"""
            key_seq = QKeySequence(event.key())
            self.edit_line.setText(key_seq.toString())
            return True
        return QDialog.eventFilter(self, source, event)


    def on_accept(self):
        Facade.getInstance().sendNotification(
            HotkeyDialogView.HOTKEY_DIALOG_OK,
        )

    def on_reject(self):
        Facade.getInstance().sendNotification(
            HotkeyDialogView.HOTKEY_DIALOG_CANCEL,
        )
