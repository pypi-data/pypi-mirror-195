from typing import Any
from PyQt5.QtCore import Qt
from editor.core.models.node import Node
from editor.config import register_node

@register_node()
class NewClassNode(Node):
    title = "New Class"
    category = "Default"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [Any, Any, *input_types], [type, *output_types])
        self.inputs[0].updateName('base classes')
        self.inputs[1].updateName('dictionary')
        self.graphics.mouseDoubleClickEvent = self.edit_title
        self.add_signals({self.graphics.title_item.UnfocusSignal: self.save_class,
                          self.graphics.title_item.KeyPressSignal: self.graphics.refresh_shape})
        self.save_class()

    def edit_title(self, event):
        title_item = self.graphics.title_item
        title_item.textCursor().setVisualNavigation(True)
        title_item.setTextInteractionFlags(Qt.TextEditorInteraction)

    def get_value(self, index=0):
        base = self.get_input_value(0)
        if base is None:
            base = tuple()
        else:
            base = tuple([base])
        dictionary = self.get_input_value(1)
        if not isinstance(dictionary, dict):
            dictionary = {}
        try:
            return type(self.title, base, dictionary)
        except TypeError as e:
            print(e)

    def save_class(self, event=None):
        new_title = self.graphics.title_item.toPlainText()
        if new_title != self.title:
            if self.scene.module.__dict__.__contains__(self.title):
                self.scene.module.__dict__.pop(self.title)
            while self.scene.module.__dict__.__contains__(new_title):
                try:
                    used_title = new_title.split('_')
                    index = int(used_title[-1])
                    new_title = used_title[0] + '_' + str(index + 1)
                except ValueError as e:
                    new_title += '_1'
            self.title = new_title
            self.graphics.update_title()
        value = self.get_value()
        self.scene.updateModule(self.title, value)

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        self.save_class()

    def update(self):
        self.save_class()
