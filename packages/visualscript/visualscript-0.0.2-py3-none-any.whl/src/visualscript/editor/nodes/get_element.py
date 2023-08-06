from typing import Any
from editor.config import register_node
from editor.core.models.node import Node


@register_node()
class GetElementNode(Node):
    title = "GetElement"
    category = "Default"
    color = "#FF116111"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [Any, int, *input_types], [Any, *output_types])
        self.inputs[0].updateName('iterable')
        self.inputs[1].updateName('id=0')

    def get_value(self, index=0):
        element_id = self.get_input_value(1)
        if element_id is None:
            element_id = 0
        return self.get_input_value(0)[element_id]

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        try:
            value = self.get_value()
            if value is not None:
                self.outputs[0].updateDataType(value)
        except TypeError:
            pass
        except KeyError:
            pass
        except IndexError:
            pass
