import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from editor.config import *
from editor.core.models.workspace import WorkspaceWidget
from editor.core.utils import dumpException

DEBUG_CONTEXT = False

class WorkspaceWindow(WorkspaceWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()
        self.context_menu = None
        self.class_defaults = {}

        self.initNewNodeActions()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.history.addHistoryRestoredListener(self.onHistoryRestored)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)
        self.scene.addMouseClickListener(self.onMouseClick)

        self._close_event_listeners = []

    def getNodeClassFromData(self, data):
        if 'class' not in data: return None
        return get_class_from_name(data['class'])

    def Compile(self):
        if self.scene.module:
            for value in dir(self.scene.module):
                self.class_defaults[value] = self.scene.module.__dict__[value]
        self.scene.getView().StartSignal.emit()

    def Stop(self):
        self.scene.getView().StopSignal.emit()
        for value in dir(self.scene.module):
            if self.class_defaults.__contains__(value):
                self.scene.module.__dict__[value] = self.class_defaults[value]


    def onHistoryRestored(self):
        pass
        # self.doEvalOutputs()

    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(CLASS_REGISTRY.keys())
        keys.sort()
        for key in keys:
            node = CLASS_REGISTRY[key]
            self.node_actions[node.__name__] = QAction(node.title)

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onMouseClick(self, event):
        pass

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        self.hideContextMenu()
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            class_name = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.graphics.views()[0].mapToScene(mouse_position)
            try:
                if not dataStream.atEnd():
                    title = dataStream.readQString()
                    node = get_class_from_name(class_name)(scene=self.scene, title=title)

                    node.generate_sockets()
                else:
                    node = get_class_from_name(class_name)(self.scene)

                node.graphics.setPos(scene_position)
                self.scene.history.storeHistory("Created node %s" % node.__class__.__name__)
            except Exception as e: dumpException(e)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        try:
            item = self.scene.itemAt(event.pos())

            # if hasattr(item, 'edge'):
            #     self.handleEdgeContextMenu(event)
            # else:
            self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e: dumpException(e)

    def handleNodeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: NODE")
        context_menu = QMenu(self)
        markDirtyAct = context_menu.addAction("Mark Dirty")
        markDirtyDescendantsAct = context_menu.addAction("Mark Descendant Dirty")
        markInvalidAct = context_menu.addAction("Mark Invalid")
        unmarkInvalidAct = context_menu.addAction("Unmark Invalid")
        evalAct = context_menu.addAction("Eval")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        # if type(item) == QGraphicsProxyWidget:
        #     item = item.widget()

        selected = item

        # if hasattr(item, 'node'):
        #     selected = item.node
        # if hasattr(item, 'socket'):
        #     selected = item.socket.node

        if DEBUG_CONTEXT: print("got item:", selected)
        if selected and action == markDirtyAct: selected.markDirty()
        if selected and action == markInvalidAct: selected.markInvalid()
        if selected and action == unmarkInvalidAct: selected.markInvalid(False)
        if selected and action == evalAct:
            val = selected.eval()
            if DEBUG_CONTEXT: print("EVALUATED:", val)


    def handleEdgeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: EDGE")
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        segmentedAct = context_menu.addAction("Segmented Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        # if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        # if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
        # if selected and action == segmentedAct: selected.edge_type = EDGE_TYPE_SEGMENTED


    def handleNewNodeContextMenu(self, event):
        from editor.core.models.context_menu import ContextMenu
        from editor.core.models.element_browsers.node_browser import NodeBrowser
        self.context_menu = ContextMenu(self, NodeBrowser())
        self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def hideContextMenu(self):
        if self.context_menu:
            self.context_menu.hide()

    # def focusInEvent(self, event):
    #     print("Focused")

    # def focusOutEvent(self, event):
    #     print("Unfocused")