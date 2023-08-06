import types
import typing

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF
from editor.core.models.data_types import EXEC, HANDLE
from editor.core.views.function_libraries.socket_function_library import TriangleSocketGraphics, CircleSocketGraphics, SquareSocketGraphics

class SocketGraphics(QGraphicsItem):
    custom_socket_tooltips = {0: 'exec', 1: 'any', 2: 'function'}

    def __init__(self, model):
        self.model = model
        super().__init__(model.node.graphics)

        self.hovered = False
        self.radius = 6
        self.default_padding = 10
        self.outline_width = 3
        self.setAcceptHoverEvents(True)

        self.setToolTip()

    def setToolTip(self, _=None):
        super().setToolTip(self.type_to_string(self.model.data_type))

    def type_to_string(self, data_type):
        if typing.get_origin(data_type) == typing.Union or typing.get_origin(data_type) == types.UnionType:
            result = ''
            for arg in typing.get_args(data_type):
                result += self.type_to_string(arg) + '\n'
            result = result.strip()
        elif typing.get_origin(data_type) == tuple:
            result = '('
            for arg in typing.get_args(data_type):
                result += self.type_to_string(arg) + ', '
            result = result.strip(', ') + ')'
        elif isinstance(data_type, int) and self.custom_socket_tooltips.__contains__(data_type):
            result = self.custom_socket_tooltips[data_type]
        else:
            result = str(data_type)
            if result.startswith("<class '"):
                result = result[len("<class '"):-len("'>")]
            elif result.startswith('typing.'):
                result = result[len('typing.'):]
        return result

    def getSocketPosition(self):
        return [self.pos().x() + self.model.node.graphics.pos().x(),
                self.pos().y() + self.model.node.graphics.pos().y()]

    def update_pos_x(self, x, refresh_edges=False):
        self.setPos(x, self.pos().y())
        if refresh_edges:
            for edge in self.model.edges:
                edge.graphics.updatePositions()

    def update_pos_y(self, y, refresh_edges=False):
        if self.model.index == 0 and self.model.content:
            y += self.radius

        if self.model.index != 0:
            y += self.default_padding

        gridSize = self.model.scene.graphics.gridSize

        if y % gridSize:
            y += gridSize - y % gridSize

        self.setPos(self.pos().x(), y)

        if refresh_edges:
            for edge in self.model.edges:
                edge.graphics.updatePositions()

    def update_pos(self, x, y):
        self.update_pos_x(x)
        self.update_pos_y(y)
        for edge in self.model.edges:
            edge.graphics.updatePositions()
        return self.pos()

    def get_height(self):
        if self.model.content:
            content_height = self.model.content.graphics.shape[1]
            return max(self.radius * 2, content_height)
        return self.radius * 2

    def get_width(self):
        width = self.radius * 2 + self.default_padding
        if self.model.content:
            width += self.model.content.graphics.shape[0]
        return width

    def get_socket_shape(self):
        if self.model.data_type == EXEC:
            return TriangleSocketGraphics
        elif self.model.data_type == HANDLE:
            return SquareSocketGraphics
        else:
            return CircleSocketGraphics

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        shape = self.get_socket_shape()
        shape(self.model, painter, self.radius, self.outline_width)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        ).normalized()

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()