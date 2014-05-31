from PySide.QtGui import QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
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

        self.ok_btn = QPushButton("&Ok")
        # noinspection PyUnresolvedReferences
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)

        self.cancel_btn = QPushButton("&Cancel")
        # noinspection PyUnresolvedReferences
        self.cancel_btn.clicked.connect(self.reject)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h_layout.addStretch(0)
        self.h_layout.addWidget(self.ok_btn)
        self.h_layout.addWidget(self.cancel_btn)

        self.v_layout.addWidget(self.edit_line)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def on_accept(self):
        Facade.getInstance().sendNotification(
            HotkeyDialogView.HOTKEY_DIALOG_OK,
        )

    def on_reject(self):
        Facade.getInstance().sendNotification(
            HotkeyDialogView.HOTKEY_DIALOG_CANCEL,
        )
