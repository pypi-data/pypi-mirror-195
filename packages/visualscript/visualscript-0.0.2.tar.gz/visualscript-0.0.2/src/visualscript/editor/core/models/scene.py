import os
from collections import OrderedDict
from PyQt5.QtCore import pyqtSignal
from editor.core.models.serializable import Serializable
from editor.core.models.scene_history import SceneHistory
from importlib.machinery import SourceFileLoader
from editor.core.models.scene_clipboard import SceneClipboard
from editor.core.views.scene import SceneView

DEBUG = False


class Scene(Serializable):
    module_update = pyqtSignal(str)

    def __init__(self, script_path=None):
        super().__init__()

        self.items = []

        self.script_path = ''
        self.module = None

        self.scene_width = 64000
        self.scene_height = 64000

        self.loaded = False
        self.has_been_modified = False
        self.last_selected_items = []

        # initialiaze all listeners
        self.has_been_modified_listeners = []
        self.item_selected_listeners = []
        self.items_deselected_listeners = []

        # here we can store callback for retrieving the class for Nodes
        self.node_class_selector = None

        # self.initUI()
        self.graphics = SceneView(self)
        self.graphics.setgraphics(self.scene_width, self.scene_height)

        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

    def initModule(self, script_path):
        self.script_path = os.path.relpath(script_path, os.curdir)
        self.module = SourceFileLoader(os.path.basename(self.script_path).split(".")[0],
                                       self.script_path).load_module() if self.script_path else None
        self.getAttributeBrowser().reload(self.module)

    def updateModule(self, key, value=None, can_remove=False):
        if value is None and can_remove:
            reload_needed = False
            if key in self.module.__dict__:
                reload_needed = True
            self.module.__dict__.pop(key)
        else:
            reload_needed = True
            if key in self.module.__dict__:
                reload_needed = False
            self.module.__dict__[key] = value
        self.getView().updateModule.emit(key)
        if reload_needed:
            self.getAttributeBrowser().reload(self.module)

    def onItemSelected(self):
        current_selected_items = self.getSelectedItems()
        if current_selected_items != self.last_selected_items:
            self.last_selected_items = current_selected_items
            self.history.storeHistory("Selection Changed")
            for callback in self.item_selected_listeners: callback()

    def onItemsDeselected(self):
        self.resetLastSelectedStates()
        if self.last_selected_items != []:
            self.last_selected_items = []
            self.history.storeHistory("Deselected Everything")
            for callback in self.items_deselected_listeners: callback()

    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.graphics.selectedItems()

    def modify(self, value):
        if not self.has_been_modified and value:
            self._has_been_modified = value
            for callback in self.has_been_modified_listeners: callback()
        self._has_been_modified = value

    def addHasBeenModifiedListener(self, callback):
        self.has_been_modified_listeners.append(callback)

    def addItemSelectedListener(self, callback):
        self.item_selected_listeners.append(callback)

    def addItemsDeselectedListener(self, callback):
        self.items_deselected_listeners.append(callback)

    def addMouseClickListener(self, callback):
        self.getView().addMouseClickListener(callback)

    def addDragEnterListener(self, callback):
        self.getView().addDragEnterListener(callback)

    def addDropListener(self, callback):
        self.getView().addDropListener(callback)

    # custom flag to detect node or edge has been selected....
    def resetLastSelectedStates(self):
        for item in self.items:
            if item and item.graphics:
                item.graphics._last_selected_state = False

    def itemAt(self, pos):
        return self.getView().itemAt(pos)

    def getView(self):
        return self.graphics.views()[0]

    def getAttributeBrowser(self):
        from editor.workspace_window import WorkspaceWindow
        window = self.getView().window()
        if isinstance(window, WorkspaceWindow):
            window = window.parent
        return window.attributeBrowser

    def addItem(self, item):
        if item in self.items:
            return
        self.items.append(item)
        self.graphics.addItem(item.graphics)

    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            self.graphics.removeItem(item.graphics)
            item.graphics = None

    def clear(self):
        while len(self.items) > 0:
            self.graphics.removeItem(self.items.pop().graphics)

        self.has_been_modified = False

    def selectedItems(self):
        result = []
        for item in self.graphics.selectedItems():
            result.append(item.model)
        return result

    def saveToFile(self, filename):
        import json
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=1))
            if DEBUG:
                print("saving to", filename, "was successfull.")

            self.has_been_modified = False

    def loadFromFile(self, file_path):
        import json
        with open(file_path, "r") as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data)
                self.initModule(data['script_path'])
                self.deserialize(data)
            except json.JSONDecodeError:
                self.initModule(file_path)
            finally:
                self.loaded = True

    def setNodeClassSelector(self, class_selecting_function):
        self.node_class_selector = class_selecting_function

    def getNodeClassFromData(self, data):
        return self.node_class_selector(data) if self.node_class_selector else None

    def serialize(self):
        serialized_items = []
        for item in self.items:
            serialized_items.append(item.serialize())

        return OrderedDict([
            ('id', self.id),
            ('script_path', self.script_path),
            ('items', serialized_items),
        ])

    def deserialize(self, data, hashmap=None, restore_id=True):
        self.clear()
        hashmap = {}

        super().deserialize(data, hashmap, restore_id)

        from editor.core.models.edge import Edge

        edges = []
        for item_data in data['items']:
            if item_data.keys().__contains__('title'):
                self.getNodeClassFromData(item_data)(self, item_data['title']).deserialize(item_data, hashmap, restore_id)
            else:
                new_edge = Edge(self).deserialize(item_data, hashmap, restore_id)
                if new_edge:
                    edges.append(new_edge)

        self.has_been_modified = False
        return True
