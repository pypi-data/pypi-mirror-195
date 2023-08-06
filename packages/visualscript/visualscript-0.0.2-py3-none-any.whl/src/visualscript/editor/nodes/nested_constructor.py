from typing import Any
from editor.config import register_node
from editor.nodes.executable import ExecutableNode

@register_node()
class NestedConstructorNode(ExecutableNode):
    title = "NestedConstruct"
    category = "Abstract"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types=[Any, *input_types], output_types=[type, *output_types])
        self.graphics.change_colors("#FF611161")
        self.graphics.setToolTip("Constructor")
        self.inputs[1].updateName("self")
        self.connected_sockets = []

    def get_value(self, index=0):
        parent_object = self.get_input_value(1)

        if not parent_object:
            return

        hierarchy = self.title.split('.')

        item = None
        for level in hierarchy:
            if item:
                item = item.__getattribute__(level)
            else:
                    item = parent_object.__getattribute__(level)

        return item

    def connect_parent(self, socket):
        from editor.core.models.edge import Edge
        Edge(self.scene, socket, self.inputs[1])

    def update_output_type(self):
        value = self.get_value()
        if value is not None:
            self.outputs[1].updateDataType(type(value))
            self.outputs[1].graphics.update()
            description = value.__doc__
            if description:
                self.graphics.setToolTip(description.strip())

    async def execute(self):
        self.update_output_type()
        await super().execute()

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        if new_edge.end_socket == self.inputs[1]:
            self.inputs[1].updateDataType(new_edge.start_socket.data_type)
            self.generate_sockets()
        self.update_output_type()
