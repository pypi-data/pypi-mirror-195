from editor.core.models.serializable import Serializable


class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None):
        super().__init__()
        self.scene = scene

        self._start_socket = None
        self._end_socket = None

        self.start_socket = start_socket
        self.end_socket = end_socket
        if self.end_socket and self.end_socket.content:
            self.end_socket.content.on_connect()

        from editor.core.views.edge import EdgeGraphics
        self.graphics = EdgeGraphics(self)
        self.scene.addItem(self)

        if start_socket and end_socket:
            self.start_socket.node.on_edge_changed(self)
            self.end_socket.node.on_edge_changed(self)

    def get_other_socket(self, known_socket):
        if known_socket == self.end_socket:
            return self.start_socket
        if known_socket == self.start_socket:
            return self.end_socket
        return None

    @property
    def start_socket(self): return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

        self._start_socket = value
        if self._start_socket:
            self._start_socket.addEdge(self)

    @property
    def end_socket(self): return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)

        self._end_socket = value
        if self._end_socket:
            self._end_socket.addEdge(self)

    @property
    def edge_type(self): return self.start_socket.data_type if self.start_socket else None

    def is_valid(self):
        return self.start_socket is not None and self.end_socket is not None

    def remove(self, trigger_events=True):
        self.scene.removeItem(self)

        start_node, end_node = None, None
        if self.start_socket:
            start_node = self.start_socket.node
            self.start_socket = None

        if self.end_socket:
            end_node = self.end_socket.node
            self.end_socket = None

        if trigger_events:
            if start_node:
                start_node.on_edge_changed(self)
            if end_node:
                end_node.on_edge_changed(self)

    def serialize(self):
        if not self.start_socket or not self.end_socket:
            return {}

        from collections import OrderedDict
        return OrderedDict([
            ('id', self.id),
            ('start_socket', self.start_socket.id),
            ('end_socket', self.end_socket.id),
        ])

    def deserialize(self, data, hashmap=None, restore_id=True):
        super().deserialize(data, hashmap, restore_id)
        if data['start_socket'] and data['start_socket'] in hashmap:
            self.start_socket = hashmap[data['start_socket']]
            self.start_socket.node.on_edge_changed(self)
        else:
            self.remove()
            return
        if data['end_socket'] and data['end_socket'] in hashmap:
            self.end_socket = hashmap[data['end_socket']]
            self.end_socket.node.on_edge_changed(self)
        else:
            self.remove()
            return

        self.graphics.updatePositions()

        if self.end_socket and self.end_socket.content:
            self.end_socket.content.on_connect()
