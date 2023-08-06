import types
import typing

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from editor.core.models.node import Node
from editor.core.models.socket import Socket
from editor.core.views.cutline import CutLine
from editor.core.views.edge import Edge, EdgeGraphics
from editor.core.models.data_types import EXEC

MODE_NOOP, MODE_EDGE_DRAG = range(2)

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = False

class WorkspaceView(QGraphicsView):

    StartSignal = pyqtSignal()
    StopSignal = pyqtSignal()

    loadedModule = pyqtSignal()
    updateModule = pyqtSignal(str)

    itemSelected = pyqtSignal()
    itemsDeselected = pyqtSignal()
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, graphics, parent=None):
        super().__init__(parent)

        self.graphics = graphics
        self.scene = graphics.model
        self.initUI()

        self.setScene(self.graphics)
        self.itemSelected.connect(self.scene.onItemSelected)
        self.itemsDeselected.connect(self.scene.onItemsDeselected)

        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDraggingRectangle = False

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 0.8
        self.zoomLevel = 0
        self.min_zoom = -12
        self.max_zoom = 3

        self.drag_edge = None

        self.cutline = CutLine()

        self._click_listeners = []
        self._drag_enter_listeners = []
        self._drop_listeners = []


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)


    def dragEnterEvent(self, event):
        for callback in self._drag_enter_listeners: callback(event)

    def dropEvent(self, event):
        for callback in self._drop_listeners: callback(event)

    def addMouseClickListener(self, callback):
        self._click_listeners.append(callback)

    def addDragEnterListener(self, callback):
        self._drag_enter_listeners.append(callback)

    def addDropListener(self, callback):
        self._drop_listeners.append(callback)

    def mousePressEvent(self, event):
        for callback in self._click_listeners: callback(event)
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if type(item) is Socket:
            if event.modifiers() & Qt.AltModifier:
                for i in range(len(item.edges)-1, -1, -1):
                    item.edges[i].remove()
                return
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return


        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(event, item)
            if res: return
            items = self.getItemsAtClick(event)
            for other_item in items:
                if other_item != item:
                    res = self.edgeDragEnd(event, other_item)
                    if res: return

        if item is None:
            # if event.modifiers() & Qt.ControlModifier:
                # self.mode = MODE_EDGE_CUT
                # fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                #                         Qt.LeftButton, Qt.NoButton, event.modifiers())
                # super().mouseReleaseEvent(fakeEvent)
                # QApplication.setOverrideCursor(Qt.CrossCursor)
                # return
            # else:
            self.rubberBandDraggingRectangle = True

        super().mousePressEvent(event)


    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)

        if item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(event, item)
                if res: return
                items = self.getItemsAtClick(event)
                for other_item in items:
                    if other_item != item:
                        res = self.edgeDragEnd(event, other_item)
                        if res: return

        # if self.mode == MODE_EDGE_CUT:
        #     self.cutIntersectingEdges()
        #     self.cutline.line_points = []
        #     self.cutline.update()
        #     QApplication.setOverrideCursor(Qt.ArrowCursor)
        #     self.mode = MODE_NOOP
        #     return


        if self.rubberBandDraggingRectangle:
            self.rubberBandDraggingRectangle = False
            current_selected_items = self.graphics.selectedItems()

            if current_selected_items != self.scene.last_selected_items:
                if current_selected_items == []:
                    self.itemsDeselected.emit()
                else:
                    self.itemSelected.emit()
                self.scene.last_selected_items = current_selected_items

            return

        if item is None:
            self.itemsDeselected.emit()

        super().mouseReleaseEvent(event)



    def rightMouseButtonPress(self, event):
        pass
    #     super().mousePressEvent(event)


    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)


    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            if self.drag_edge:
                self.drag_edge.setDestination(pos.x(), pos.y())
                self.drag_edge.update()

        # if self.mode == MODE_EDGE_CUT:
        #     pos = self.mapToScene(event.pos())
        #     self.cutline.line_points.append(pos)
        #     self.cutline.update()

        self.last_scene_mouse_position = self.mapToScene(event.pos())

        self.scenePosChanged.emit(
            int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y())
        )

        try:
            super().mouseMoveEvent(event)
        except Exception as e:
            print(e)


    def keyPressEvent(self, event):
        super().keyPressEvent(event)


    # def cutIntersectingEdges(self):
    #     for ix in range(len(self.cutline.line_points) - 1):
    #         p1 = self.cutline.line_points[ix]
    #         p2 = self.cutline.line_points[ix + 1]
    #
    #         for edge in self.scene.edges:
    #             if edge.graphics.intersectsWith(p1, p2):
    #                 edge.remove()
    #     self.scene.history.storeHistory("Delete cutted edges", setModified=True)



    def deleteSelected(self):
        for item in self.scene.selectedItems():
            item.remove()
        self.scene.history.storeHistory("Delete selected", setModified=True)



    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out

    def getItemAtClick(self, event):
        pos = event.pos()
        graphic_item = self.itemAt(pos)
        if isinstance(graphic_item, EdgeGraphics):
            return None
        return graphic_item.model if hasattr(graphic_item, "model") else graphic_item

    def getItemsAtClick(self, event):
        graphic_items = self.items(event.pos())
        items = []
        for graphic_item in graphic_items:
            if isinstance(graphic_item, EdgeGraphics):
                continue
            items.append(graphic_item.model if graphic_item and hasattr(graphic_item, "model") else graphic_item)
        return items

    def edgeDragStart(self, item):
        # from editor.core.models.edge import Edge
        self.drag_start_socket = item
        self.drag_edge = EdgeGraphics(start_socket=item)
        # self.drag_edge.setSource()
        self.scene.graphics.addItem(self.drag_edge)


    def edgeDragEnd(self, event, item):
        self.mode = MODE_NOOP

        if DEBUG:
            print('View::edgeDragEnd ~ End dragging edge')

        if type(item) is Socket:
            if item.is_input != self.drag_start_socket.is_input and item.node is not self.drag_start_socket.node:
                sockets = (self.drag_start_socket, item) if item.is_input else (item, self.drag_start_socket)

                if not self.check_type_compatibility(sockets[0].data_type, sockets[1].data_type):
                    self.removeDragEdge()
                    return False

                if not item.is_multi_edges:
                    item.removeAllEdges()

                if not self.drag_start_socket.is_multi_edges:
                    self.drag_start_socket.removeAllEdges()

                new_edge = Edge(self.scene, *sockets)
                if DEBUG: print("View::edgeDragEnd ~  created new edge:", new_edge, "connecting", new_edge.start_socket, "<-->", new_edge.end_socket)

                self.removeDragEdge()
                self.scene.history.storeHistory("Created new edge by dragging", setModified=True)
                return True
            else:
                self.removeDragEdge()
                return False
        elif isinstance(item, Node):
            self.removeDragEdge()
            return False
        elif item is None:
            self.handleContextMenu(event, self.drag_start_socket)
            self.removeDragEdge()
            return False
        else:
            self.removeDragEdge()
            return False

    def check_type_compatibility(self, type_a, type_b, check_flipped=True):
        if type_a == typing.Any and type_b != EXEC:
            return True
        if check_flipped:
            if type_a == type_b:
                return True
            if isinstance(type_a, type) and isinstance(type_b, type):
                return issubclass(type_a, type_b)
            if self.check_type_compatibility(type_b, type_a, False):
                return True
        if typing.get_origin(type_a) == typing.Union or typing.get_origin(type_a) == types.UnionType:
            for arg in typing.get_args(type_a):
                if self.check_type_compatibility(arg, type_b):
                    return True
        if typing.get_origin(type_a) == tuple:
            if hasattr(type_b, '__len__') and len(typing.get_args(type_a)) == len(type_b):
                return True
        if typing.get_origin(type_a) == list:
            required_elements_type = typing.get_args(type_a)
            if len(required_elements_type) == 1:
                required_elements_type = required_elements_type[0]
                if isinstance(type_b, tuple) or isinstance(type_b, list):
                    for element in type_b:
                        if element != required_elements_type:
                            break
                    else:
                        return True
                if type_b == tuple or typing.get_origin(type_b) == tuple:
                    for arg in typing.get_args(type_b):
                        if arg != required_elements_type:
                            break
                    else:
                        return True
        return False

    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            if self.zoomLevel < self.max_zoom:
                self.zoomLevel += 1
                self.scale(self.zoomInFactor, self.zoomInFactor)
            else:
                return
        else:
            if self.zoomLevel > self.min_zoom:
                self.zoomLevel -= 1
                self.scale(self.zoomOutFactor, self.zoomOutFactor)
            else:
                return

    def clamp(self, value, min, max):
        return min(max(min, value), max)

    def removeDragEdge(self):
        if self.drag_edge:
            self.scene.graphics.removeItem(self.drag_edge)
            # self.drag_edge.remove()
            self.drag_edge = None

    def handleContextMenu(self, event, start_socket: Socket):
        if not start_socket.is_input and not isinstance(start_socket.data_type, int):
            from editor.core.models.context_menu import ContextMenu
            from editor.core.models.element_browsers.inherited_attribute_browser import InheritedAttibutesBrowser
            self.context_menu = ContextMenu(self, InheritedAttibutesBrowser(start_socket))
            self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def focusInEvent(self, event):
        attribute_browser = self.scene.getAttributeBrowser()
        if attribute_browser.module != self.scene.module:
            attribute_browser.reload(self.scene.module)