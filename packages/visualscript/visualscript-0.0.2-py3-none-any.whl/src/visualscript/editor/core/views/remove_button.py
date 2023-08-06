from editor.core.views.circle_button import CircleButton
from PyQt5.QtGui import QPen, QColor

class RemoveButton(CircleButton):
    def paint(self, painter, style, widget=None):
        super().paint(painter, style, widget)
        painter.setPen(QPen(QColor("#FFFFFFFF"), 2))
        painter.drawLine(-self.radius//2, 0, self.radius//2, 0)
