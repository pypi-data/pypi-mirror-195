import asyncio, threading
from editor.config import register_node
from editor.nodes.event import EventNode

@register_node()
class StartEventNode(EventNode):
    title = "Start"
    category = "Default"

    def __init__(self, scene, title=title):
        super().__init__(scene, title=title, input_types=[], output_types=[])
        self.add_signals({self.scene.getView().StartSignal: self.start_thread})
        self.graphics.setToolTip("Event triggered on start")

    def start_thread(self):
        thread = threading.Thread(target=self.run_async_execute)
        thread.start()

    def run_async_execute(self):
        asyncio.run(self.execute())

    async def execute(self):
        await self.execute_child(0)