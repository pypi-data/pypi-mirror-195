from typing import Any
import asyncio
from editor.nodes.executable import ExecutableNode
from editor.config import register_node

@register_node()
class DelayNode(ExecutableNode):
    title = "Delay"
    category = "Default"
    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [Any, *input_types], output_types)
        self.graphics.refresh_shape()
        self.can_execute = False
        self.add_signals({self.scene.getView().StartSignal: self.enable_coroutine,
                          self.scene.getView().StopSignal: self.disable_coroutine})

    def enable_coroutine(self):
        self.can_execute = True

    def disable_coroutine(self):
        self.can_execute = False

    async def execute(self):
        if self.can_execute:
            input_value = self.get_input_value(1)
            if input_value:
                await asyncio.sleep(input_value)
        if self.can_execute:
            await super().execute()
