from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

class BlueprintPropertiesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_UI()

    def init_UI(self):
        layout = QHBoxLayout(self)
        button = QPushButton("Add Class", self)
        layout.addWidget(button)
        self.setLayout(layout)