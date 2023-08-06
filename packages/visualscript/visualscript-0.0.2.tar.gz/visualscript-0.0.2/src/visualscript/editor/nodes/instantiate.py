from typing import Any
import inspect, asyncio
from editor.config import register_node
from editor.nodes.executable import ExecutableNode

@register_node()
class InstantiateNode(ExecutableNode):
    title = "Instantiate"
    category = "Default"
    color = "#FF611161"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, title, [type, *input_types], [Any, *output_types])
        self.inputs[1].updateName("class")

    def get_parent_item(self):
        return self.get_input_value(1)

    def generate_sockets(self, sockets_data=None):
        trimmed_edges = []

        if sockets_data:
            for i in range(2, len(sockets_data[0])):
                self.add_input(Any, sockets_data[0][i]['name'])
        if self.scene.loaded:
            trimmed_edges = self.reset_inputs()

        item = self.get_parent_item()
        if item is None:
            return
        self.outputs[1].updateDataType(item)

        description = item.__doc__
        if description:
            self.graphics.setToolTip(description.strip())

        try:
            item_init = item.__init__

            parameters = inspect.signature(item).parameters
            parameter_names = list(parameters.keys())

            first_optional_parameter = len(parameter_names)
            if hasattr(item_init, '__defaults__') and item_init.__defaults__ is not None:
                first_optional_parameter -= len(item_init.__defaults__)

            for i in range(len(parameter_names)):
                default_value = ''
                if i >= first_optional_parameter:
                    default_value = '=' + str(item_init.__defaults__[i - first_optional_parameter])
                if not self.has_input(parameter_names[i] + default_value) and not self.has_input(parameter_names[i]):
                    if hasattr(item_init, '__annotations__') and parameter_names[i] in item_init.__annotations__:
                        self.add_input(item_init.__annotations__[parameter_names[i]], parameter_names[i] + default_value)
                    else:
                        socket_name = parameter_names[i] + default_value
                        if parameters[parameter_names[i]].kind == inspect.Parameter.VAR_POSITIONAL:
                            socket_name = '*' + socket_name
                        elif parameters[parameter_names[i]].kind == inspect.Parameter.VAR_KEYWORD:
                            socket_name = '**' + socket_name
                        if not self.has_input(socket_name):
                            self.add_input(Any, socket_name)
                elif hasattr(item_init, '__annotations__') and parameter_names[i] in item_init.__annotations__:
                    self.inputs[i + 2].updateDataType(item_init.__annotations__[parameter_names[i]])
        except ValueError as e:
            pass
        except TypeError as e:
            pass

        # restoring edges that were connected before regenerating inputs
        for i in range(len(trimmed_edges)):
            if not trimmed_edges[i]:
                continue
            if i >= len(self.inputs) - 2:
                trimmed_edges[i].remove()
            else:
                trimmed_edges[i].end_socket = self.inputs[i + 2]

        super().generate_sockets(sockets_data)

    async def execute(self):
        # item = self.get_input_value(1)
        # if not item:
        #     return
        # item_init = item.__init__
        # input_values = [None] * (len(self.inputs) - 2)
        # if hasattr(item_init, '__defaults__') and item_init.__defaults__:
        #     for i in range(len(item_init.__defaults__)):
        #         input_values[-1 - i] = item_init.__defaults__[-1 - i]
        #
        # for i in range(2, len(self.inputs)):
        #     if len(self.inputs[i].edges):
        #         input_values[i - 2] = self.get_input_value(i)

        parent_item = self.get_parent_item()
        if not parent_item:
            return

        item = parent_item.__init__

        args, kwargs = [], {}

        input_values = [None] * (len(self.inputs) - 2)
        if hasattr(item, '__defaults__') and item.__defaults__:
            for i in range(len(item.__defaults__)):
                input_values[-1 - i] = item.__defaults__[-1 - i]

        for i in range(2, len(self.inputs)):
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
                    input_values[i - 2] = self.get_input_value(i)

        if asyncio.iscoroutinefunction(item):
            # temporarily replacing async __init__ with synchronous version
            # due to requirement that it needs to return None
            async_init = item
            parent_item.__init__ = self.make_synchronous_init(item)
            self.value = parent_item(*input_values, *args, **kwargs)
            parent_item.__init__ = async_init
        else:
            self.value = self.get_parent_item()(*input_values, *args, **kwargs)
            await super().execute()

    def make_synchronous_init(self, function):
        def __init__(*args, **kwargs):
            task = asyncio.create_task(function(*args, **kwargs))
            task.add_done_callback(self.postponed_execute)
        return __init__

    def postponed_execute(self, task):
        task.remove_done_callback(self.postponed_execute)
        asyncio.create_task(super().execute())

    def reset_inputs(self):
        self.outputs[1].updateDataType(Any)
        trimmed_edges = []
        for i in range(2, len(self.inputs)):
            if len(self.inputs[i].edges):
                trimmed_edges.append(self.inputs[i].edges[0])
            else:
                trimmed_edges.append(None)
            self.scene.graphics.removeItem(self.inputs[i].graphics)
        self.inputs = self.inputs[:2]
        self.graphics.refresh_shape()
        return trimmed_edges

    def on_edge_changed(self, edge):
        super().on_edge_changed(edge)
        if not edge.is_valid() and not self.get_input_value(1):
            self.reset_inputs()
        elif edge.end_socket == self.inputs[1]:
            self.generate_sockets()

    def update(self):
        self.generate_sockets()
