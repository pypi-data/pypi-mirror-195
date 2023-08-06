from editor.config import register_node
from editor.core.models.node import Node
from editor.core.models.socket_contents.socket_text_content import SocketTextContent

@register_node()
class TextNode(Node):
    title = "Text"
    category = "Default"
    color = "#FF116111"
    tooltip = "Text"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, [str, *output_types])
        self.outputs[0].content = SocketTextContent(self.outputs[0])
        self.graphics.update_sockets_pos()

    def get_value(self, index=0):
        return self.outputs[0].content.get_value()

    def update(self):
        for node in self.outputs[0].get_connected_nodes():
            node.update()
