from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QPen, QColor

class CircleButton(QGraphicsItem):
    def __init__(self, parent, x=0, y=0):
        super().__init__(parent)
        self.radius = 6
        self.hovered = False
        self.setPos(x, y)

        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def paint(self, painter, style, widget=None):
        painter.setBrush(QBrush((QColor("#FF333333"))))
        outline_color = QColor("#FF66660FF") if self.hovered else QColor("#FF000000")
        painter.setPen(QPen(outline_color, 1))
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(
            - self.radius,
            - self.radius,
            self.radius * 2,
            self.radius * 2,
        ).normalized()