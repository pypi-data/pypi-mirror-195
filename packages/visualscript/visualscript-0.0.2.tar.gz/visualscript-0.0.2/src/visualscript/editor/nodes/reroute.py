from typing import Any
from editor.config import register_node
from editor.core.models.node import Node

@register_node()
class RerouteNode(Node):
    """Reroute"""
    title = "Reroute"
    category = "Helpers"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, '', [Any, *input_types], [Any, *output_types])
        self.graphics.change_colors(title_background_color=self.graphics.background_color,
                                    title_shadow_color=self.graphics.background_color)
        self.graphics.corner_roundness = 0
        self.graphics.refresh_shape()

    def get_value(self, index=0):
        return self.get_input_value(0)

    def update(self):
        if len(self.inputs[0].edges):
            new_type = self.inputs[0].edges[0].start_socket.data_type
            if new_type != self.inputs[0].data_type:
                self.inputs[0].updateDataType(new_type)
                self.outputs[0].updateDataType(new_type)
                for node in self.get_children_nodes(0):
                    node.update()

    def on_edge_changed(self, new_edge):
        if new_edge.end_socket == self.inputs[0]:
            self.update()
