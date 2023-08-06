from collections import OrderedDict
from editor.core.models.node import Node
from editor.core.models.edge import Edge
from PyQt5.QtCore import QPoint

DEBUG = False


class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, cut=False):
        if DEBUG: print("-- COPY TO CLIPBOARD ---")

        sel_nodes, sel_edges, sel_sockets = [], [], {}

        # sort edges and nodes
        edges = []
        for item in self.scene.selectedItems():
            if isinstance(item, Node):
                sel_nodes.append(item.serialize())
                for socket in (item.inputs + item.outputs):
                    sel_sockets[socket.id] = socket
                    for edge in socket.edges:
                        if edge in edges:
                            continue
                        edges.append(edge)

        # debug
        if DEBUG:
            print("  NODES\n      ", sel_nodes)
            print("  EDGES\n      ", edges)
            print("  SOCKETS\n     ", sel_sockets)

        # make final list of edges
        edges_final = []
        for edge in edges:
            edges_final.append(edge.serialize())

        if DEBUG: print("our final edge list:", edges_final)


        data = OrderedDict([
            ('nodes', sel_nodes),
            ('edges', edges_final),
        ])

        if cut:
            self.scene.getView().deleteSelected()
            self.scene.history.storeHistory("Cut out elements from scene", setModified=True)

        return data

    def deserializeFromClipboard(self, data):
        self.scene.loaded = False
        hashmap = {}

        # calculate mouse pointer - scene position
        mouse_scene_pos = self.scene.getView().last_scene_mouse_position

        # calculate selected objects bbox and center
        min_x, max_x, min_y, max_y = self.scene.scene_width, -self.scene.scene_width, \
            self.scene.scene_height, -self.scene.scene_height

        new_nodes = []
        # create each node
        for node_data in data['nodes']:
            new_node = self.scene.getNodeClassFromData(node_data)(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)
            new_nodes.append(new_node)

        for node in new_nodes:
            x, y = node.pos.x() + node.graphics.width//2, node.pos.y() + node.graphics.height//2
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        bbox_center_x = (min_x + max_x) // 2
        bbox_center_y = (min_y + max_y) // 2

        self.scene.graphics.clearSelection()

        # readjust the new node's position
        for node in new_nodes:
            new_pos_x = node.pos.x() - bbox_center_x + mouse_scene_pos.x()
            new_pos_y = node.pos.y() - bbox_center_y + mouse_scene_pos.y()
            node.graphics.setPos(QPoint(int(new_pos_x), int(new_pos_y)))
            node.graphics.setSelected(True)

        # # create each edge
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        # store history
        self.scene.history.storeHistory("Pasted elements in scene", setModified=True)
        self.scene.loaded = True