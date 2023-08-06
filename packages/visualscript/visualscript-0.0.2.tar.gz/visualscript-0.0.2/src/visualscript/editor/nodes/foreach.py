from typing import Any
from editor.config import register_node
from editor.nodes.executable import ExecutableNode
from editor.core.models.data_types import EXEC


@register_node()
class ForEachNode(ExecutableNode):
    title = "For Each"
    category = "Default"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [Any, *input_types], [Any, int, EXEC, *output_types])

    async def execute(self):
        iterable = self.get_input_value(1)
        for i, element in enumerate(iterable):
            self.value = [element, i]
            await super().execute()
        await self.execute_child(3)

    def get_value(self, index=0):
        if index <= len(self.outputs) - 2:
            return self.value[index - 1]
