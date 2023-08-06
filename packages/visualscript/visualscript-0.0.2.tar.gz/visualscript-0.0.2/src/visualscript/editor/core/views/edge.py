from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem
from PyQt5.QtGui import QPen, QPainterPath, QColor
from PyQt5.QtCore import Qt, QPoint, QPointF
from editor.core.views.data_types import TYPE_COLORS, OBJECT_COLOR
from editor.core.models.edge import Edge

EDGE_CP_ROUNDNESS = 100


class EdgeGraphics(QGraphicsPathItem):
    def __init__(self, model=None, parent=None, start_socket=None):
        super().__init__(parent)

        self.model = model

        self._last_selected_state = False
        self.hovered = False

        if self.model:
            self.posSource = self.model.start_socket.graphics.getSocketPosition() if self.model.start_socket else [0, 0]
            self.posDestination = self.model.end_socket.graphics.getSocketPosition() if self.model.end_socket else self.posSource
        else:
            self.posSource = self.posDestination = start_socket.graphics.getSocketPosition()

        self.start_socket = start_socket

        self.initAssets()
        self.initUI()

    def initUI(self):
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

    def initAssets(self):
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._color_hovered = QColor("#FF37A6FF")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidthF(3.0)
        self._pen_selected.setWidthF(3.0)
        self._pen_dragging.setWidthF(3.0)
        self._pen_hovered.setWidthF(5.0)

    # def onSelected(self):
    #     self.model.scene.getView().itemSelected.emit()

    def mouseDoubleClickEvent(self, event):
        from editor.nodes.reroute import RerouteNode
        reroute_node = RerouteNode(self.model.scene)
        reroute_node.graphics.setPos(QPoint(int(event.pos().x() - reroute_node.graphics.width//2),
                                            int(event.pos().y() - reroute_node.graphics.height//2)))
        Edge(self.model.scene, self.model.start_socket, reroute_node.inputs[0])
        Edge(self.model.scene, reroute_node.outputs[0], self.model.end_socket)
        self.model.remove()

    # def doSelect(self, new_state=True):
    #     self.setSelected(new_state)
    #     self._last_selected_state = new_state
    #     if new_state:
    #         self.onSelected()

    # def mouseReleaseEvent(self, event):
    #     super().mouseReleaseEvent(event)
    #     if self._last_selected_state != self.isSelected():
    #         self.model.scene.resetLastSelectedStates()
    #         self._last_selected_state = self.isSelected()
    #         self.onSelected()

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def updatePositions(self):
        if self.model.start_socket is not None:
            source_pos = self.model.start_socket.graphics.getSocketPosition()
            self.setSource(*source_pos)
        if self.model.end_socket is not None:
            end_pos = self.model.end_socket.graphics.getSocketPosition()
            self.setDestination(*end_pos)
        self.update()

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calcPath()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.setPath(self.calcPath())

        painter.setBrush(Qt.NoBrush)

        if self.model:
            data_type = self.model.start_socket.data_type
        else:
            data_type = self.start_socket.data_type

        if TYPE_COLORS.__contains__(data_type):
            common_pen = QPen(TYPE_COLORS[data_type])
        else:
            common_pen = QPen(OBJECT_COLOR)
        common_pen.setStyle(Qt.SolidLine)
        common_pen.setWidthF(3.0)

        # if self.model.end_socket:
        if self.model is None:
            common_pen.setStyle(Qt.DashLine)

        if self.hovered:
            common_pen.setWidthF(7.0)

        painter.setPen(common_pen)
        painter.drawPath(self.path())

    # def intersectsWith(self, p1, p2):
    #     raise NotImplemented("This method has to be overriden in a child class")

    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        signX = 1 if self.posDestination[0] > self.posSource[0] else -1
        signY = 1 if self.posDestination[1] > self.posSource[1] else -1
        phase_forward = 1
        if (self.model and self.model.start_socket.is_input) or (self.start_socket and self.start_socket.is_input):
            signX *= -1
            phase_forward = -1
        max_phase = 15
        distX = abs(self.posDestination[0] - self.posSource[0])
        distY = abs(self.posDestination[1] - self.posSource[1])
        use_additional_fold = signX == -1 or (distX != distY and distX <= 2*max_phase)

        phase = min(max_phase, distY//4) if use_additional_fold else min(max_phase, distY//2)
        next_point = [self.posSource[0], self.posSource[1]]
        next_point[0] = self.posSource[0] + min(distY//2 - phase, phase) * phase_forward if use_additional_fold \
            else (self.posSource[0] + self.posDestination[0]) // 2 - phase * signX * phase_forward
        path.lineTo(*next_point)
        next_point[0] += phase * phase_forward
        next_point[1] += phase * signY
        path.lineTo(*next_point)
        if use_additional_fold:
            next_point[1] = (self.posSource[1] + self.posDestination[1]) // 2 - phase * signY
            path.lineTo(*next_point)
            next_point[0] -= phase * phase_forward
            next_point[1] += phase * signY
            path.lineTo(*next_point)
            next_point[0] = self.posDestination[0] - phase * phase_forward
            path.lineTo(*next_point)
            next_point[0] -= phase * phase_forward
            next_point[1] += phase * signY
            path.lineTo(*next_point)
        next_point[1] = self.posDestination[1] - phase * signY
        path.lineTo(*next_point)
        next_point[0] += phase * phase_forward
        next_point[1] += phase * signY
        path.lineTo(*next_point)
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path
