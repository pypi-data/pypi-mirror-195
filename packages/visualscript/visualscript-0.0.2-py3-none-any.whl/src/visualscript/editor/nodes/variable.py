from typing import Any
from editor.config import register_node
from editor.core.models.node import Node

@register_node()
class VariableNode(Node):
    title = "Variable"
    color = "#FF116111"
    tooltip = "Variable"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, [Any, *output_types])
        self.add_signals({self.scene.getView().updateModule: self.propagate_value_update})

    def generate_sockets(self, sockets_data=None):
        value = self.get_value()
        if value is not None:
            self.outputs[0].updateDataType(value.__class__)
            self.graphics.setToolTip(str(value))

        super().generate_sockets(sockets_data)

    def get_parent_item(self):
        return self.scene.module

    def get_value(self, index=0):
        return self.find_item(self.get_parent_item())

    def propagate_value_update(self, module_key):
        if module_key == self.title:
            self.generate_sockets()
            for node in self.outputs[0].get_connected_nodes():
                node.update()
