from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsTextItem

class TitleTextItem(QGraphicsTextItem):
    UnfocusSignal = pyqtSignal()
    KeyPressSignal = pyqtSignal()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.clearFocus()
            return
        super().keyPressEvent(event)
        self.KeyPressSignal.emit()

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        self.UnfocusSignal.emit()