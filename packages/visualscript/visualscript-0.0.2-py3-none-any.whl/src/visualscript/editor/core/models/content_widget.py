from collections import OrderedDict
from editor.core.models.serializable import Serializable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class NodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        layout = QVBoxLayout()
        self.layout.addLayout(layout)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignRight | Qt.AlignHCenter)
        self.layout.addLayout(layout)

    def setEditingFlag(self, value):
        self.node.model.getView().editingFlag = value

    def serialize(self):
        return OrderedDict([
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        return True