from editor.nodes.event import EventNode
from editor.core.models.data_types import EXEC

class ExecutableNode(EventNode):
    title = "ExecutableNode"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [EXEC, *input_types], output_types)
        self.graphics.title_horizontal_padding = 5
        self.graphics.update_title()
