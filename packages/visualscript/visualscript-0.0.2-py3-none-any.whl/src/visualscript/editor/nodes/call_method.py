from typing import Any
from editor.config import register_node
from editor.nodes.call_function import CallFunctionNode

@register_node()
class CallMethodNode(CallFunctionNode):
    title = "Call Method"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types=[Any, *input_types], output_types=output_types)
        self.inputs[1].updateName("self")
        self.inputs_first_index = 2

    def get_parent_item(self):
        return self.get_input_data_type(1)

    def reset_inputs(self, module_key=None):
        parent_name = str(self.get_parent_item())
        if parent_name.startswith("<class '"):
            parent_name = parent_name[len("<class '"):-len("'>")]
        parent_name = parent_name.split('.')[-1]
        if module_key == parent_name or module_key is None:
            parent_edges = self.inputs[1].edges
            if len(parent_edges):
                self.inputs[1].updateDataType(parent_edges[0].start_socket.data_type)
            super().reset_inputs()

    def connect_parent(self, socket):
        from editor.core.models.edge import Edge
        Edge(self.scene, socket, self.inputs[1])

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        if new_edge.end_socket == self.inputs[1]:
            self.reset_inputs()
