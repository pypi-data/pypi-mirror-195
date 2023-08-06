from editor.core.models.node import Node
from editor.core.models.data_types import EXEC

class EventNode(Node):
    title = "EventNode"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, [EXEC, *output_types], give_handle=True)
