import asyncio
import threading
import time

from editor.config import register_node
from editor.nodes.event import EventNode

@register_node()
class TickEventNode(EventNode):
    title = "Tick"
    category = "Default"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, [float, *output_types])

        self.shouldTick = False
        self.last_timestamp = 0

        self.add_signals({self.scene.getView().StartSignal: self.start_tick_thread,
                          self.scene.getView().StopSignal: self.end_tick_thread})

        self.graphics.setToolTip("Event triggered on start")

    def start_tick_thread(self):
        self.shouldTick = True
        self.last_timestamp = time.time()
        thread = threading.Thread(target=self.run_async_execute)
        thread.start()

    def end_tick_thread(self):
        self.shouldTick = False

    def run_async_execute(self):
        asyncio.run(self.execute())

    async def execute(self):
        while self.shouldTick:
            await self.execute_child(0)
            new_timestamp = time.time()
            self.value = new_timestamp - self.last_timestamp
            self.last_timestamp = new_timestamp
