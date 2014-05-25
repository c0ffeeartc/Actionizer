from PySide.QtGui import QDialog, QComboBox, QPushButton, QHBoxLayout, \
    QVBoxLayout
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class ComboDialog(QDialog):
    COMBO_DIALOG_OK = "COMBO_DIALOG_OK"
    COMBO_DIALOG_CANCEL = "COMBO_DIALOG_CANCEL"

    def __init__(self, *args, **kwargs):
        super(ComboDialog, self).__init__(*args, **kwargs)

        self.combo_box = QComboBox()

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

        self.v_layout.addWidget(self.combo_box)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

        # noinspection PyUnresolvedReferences
        self.accepted.connect(self.on_accept)
        # noinspection PyUnresolvedReferences
        self.rejected.connect(self.on_reject)

    def on_accept(self):
        Facade.getInstance().sendNotification(
            ComboDialog.COMBO_DIALOG_OK,
        )

    def on_reject(self):
        Facade.getInstance().sendNotification(
            ComboDialog.COMBO_DIALOG_CANCEL,
        )
