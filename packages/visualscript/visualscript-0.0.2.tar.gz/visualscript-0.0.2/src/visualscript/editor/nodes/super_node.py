from typing import Any
import inspect
from editor.config import register_node
from editor.nodes.executable import ExecutableNode
from editor.core.models.socket_contents.socket_text_content import SocketTextContent
from editor.core.views.socket_contents.socket_combo_box_content_widget import SocketComboBoxContentWidget

@register_node()
class SuperNode(ExecutableNode):
    """
    Node for referencing super object
    """

    title = "Super"
    category = "Default"

    def __init__(self, scene, title=title, input_types=tuple(), output_types=tuple()):
        super().__init__(scene, title, [Any, str, *input_types], [Any, *output_types])
        self.inputs[2].content = SocketTextContent(self.inputs[2], SocketComboBoxContentWidget)
        self.combo_box = self.inputs[2].content.graphics.combo_box
        self.add_signals({self.combo_box.textActivated: self.on_combo_box_item_change})
        self.graphics.update_sockets_pos()

    def on_combo_box_item_change(self, event):
        self.generate_sockets()
        for node in self.handle.get_connected_nodes():
            node.update()

    async def execute(self):
        input_object = self.get_input_value(1)
        if input_object is not None:
            args = []
            for i in range(3, len(self.inputs)):
                args.append(self.get_input_value(i))
            getattr(super(input_object.__class__, input_object), self.combo_box.currentText())(*args)
        await super().execute()

    def generate_sockets(self, sockets_data=None):
        for i in range(len(self.inputs) - 1, 2, -1):
            self.scene.graphics.removeItem(self.inputs[i].graphics)
            self.inputs.pop(i)

        if len(self.inputs[1].edges):
            item = self.inputs[1].edges[0].start_socket.data_type
        else:
            return

        item = self.find_item(super(item.__class__, item), self.combo_box.currentText())

        description = item.__doc__
        if description:
            self.graphics.setToolTip(description.strip())

        try:
            parameters = list(inspect.signature(item).parameters.keys())

            for i in range(len(parameters)):
                if parameters[i] == 'self' or parameters[i] == 'args' or parameters[i] == 'kwargs':
                    continue
                if hasattr(item, '__annotations__') and item.__annotations__.__contains__(parameters[i]):
                    self.add_input(item.__annotations__[parameters[i]], parameters[i])
                else:
                    self.add_input(Any, parameters[i])

        except ValueError as e:
            self.add_input(Any, "args")
        except TypeError as e:
            pass
        super().generate_sockets(sockets_data)

    def update(self):
        if not len(self.inputs[1].edges):
            return
        new_type = self.inputs[1].edges[0].start_socket.data_type
        methods = [method for method in dir(new_type)
                   if hasattr(new_type, method) and
                   callable(getattr(new_type, method))]

        text = self.combo_box.currentText()
        self.combo_box.clear()
        self.combo_box.addItems(methods)
        if text != '':
            self.combo_box.setCurrentText(text)
            self.generate_sockets()

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)

        if new_edge.end_socket == self.inputs[1]:
            self.update()
