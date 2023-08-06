from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QStylePainter, QStyleOptionButton

class ButtonItem(QStyledItemDelegate):
    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)

        style_painter = QStylePainter(self.parent())

        style_painter.drawItemText(option.rect, Qt.AlignLeft, option.palette, True, index.data())

        # Get the button rect
        button_option = QStyleOptionButton()

        button_option.text = "+"
        button_option.rect = self.get_button_rect(option)
        button_option.state = QStyle.State_Enabled

        # Draw the button using the QStylePainter object
        style_painter.drawControl(QStyle.CE_PushButton, button_option)

    def get_button_rect(self, option):
        # Calculate the button rect based on the option rect
        button_rect = QRect(option.rect)
        button_rect.setLeft(button_rect.right() - 20)
        button_rect.setTop(button_rect.top() + (button_rect.height() - 20) // 2)
        button_rect.setSize(QSize(20, 20))
        return button_rect