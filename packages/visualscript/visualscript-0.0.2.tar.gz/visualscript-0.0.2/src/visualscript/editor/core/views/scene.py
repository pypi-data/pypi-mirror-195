import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QLine, pyqtSignal
from PyQt5.QtGui import QColor, QPen

class SceneView(QGraphicsScene):

    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.model = model

        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")
        self._color_very_dark = QColor("#232323")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)
        self._pen_bold = QPen(self._color_very_dark)
        self._pen_bold.setWidth(5)

        self.setBackgroundBrush(self._color_background)

    def dragMoveEvent(self, event):
        pass

    def setgraphics(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        lines_light, lines_dark, lines_bold = [], [], []
        for x in range(first_left, right, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            elif x != 0:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_bold.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(left, y, right, y))
            elif y != 0:
                lines_dark.append(QLine(left, y, right, y))
            else:
                lines_bold.append(QLine(left, y, right, y))

        if len(lines_light):
            painter.setPen(self._pen_light)
            painter.drawLines(*lines_light)

        if len(lines_dark):
            painter.setPen(self._pen_dark)
            painter.drawLines(*lines_dark)

        if len(lines_bold):
            painter.setPen(self._pen_bold)
            painter.drawLines(*lines_bold)