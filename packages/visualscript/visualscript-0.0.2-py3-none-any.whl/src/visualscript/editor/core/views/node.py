from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QColor, QPen, QBrush, QFont, QPainterPath, QLinearGradient
from editor.core.views.title_text_item import TitleTextItem


class NodeGraphics(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.model = node

        self.hovered = False
        self._was_moved = False
        self._last_selected_state = False
        self.title_item = None
        self.title_background_color = self.model.color
        self.title_shadow_color = "FF191919"
        self.background_color = "#FF212121"
        self.last_pos = QPoint()

        # sizes
        self.width = 150
        self.max_width = -1
        self.height = 500
        self.corner_roundness = 10
        self.socket_padding = 8
        self.title_height = 20
        self.title_horizontal_padding = 0
        self.title_vertical_padding = 10

        # assets
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title = QBrush(QColor(self.title_background_color))
        self._brush_background = QBrush(QColor(self.background_color))

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.update_title()
        self.setToolTip(self.model.__doc__)

    def on_selected(self):
        self.model.scene.getView().itemSelected.emit()

    def mousePressEvent(self, event):
        for item in self.model.scene.items:
            if isinstance(item.graphics, NodeGraphics) and item.graphics.isSelected():
                item.graphics.last_pos = event.scenePos() - item.graphics.pos()
        super().mousePressEvent(event)

    def setPos(self, pos):
        super().setPos(pos.x() - pos.x() % self.model.scene.graphics.gridSize,
                       pos.y() - pos.y() % self.model.scene.graphics.gridSize)
        sockets = self.model.inputs + self.model.outputs
        if self.model.handle:
            sockets.append(self.model.handle)
        for socket in sockets:
            for edge in socket.edges:
                edge.graphics.updatePositions()

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)
        for item in self.model.scene.selectedItems():
            if isinstance(item.graphics, NodeGraphics):
                item.graphics.setPos(item.graphics.pos())
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self._was_moved:
            self._was_moved = False
            self.model.scene.history.storeHistory("Node moved", setModified=True)

            self.model.scene.resetLastSelectedStates()
            self._last_selected_state = True
            self.model.scene.last_selected_items = self.model.scene.getSelectedItems()
            return

        # handle when graphics was clicked on
        if self._last_selected_state != self.isSelected() or \
                self.model.scene.last_selected_items != self.model.scene.getSelectedItems():
            self.model.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.on_selected()

    def itemChange(self, change, value):
        if change == 4:
            return value * 100
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def change_colors(self, title_background_color=None, background_color=None, title_shadow_color=None):
        if title_background_color:
            self.title_background_color = title_background_color
        if background_color:
            self.background_color = background_color
        if title_shadow_color:
            self.title_shadow_color = title_shadow_color

    def refresh_colors(self):
        gradient = QLinearGradient(QPointF(self.width * 0.75, 0), QPointF(self.width, self.title_height))
        gradient.setColorAt(0, QColor(self.title_background_color))
        gradient.setColorAt(1, QColor(self.title_shadow_color))
        self._brush_title = QBrush(gradient)
        self._brush_background = QBrush(QColor(self.background_color))

    def scenePos(self):
        return QPoint(int(super().scenePos().x()), int(super().scenePos().y()))

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def update_title(self, custom_title=None):
        title = custom_title if custom_title is not None else self.model.title
        if not self.title_item:
            self.title_item = TitleTextItem(self)
        self.title_item.setPlainText(title)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding + self.corner_roundness, 0)
        self.refresh_shape()

    def draw_shape(self, painter, shape, pen=Qt.NoPen, brush=None):
        painter.setPen(pen)
        painter.setBrush(brush if brush else self._brush_background)
        painter.drawPath(shape.simplified())

        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen_selected if self.isSelected() else
                       self._pen_hovered if self.hovered else
                       self._pen_default)
        painter.drawPath(shape.simplified())

    def refresh_shape(self):
        max_input_width = 0
        max_output_width = 0

        for socket in self.model.inputs:
            input_width = socket.graphics.get_width()
            if input_width > max_input_width:
                max_input_width = input_width

        for socket in self.model.outputs:
            output_width = socket.graphics.get_width()
            if output_width > max_output_width:
                max_output_width = output_width

        min_width = self.title_item.boundingRect().width() + self.title_horizontal_padding if self.title_item else 0

        if len(self.model.inputs):
            last_input = self.model.inputs[-1].graphics
            inputs_height = last_input.pos().y() + last_input.get_height()//2
        else:
            inputs_height = 0
        if len(self.model.outputs):
            last_output = self.model.outputs[-1].graphics
            outputs_height = last_output.pos().y() + last_output.get_height()//2
        else:
            outputs_height = 0

        self.height = max(inputs_height, outputs_height)
        self.width = 2 * self.corner_roundness + max(max_input_width + max_output_width, min_width)
        if self.max_width >= 0:
            self.width = min(self.width, self.max_width)

        grid_size = self.model.scene.graphics.gridSize
        if self.height % grid_size:
            self.height = self.height - self.height % grid_size + grid_size

        if self.width % grid_size:
            self.width = self.width - self.width % grid_size + grid_size

        self.refresh_colors()

        for output in self.model.outputs:
            output.graphics.update_pos_x(self.width - self.socket_padding, refresh_edges=True)

        if self.model.handle is not None:
            self.model.handle.graphics.update_pos_x(self.width, refresh_edges=True)

    def update_sockets_pos(self):
        socket_y = self.title_height
        for socket in self.model.inputs:
            socket_y = socket.graphics.update_pos(self.socket_padding, socket_y).y()
        socket_y = self.title_height
        for socket in self.model.outputs:
            socket_y = socket.graphics.update_pos(self.width - self.socket_padding, socket_y).y()
        self.refresh_shape()

    def paint(self, painter, _, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.moveTo(0, self.title_height + 1)
        path_title.lineTo(self.width, self.title_height + 1)
        path_title.lineTo(self.width, self.corner_roundness)
        path_title.arcTo(self.width - self.corner_roundness * 2, 0,
                         self.corner_roundness * 2, self.corner_roundness * 2, 0, 90)
        path_title.lineTo(self.corner_roundness, 0)
        path_title.arcTo(0, 0, self.corner_roundness * 2, self.corner_roundness * 2, 90, 90)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width,
                                    self.height - self.title_height, self.corner_roundness, self.corner_roundness)
        path_content.addRect(0, self.title_height, self.corner_roundness, self.corner_roundness)
        path_content.addRect(self.width - self.corner_roundness, self.title_height,
                             self.corner_roundness, self.corner_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.corner_roundness, self.corner_roundness)
        painter.setBrush(Qt.NoBrush)
        if self.hovered and not self.isSelected():
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())
