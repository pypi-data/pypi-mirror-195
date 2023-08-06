from typing import Any
import inspect
import builtins
from editor.config import register_node
from editor.nodes.executable import ExecutableNode

@register_node()
class ConstructorNode(ExecutableNode):
    title = "Construct"
    category = "Abstract"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, output_types)
        self.graphics.change_colors("#FF611161")
        self.graphics.setToolTip("Constructor")

    def generate_sockets(self, sockets_data=None):
        item = None
        hierarchy = self.title.split('.')
        for level in hierarchy:
            if item:
                item = item.__dict__[level]
            else:
                if self.scene.module and self.scene.module.__dict__.__contains__(level):
                    item = self.scene.module.__dict__[level]
                elif level == 'builtins':
                    item = builtins

        self.object_class = self.get_class()
        description = self.object_class.__doc__
        if description:
            self.graphics.setToolTip(description.strip())
        self.add_output(self.object_class)

        try:
            parameters = list(inspect.signature(item).parameters.keys())
            if parameters.__contains__("self"):
                parameters.pop(0)
            for i in range(len(parameters)):
                if hasattr(item, "__code__"):
                    parameter_name = item.__code__.co_varnames[i]
                    if item.__annotations__.__contains__(parameter_name):
                        self.add_input(item.__annotations__[parameter_name], item.__code__.co_varnames[i])
                    else:
                        self.add_input(Any, item.__code__.co_varnames[i])
                else:
                    self.add_input(Any, parameters[i])
        except ValueError as e:
            self.add_input(Any, "args")
        super().generate_sockets(sockets_data)

    async def execute(self):
        input_values = []
        for i in range(1, len(self.inputs)):
            # value = None
            input_node = self.get_input_node(i)
            if input_node:
                value = input_node.get_value()
                input_values.append(value)

        try:
            self.value = self.object_class(*input_values)
            await super().execute()
        except Exception as e:
            from editor.core.utils import dumpException
            dumpException(e)


    def get_class(self):
        module = self.scene.module

        if not module:
            return None

        hierarchy = self.title.split('.')

        item = None
        for level in hierarchy:
            if item:
                item = item.__dict__[level]
            else:
                if module.__dict__.__contains__(level):
                    item = module.__dict__[level]
                elif level == 'builtins':
                    item = builtins
        return item