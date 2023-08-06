import asyncio
from typing import Any
from editor.config import register_node
from editor.core.models.node import Node

@register_node()
class CastNode(Node):
    """Cast to different data type"""
    title = "Cast"
    category = "Helpers"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, '', [Any, *input_types], [Any, *output_types])
        self.type = ''
        self.graphics.change_colors(title_background_color=self.graphics.background_color,
                                    title_shadow_color=self.graphics.background_color)
        self.graphics.corner_roundness = 0
        self.graphics.refresh_shape()

        self.add_signals({self.scene.getView().updateModule: self.update})

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        if not new_edge.is_valid():
            return
        if self.outputs[0].data_type == Any:
            self.outputs[0].updateDataType(new_edge.start_socket.data_type if new_edge.end_socket == self.inputs[0]
                                           else new_edge.end_socket.data_type)

    def get_value(self, index=0):
        if not isinstance(self.outputs[0].data_type, int) and self.outputs[0].data_type != Any \
                and not asyncio.iscoroutine(self.outputs[0].data_type.__init__):
            try:
                return self.outputs[0].data_type(self.get_input_value(0))
            except ValueError as e:
                print(e)
            except TypeError as e:
                pass
        return self.get_input_value(0)

    def serialize(self):
        res = super().serialize()
        if self.outputs[0].data_type != Any:
            type_name = str(self.outputs[0].data_type)
            if type_name.startswith("<class '"):
                type_name = type_name[len("<class '"):-len("'>")]
            res['type'] = type_name
        return res

    def update(self, module_key=None):
        if self.outputs[0].data_type != Any:
            return
        prefix = ''
        type_name = self.type.split('.')
        if len(type_name) == 1:
            prefix = 'builtins.'
        type_name = type_name[-1]
        if type_name == module_key or module_key is None:
            data_type = self.find_item(self.scene.module, prefix + type_name)
            if data_type is None:
                data_type = self.find_item(self.scene.module, self.type)
            if data_type:
                self.outputs[0].updateDataType(data_type)
                for node in self.get_children_nodes(0):
                    node.update()

    def deserialize(self, data, hashmap=None, restore_id=True):
        super().deserialize(data, hashmap, restore_id)
        if 'type' in data:
            self.type = data['type']
            self.update()
