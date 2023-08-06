import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QVBoxLayout, QTextEdit

class ContextMenu(QMenu):
    def __init__(self, parent=None, content=None):
        super().__init__(parent)
        self.content = content
        self.init_UI()

    def init_UI(self):
        self.setMinimumSize(200, 250)
        layout = QVBoxLayout(self)
        self.search_bar = QTextEdit(self)
        self.search_bar.setMinimumWidth(125)
        self.search_bar.setMaximumHeight(25)
        self.search_bar.textChanged.connect(self.filter_tree)
        layout.addWidget(self.search_bar)
        if self.content:
            layout.addWidget(self.content)
        self.setLayout(layout)


    def filter_tree(self):
        pattern = re.compile(f'.*{self.search_bar.toPlainText()}.*', re.IGNORECASE)
        for index in range(self.content.topLevelItemCount()):
            item = self.content.topLevelItem(index)
            self.check_items(item, pattern)

    def check_items(self, parent, pattern):
        can_be_hidden = True
        for index in range(parent.childCount()):
            child = parent.child(index)
            if self.check_items(child, pattern):
                can_be_hidden = False
        if pattern.search(parent.text(0)) and (parent.flags() & Qt.ItemIsDragEnabled):
            can_be_hidden = False
        parent.setHidden(can_be_hidden)
        parent.setExpanded(pattern.pattern != '.*.*')
        return not can_be_hidden
