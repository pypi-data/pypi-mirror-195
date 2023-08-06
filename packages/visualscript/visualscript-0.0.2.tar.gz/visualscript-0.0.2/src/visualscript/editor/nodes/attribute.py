from typing import Any
from editor.config import register_node
from editor.nodes.variable import VariableNode
from editor.core.models.data_types import WILDCARD

@register_node()
class AttributeNode(VariableNode):
    title = "Attribute"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types=[Any, *input_types], output_types=output_types)
        self.graphics.title_horizontal_padding = 5

    def get_parent_item(self):
        return self.get_input_value(0)

    def connect_parent(self, socket):
        from editor.core.models.edge import Edge
        Edge(self.scene, socket, self.inputs[0])

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        if new_edge.end_socket == self.inputs[0]:
            self.inputs[0].updateDataType(new_edge.start_socket.data_type)

        value = self.get_value()
        if value is not None:
            self.outputs[0].updateDataType(type(value))
