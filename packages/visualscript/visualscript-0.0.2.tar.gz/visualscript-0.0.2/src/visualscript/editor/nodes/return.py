from typing import Any
from editor.config import register_node
from editor.core.models.node import Node
from editor.core.models.data_types import EXEC

@register_node()
class ReturnNode(Node):
    title = "Return"
    category = "Default"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [EXEC, Any, *input_types], output_types)

    async def execute(self):
        node = self
        while node.get_input_node(0):
            node = node.get_input_node(0)
        node.value = self.get_input_value(1)
        # await super().execute()
