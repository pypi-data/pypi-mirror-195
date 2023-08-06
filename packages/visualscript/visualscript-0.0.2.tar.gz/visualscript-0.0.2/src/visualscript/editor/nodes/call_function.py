from typing import Any
from collections.abc import Iterable
import asyncio
import inspect
from editor.config import register_node
from editor.nodes.executable import ExecutableNode
from editor.core.models.data_types import WILDCARD

@register_node()
class CallFunctionNode(ExecutableNode):
    """Function call node. Tries to execute a function from scene's
module scope with connected pins as named arguments"""

    title = "Call Function"
    color = "#FF111161"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, input_types, [Any, *output_types])
        self.graphics.change_colors()
        self.inputs_first_index = 1
        self.add_signals({self.scene.getView().updateModule: self.reset_inputs})

    def get_parent_item(self):
        return self.scene.module

    def reset_inputs(self, module_key=None):
        if module_key == self.title or module_key is None:
            trimmeded_edges = []
            for i in range(self.inputs_first_index, len(self.inputs)):
                if len(self.inputs[i].edges):
                    trimmeded_edges.append(self.inputs[i].edges[0])
                else:
                    trimmeded_edges.append(None)
                self.scene.graphics.removeItem(self.inputs[i].graphics)
            self.inputs = self.inputs[:self.inputs_first_index]
            self.graphics.refresh_shape()
            self.generate_sockets()
            for i in range(len(trimmeded_edges)):
                if trimmeded_edges[i]:
                    if i >= len(self.inputs) - self.inputs_first_index:
                        trimmeded_edges[i].remove()
                    else:
                        trimmeded_edges[i].end_socket = self.inputs[i + self.inputs_first_index]

    def generate_sockets(self, sockets_data=None):
        if sockets_data:
            for i in range(self.inputs_first_index, len(sockets_data[0])):
                self.add_input(WILDCARD, sockets_data[0][i]['name'])

        item = self.find_item(self.get_parent_item())

        if item is None:
            super().generate_sockets()
            return

        if hasattr(item, '__doc__') and item.__doc__:
            self.graphics.setToolTip(item.__doc__.strip().replace('\n\n', '\n'))

        if hasattr(item, '__annotations__') and item.__annotations__.__contains__('return'):
            self.outputs[1].updateDataType(item.__annotations__['return'])

        try:
            parameters = inspect.signature(item).parameters
            parameter_names = list(parameters.keys())

            first_optional_parameter = len(parameter_names)
            if hasattr(item, '__defaults__') and item.__defaults__ is not None:
                first_optional_parameter -= len(item.__defaults__)
            for i in range(len(parameter_names)):
                if parameters[parameter_names[i]].kind == inspect.Parameter.KEYWORD_ONLY:
                    if not self.has_input('**kwargs'):
                        self.add_input(WILDCARD, '**kwargs')
                    continue
                default_value = ''
                if not self.has_input(parameter_names[i]) and i >= self.inputs_first_index - 1:
                    if i >= first_optional_parameter:
                        default_value = '=' + str(item.__defaults__[i - first_optional_parameter])
                    if hasattr(item, '__annotations__') and item.__annotations__.__contains__(parameter_names[i]):
                        self.add_input(item.__annotations__[parameter_names[i]], parameter_names[i] + default_value)
                    else:
                        socket_name = parameter_names[i] + default_value
                        if parameters[parameter_names[i]].kind == inspect.Parameter.VAR_POSITIONAL:
                            socket_name = '*' + socket_name
                        elif parameters[parameter_names[i]].kind == inspect.Parameter.VAR_KEYWORD:
                            socket_name = '**' + socket_name
                        if not self.has_input(socket_name):
                            self.add_input(WILDCARD, socket_name)
        except ValueError as e:
            if not self.has_input('*args'):
                self.add_input(WILDCARD, '*args')
            if not self.has_input('**kwargs'):
                self.add_input(WILDCARD, '**kwargs')
        except TypeError as e:
            pass
        super().generate_sockets(sockets_data)

    async def execute(self):
        item = self.find_item(self.get_parent_item())
        args, kwargs = [], {}

        input_values = [None] * (len(self.inputs) - 1)
        if hasattr(item, '__defaults__') and item.__defaults__:
            for i in range(len(item.__defaults__)):
                input_values[-1 - i] = item.__defaults__[-1 - i]

        for i in range(1, len(self.inputs)):
            if self.inputs[i].name.startswith('*'):
                input_values.pop()
            if len(self.inputs[i].edges):
                if self.inputs[i].name.startswith('**'):
                    kwargs = self.get_input_value(i)
                    if not isinstance(kwargs, dict):
                        kwargs = {}
                elif self.inputs[i].name.startswith('*'):
                    args = self.get_input_value(i)
                    if not hasattr(args, '__iter__') or isinstance(args, str) or isinstance(args, type):
                        args = [self.get_input_value(i)]
                else:
                    input_values[i - 1] = self.get_input_value(i)

        try:
            if asyncio.iscoroutinefunction(item):
                self.value = await item(*input_values, *args, **kwargs)
            else:
                self.value = item(*input_values, *args, **kwargs)

        except TypeError as e:
            from editor.core.utils import dumpException
            dumpException(e)
        try:
            await super().execute()
        except Exception as e:
            from editor.core.utils import dumpException
            dumpException(e)
