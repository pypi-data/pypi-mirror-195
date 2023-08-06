from typing import Any
from editor.config import register_node
from editor.core.models.node import Node
from editor.core.views.add_button import AddButton
from editor.core.views.remove_button import RemoveButton

@register_node()
class MakeListNode(Node):
    title = "Make List"
    category = "Default"
    color = "#FF116111"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, [list, *output_types])
        self.add_button = AddButton(self.graphics)
        self.add_button.mousePressEvent = self.add_entry
        self.remove_button = RemoveButton(self.graphics)
        self.remove_button.mousePressEvent = self.remove_entry
        self.remove_button.hide()
        self.entries = 0
        for _ in range(1):
            self.add_entry()

    def add_entry(self, event=None):
        self.add_input(Any)
        self.entries += 1
        if self.entries > 1:
            self.remove_button.show()
        self.update_buttons()

    def remove_entry(self, event=None):
        self.scene.graphics.removeItem(self.inputs[-1].graphics)
        for edge in self.inputs[-1].edges:
            edge.remove()
        self.inputs.pop(-1)
        self.entries -= 1
        if self.entries == 1:
            self.remove_button.hide()
        self.graphics.refresh_shape()
        self.update_buttons()

    def update_buttons(self):
        pos_x = self.graphics.socket_padding
        self.remove_button.setPos(pos_x, self.graphics.height)
        if self.remove_button.isVisible():
            pos_x += 2 * self.remove_button.radius
        self.add_button.setPos(pos_x, self.graphics.height)
        self.add_button.hovered = False
        self.remove_button.hovered = False

    def get_value(self, index=0):
        result = []
        for i in range(len(self.inputs)):
            result.append(self.get_input_value(i))
        return result

    def serialize(self):
        data = super().serialize()
        data['entries'] = self.entries
        return data

    def deserialize(self, data, hashmap={}, restore_id=True):
        for i in range(1, data['entries']):
            self.add_entry()
        super().deserialize(data, hashmap, restore_id)
