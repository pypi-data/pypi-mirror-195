from typing import Any
import inspect
from PyQt5.QtCore import Qt
from editor.nodes.event import EventNode
from editor.config import register_node
from editor.core.views.add_button import AddButton
from editor.core.views.remove_button import RemoveButton


@register_node()
class NewFunctionNode(EventNode):
    title = "New Function"
    category = "Default"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, output_types)
        self.keep_title_unique()
        self.graphics.mouseDoubleClickEvent = self.edit_title
        self.add_signals({self.graphics.title_item.UnfocusSignal: self.change_title,
                          self.graphics.title_item.KeyPressSignal: self.graphics.refresh_shape})

        self.entries = 0
        self.add_button = AddButton(self.graphics)
        self.add_button.mousePressEvent = self.add_entry
        self.remove_button = RemoveButton(self.graphics)
        self.remove_button.mousePressEvent = self.remove_entry
        self.remove_button.hide()
        self.update()

    def add_entry(self, event=None):
        self.add_output(Any, f"arg{len(self.outputs)-1}")
        self.entries += 1
        self.remove_button.show()
        self.update()

    def remove_entry(self, event=None):
        self.scene.graphics.removeItem(self.outputs[-1].graphics)
        for edge in self.outputs[-1].edges:
            edge.remove()
        self.outputs.pop(-1)
        self.entries -= 1
        if not self.entries:
            self.remove_button.hide()
        self.graphics.refresh_shape()
        self.update()

    def update_buttons(self):
        pos_x = self.graphics.width - self.graphics.socket_padding
        self.add_button.setPos(pos_x, self.graphics.height)
        pos_x -= 2 * self.remove_button.radius
        self.remove_button.setPos(pos_x, self.graphics.height)
        self.add_button.hovered = False
        self.remove_button.hovered = False

    def update_signature(self):
        async def overriden_function(*args, **kwargs):
            self.value = args
            for index in range(len(args)):
                if index + 1 < len(self.outputs):
                    self.outputs[index + 1].updateDataType(args[index].__class__)
            await super(NewFunctionNode, self).execute()
            return self.value

        param_objects = []
        for i in range(1, len(self.outputs)):
            param_objects.append(inspect.Parameter(self.outputs[i].name, inspect.Parameter.POSITIONAL_OR_KEYWORD))
        overriden_function.__signature__ = \
            inspect.signature(overriden_function).replace(parameters=param_objects)
        self.execute = overriden_function

    def update(self):
        self.update_buttons()
        self.update_signature()
        self.scene.updateModule(self.title, self.execute)
        for node in self.handle.get_connected_nodes():
            node.update()

    def edit_title(self, event):
        title_item = self.graphics.title_item
        title_item.textCursor().setVisualNavigation(True)
        title_item.setTextInteractionFlags(Qt.TextEditorInteraction)

    def change_title(self):
        new_title = self.graphics.title_item.toPlainText()
        if new_title != self.title:
            if self.title in self.scene.module.__dict__:
                self.scene.module.__dict__.pop(self.title)
            self.title = new_title
            self.keep_title_unique()

    def keep_title_unique(self):
        while self.title in self.scene.module.__dict__:
            try:
                used_title = self.title.split('_')
                index = int(used_title[-1])
                self.title = used_title[0] + '_' + str(index + 1)
            except ValueError as e:
                self.title += '_1'
        self.graphics.update_title()
        self.scene.updateModule(self.title, self.execute)

    def remove(self):
        super().remove()
        if self.scene.module.__dict__.__contains__(self.title):
            self.scene.updateModule(self.title, can_remove=True)

    def get_value(self, index=0):
        if not self.value or len(self.value) < index:
            return None
        return self.value[index-1]

    def serialize(self):
        data = super().serialize()
        if self.entries:
            data['entries'] = self.entries
        return data

    def deserialize(self, data, hashmap=None, restore_id=True):
        if not restore_id:
            self.scene.module.__dict__.pop(self.title)

        if data.__contains__('entries'):
            for i in range(data['entries']):
                self.add_entry()
        super().deserialize(data, hashmap, restore_id)

        if not restore_id:
            self.keep_title_unique()
