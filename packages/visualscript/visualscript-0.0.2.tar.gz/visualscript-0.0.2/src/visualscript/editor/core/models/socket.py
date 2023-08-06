from types import NoneType
from typing import Any
from collections import OrderedDict
from editor.core.models.data_types import EXEC, WILDCARD
from editor.core.models.serializable import Serializable
from editor.core.views.socket import SocketGraphics
from editor.core.models.socket_contents.socket_content import SocketContent
from logging import *

DEBUG = False

class Socket(Serializable):
    def __init__(self, node, index=0, data_type=EXEC, multi_edges=True, is_input=False, name=""):
        super().__init__()

        self.node = node
        self.scene = node.scene
        self.name = name
        self.index = index
        if data_type is None or isinstance(data_type, NoneType) or data_type == WILDCARD:
            data_type = Any
        if isinstance(data_type, str):
            try:
                data_type = eval(data_type)
            except:
                opened_class = self.node.graphics.getView().window().module
                data_type = opened_class.__dict__[data_type]
        self.data_type = data_type
        self.is_multi_edges = multi_edges
        self.is_input = is_input
        self.is_output = not self.is_input
        self.edges = []

        if DEBUG:
            print("Socket -- creating with", self.index, "for node", self.node)

        self.content = None
        self.graphics = SocketGraphics(self)

        if name != "":
            self.content = SocketContent(self, name=name)

    def get_connected_nodes(self):
        nodes = []
        for edge in self.edges:
            other_socket = edge.get_other_socket(self)
            if other_socket:
                nodes.append(other_socket.node)
        return nodes

    def updateDataType(self, new_type):
        if new_type is None or new_type == NoneType:
            new_type = Any
        self.data_type = new_type
        self.graphics.setToolTip(str(new_type))

    def updateName(self, new_name):
        self.name = new_name
        if new_name != "":
            if not self.content:
                self.content = SocketContent(self, name=new_name)
            self.content.updateName(new_name)

    def addWidget(self, widget):
        if self.content:
            self.content.addWidget(widget)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)

    def removeAllEdges(self):
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()

    def determineMultiEdges(self, data):
        if 'multi_edges' in data:
            return data['multi_edges']

    def serialize(self):
        res = OrderedDict([
            ('id', self.id),
            ('name', self.name)
        ])
        if self.content:
            seralized_content = self.content.serialize()
            if seralized_content is not None:
                res['content'] = seralized_content
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        if len(data) > self.index:
            data = data[self.index]
            super().deserialize(data, hashmap, restore_id)
            if self.content and 'content' in data:
                self.content.deserialize(data['content'], hashmap)
        return True