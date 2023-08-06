import builtins
from collections import OrderedDict
from editor.core.models.serializable import Serializable
from editor.core.models.data_types import EXEC, HANDLE
from editor.core.models.socket import Socket
from editor.core.views.node import NodeGraphics

DEBUG = False


class Node(Serializable):
    category = "Abstract"
    title = "Node"
    color = "#FF611111"

    def __init__(self, scene, title="Undefined Node", input_types=tuple(), output_types=tuple(), give_handle=False):
        super().__init__()
        self.scene = scene
        self.title = title

        self.handle = None

        self.inputs = []
        self.outputs = []
        self.value = None
        self.connections = {}

        self.graphics = NodeGraphics(self)
        self.content = None

        if give_handle:
            self.handle = Socket(node=self, name='', index=0, data_type=HANDLE,
                                 multi_edges=True, is_input=False)

        self.scene.addItem(self)
        self.init_sockets(input_types, output_types)

    def init_sockets(self, input_types, output_types, reset=True):
        """ Create sockets for inputs and outputs"""
        if reset:
            self.clear_sockets()
        for input_type in input_types:
            self.add_input(input_type, update_socket_graphics=False)
        for output_type in output_types:
            self.add_output(output_type, update_socket_graphics=False)
        self.graphics.update_sockets_pos()

    def add_signals(self, connections):
        for key in connections.keys():
            key.connect(connections[key])
        self.connections = connections

    def clear_sockets(self):
        if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
            for socket in (self.inputs + self.outputs):
                self.scene.graphics.removeItem(socket.graphics)
            self.inputs = []
            self.outputs = []

    def add_input(self, input_type, name="", update_socket_graphics=True):
        multi_edges = input_type == EXEC
        index = len(self.inputs)
        socket = Socket(node=self, name=name, index=index, data_type=input_type,
                        multi_edges=multi_edges, is_input=True)
        self.inputs.append(socket)
        if update_socket_graphics:
            self.graphics.update_sockets_pos()

    def add_output(self, output_type, name="", update_socket_graphics=True):
        multi_edges = not output_type == EXEC
        index = len(self.outputs)
        socket = Socket(node=self, name=name, index=index, data_type=output_type,
                        multi_edges=multi_edges, is_input=False)
        self.outputs.append(socket)
        if update_socket_graphics:
            self.graphics.update_sockets_pos()

    def remove_socket(self, socket):
        if socket in self.inputs:
            self.scene.graphics.removeItem(socket.graphics)
            self.inputs.remove(socket)

    def has_input(self, name):
        for input_socket in self.inputs:
            if input_socket.name == name:
                return True
        return False

    def on_edge_changed(self, edge):
        pass

    def __str__(self):
        return self.title

    @property
    def pos(self):
        return self.graphics.pos()

    def remove(self):
        sockets = self.inputs + self.outputs
        if self.handle:
            sockets.append(self.handle)
        self.scene.removeItem(self)
        self.graphics = None
        self.on_edge_changed = lambda *args: None
        for socket in sockets:
            for edge in socket.edges:
                edge.remove()
        for signal in self.connections.keys():
            signal.disconnect(self.connections[signal])

    def get_value(self, index=0):
        return self.value

    def update(self):
        pass

    async def execute(self):
        await self.execute_child(0)

    async def execute_child(self, index):
        if len(self.outputs) <= index or self.outputs[index].data_type != EXEC:
            return
        children_nodes = self.get_children_nodes(index)
        for child_node in children_nodes:
            await child_node.execute()

    def get_children_nodes(self, index):
        if index >= len(self.outputs):
            return []

        other_nodes = []
        for edge in self.outputs[index].edges:
            other_node = edge.end_socket.node
            other_nodes.append(other_node)
        return other_nodes

    def get_input_socket(self, index=0):
        if len(self.inputs) > index and len(self.inputs[index].edges):
            edge = self.inputs[index].edges[0]
            return edge.start_socket

    def get_input_node(self, index=0):
        input_socket = self.get_input_socket(index)
        if input_socket is not None:
            return input_socket.node
        return None

    def get_input_data_type(self, index=0):
        if index >= len(self.inputs):
            return None
        return self.inputs[index].data_type

    def get_input_value(self, index=0):
        socket = self.get_input_socket(index)
        if socket is None:
            input_content = self.inputs[index].content
            if input_content:
                return input_content.get_value()
            return None
        node = socket.node
        if socket.data_type == HANDLE:
            return node.execute
        else:
            return node.get_value(socket.index)

    def get_parent_item(self):
        return

    def find_item(self, parent_item, name=None):
        if parent_item is None or isinstance(parent_item, int):
            return
        if name is None:
            name = self.title
        hierarchy = name.split('.')
        item = None
        for level in hierarchy:
            if item:
                if level in item.__dict__:
                    item = item.__dict__[level]
                else:
                    return
            else:
                if level == 'builtins':
                    item = builtins
                    continue
                if hasattr(parent_item, level):
                    try:
                        item = getattr(parent_item, level)
                        continue
                    except TypeError:
                        pass
                if hasattr(parent_item, '__dict__'):
                    dictionary = parent_item.__dict__
                    if dictionary.__contains__(level):
                        item = dictionary[level]
                        continue
                if not hasattr(parent_item, 'mro'):
                    parent_item = parent_item.__class__
                if hasattr(parent_item, 'mro'):
                    for cls in parent_item.mro():
                        dictionary = cls.__dict__
                        if dictionary.__contains__(level):
                            item = dictionary[level]
                            break
        return item

    def generate_sockets(self, sockets_data=None):
        self.graphics.refresh_shape()

    def serialize(self):
        serialized_inputs, serialized_outputs = [], []
        for socket in self.inputs:
            serialized_inputs.append(socket.serialize())
        for socket in self.outputs:
            serialized_outputs.append(socket.serialize())
        serialized_data = [
            ('id', self.id),
            ('class', self.__class__.__name__),
            ('title', self.title),
            ('pos_x', self.graphics.scenePos().x()),
            ('pos_y', self.graphics.scenePos().y()),
        ]
        if len(serialized_inputs):
            serialized_data.append(('inputs', serialized_inputs))
        if len(serialized_outputs):
            serialized_data.append(('outputs', serialized_outputs))
        if self.handle:
            serialized_data.append(('handle', [self.handle.serialize()]))
        if self.content:
            serialized_data.append(('content', self.content.serialize()))
        return OrderedDict(serialized_data)

    def deserialize(self, data, hashmap=None, restore_id=True):
        from PyQt5.QtCore import QPoint
        super().deserialize(data, hashmap, restore_id)
        title = data['title']
        if title != '':
            self.title = title

        self.graphics.setPos(QPoint(int(data['pos_x']), int(data['pos_y'])))
        inputs_data = data['inputs'] if 'inputs' in data else None
        outputs_data = data['outputs'] if 'outputs' in data else None
        self.generate_sockets((inputs_data, outputs_data))

        if inputs_data:
            for socket in self.inputs:
                socket.deserialize(inputs_data, hashmap, restore_id)
        if outputs_data:
            for socket in self.outputs:
                socket.deserialize(outputs_data, hashmap, restore_id)

        if self.handle is not None and 'handle' in data:
            self.handle.deserialize(data['handle'], hashmap, restore_id)

        if self.content is not None:
            self.content.deserialize(data['content'], hashmap)

        self.graphics.update_title()

        return True
