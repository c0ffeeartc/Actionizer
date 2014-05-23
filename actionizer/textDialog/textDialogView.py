from PySide.QtGui import QDialog, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QPushButton
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class TextDialog(QDialog):
    TEXT_DIALOG_OK = "TEXT_DIALOG_OK"
    TEXT_DIALOG_CANCEL = "TEXT_DIALOG_CANCEL"

    def __init__(self, *args, **kwargs):
        super(TextDialog, self).__init__(*args, **kwargs)
        self.edit_line = QLineEdit()

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

        # noinspection PyUnresolvedReferences
        self.accepted.connect(self.on_accept)
        # noinspection PyUnresolvedReferences
        self.rejected.connect(self.on_reject)

    def on_accept(self):
        Facade.getInstance().sendNotification(
            TextDialog.TEXT_DIALOG_OK,
            {"text": self.edit_line.text()},
        )
        print("accepted")

    def on_reject(self):
        Facade.getInstance().sendNotification(
            TextDialog.TEXT_DIALOG_CANCEL,
        )
