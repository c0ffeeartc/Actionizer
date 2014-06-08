from PySide.QtGui import QTreeView

__author__ = 'c0ffee'


class TreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        super(TreeView, self).__init__(*args, **kwargs)
        self.setIndentation(10)
