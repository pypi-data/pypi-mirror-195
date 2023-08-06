from typing import Any
import inspect
from editor.config import register_node
from editor.nodes.event import EventNode
from editor.core.models.socket_contents.socket_text_content import SocketTextContent
from editor.core.views.socket_contents.socket_combo_box_content_widget import SocketComboBoxContentWidget

@register_node()
class CopySignatureNode(EventNode):
    title = "Copy Signature"
    category = "Default"
    color = "#FF611161"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [type, str, *input_types], output_types)
        self.inputs[0].updateName("class")
        self.inputs[1].content = SocketTextContent(self.inputs[1], SocketComboBoxContentWidget)
        self.combo_box = self.inputs[1].content.graphics.combo_box

        self.graphics.update_sockets_pos()
        self.add_signals({self.combo_box.textActivated: self.on_combo_box_item_change})

    def on_combo_box_item_change(self, event):
        self.generate_sockets()
        for node in self.handle.get_connected_nodes():
            node.update()

    def get_value(self, index=0):
        if self.overriden_args is not None and index <= len(self.overriden_args):
            return self.overriden_args[index-1]
        return None

    def generate_sockets(self, sockets_data=None):
        for i in range(len(self.outputs) - 1, 0, -1):
            self.scene.graphics.removeItem(self.outputs[i].graphics)
            self.outputs.pop(i)

        class_item = self.get_input_value(0)
        if class_item is None:
            return

        item = self.find_item(class_item, self.combo_box.currentText())

        description = item.__doc__
        if description:
            self.graphics.setToolTip(description.strip())

        try:
            parameters = list(inspect.signature(item).parameters.keys())

            """ Updating signature of the overriden function """

            async def overriden_function(*args, **kwargs):
                self.overriden_args = args
                for index in range(len(args)):
                    self.outputs[index+1].updateDataType(args[index].__class__)
                await super(CopySignatureNode, self).execute()

            param_objects = []
            for name in parameters:
                param_objects.append(inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD))
            overriden_function.__signature__ = \
                inspect.signature(overriden_function).replace(parameters=param_objects)
            self.execute = overriden_function

            for i in range(len(parameters)):
                if hasattr(item, '__annotations__') and item.__annotations__.__contains__(parameters[i]):
                    self.add_output(item.__annotations__[parameters[i]], parameters[i])
                else:
                    self.add_output(Any, parameters[i])

        except ValueError as e:
            self.add_output(Any, "args")
        except TypeError as e:
            pass
        super().generate_sockets(sockets_data)

    def on_edge_changed(self, new_edge):
        super().on_edge_changed(new_edge)
        if new_edge.end_socket == self.inputs[0]:
            input_value = self.get_input_value(0)
            methods = [method for method in dir(input_value) if callable(getattr(input_value, method))]
            if input_value is not None:
                text = self.combo_box.currentText()
                self.combo_box.clear()
                self.combo_box.addItems(methods)
                if text != '':
                    self.combo_box.setCurrentText(text)
                    self.generate_sockets()
