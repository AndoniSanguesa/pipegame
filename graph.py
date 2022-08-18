from element import Element
from node import Node
from random import random
from random import choice


class Graph(Element):
    def __init__(self, surf, font, size=(10,10)):
        super().__init__("graph")
        self.surf = surf
        self.font = font
        self.nodes = []
        self.size = size
        self.colors = []
        self.path = []
        self.all_paths = []

        self.generate_puzzle()

    def get_len(self, node, direction=-1):
        tmp_connected = node.connected.copy()
        if direction != -1:
            tmp_connected[direction-2] = 0
        if all([c == 0 for c in tmp_connected]):
            return 1
        new_direction = tmp_connected.index(1)
        inds = node.inds
        con = tmp_connected
        new_node = list(filter(lambda n: n.inds == (inds[0] + con[1] - con[3], inds[1] + con[2] - con[0]), self.nodes))[0]

        return 1 + self.get_len(new_node, new_direction)

    def generate_puzzle(self, size=None):
        size = size if size is not None else self.size
        self.update_nodes(size)
        terms = []
        for node in self.nodes[:size[0]]:
            terms.append(node)
            node.term = True
            new_color = (random()*255, random()*255, random()*255)
            node.connected = [0, 0, 1, 0]
            node.color = new_color
            self.colors.append(new_color)
        for ind in range(size[0]):
            node = self.nodes[-1-ind]
            terms.append(node)
            node.term = True
            node.color = self.colors[-1-ind]
            node.connected = [1, 0, 0, 0]

        for node in self.nodes[size[0]:-size[0]]:
            node.connected = [1, 0, 1, 0]

        for _ in range(5000):
            node_to_modify = choice(terms)
            while self.get_len(node_to_modify) == 3 or len(list(filter(lambda x: x.is_adj(node_to_modify), terms))) == 0:
                node_to_modify = choice(terms)

            adj_terms = list(filter(lambda x: x.is_adj(node_to_modify), terms))
            adj_to_move = choice(adj_terms)

            adj_move_dir = adj_to_move.is_adj(node_to_modify)

            ntm_inds = node_to_modify.inds

            if node_to_modify.connected[0] == 1:
                new_term = list(filter(lambda n: n.inds == (ntm_inds[0], ntm_inds[1] - 1), self.nodes))[0]
                node_to_modify.connected = [0, 0, 0, 0]
                new_term.connected[2] = 0
            elif node_to_modify.connected[1] == 1:
                new_term = list(filter(lambda n: n.inds == (ntm_inds[0] + 1, ntm_inds[1]), self.nodes))[0]
                node_to_modify.connected = [0, 0, 0, 0]
                new_term.connected[3] = 0
            elif node_to_modify.connected[2] == 1:
                new_term = list(filter(lambda n: n.inds == (ntm_inds[0], ntm_inds[1] + 1), self.nodes))[0]
                node_to_modify.connected = [0, 0, 0, 0]
                new_term.connected[0] = 0
            else:
                new_term = list(filter(lambda n: n.inds == (ntm_inds[0] - 1, ntm_inds[1]), self.nodes))[0]
                node_to_modify.connected = [0, 0, 0, 0]
                new_term.connected[1] = 0

            new_term.color = node_to_modify.color
            new_term.term = True

            if adj_move_dir == -1:
                adj_to_move.connected[3] = 1
                node_to_modify.connected[1] = 1
            elif adj_move_dir == 1:
                adj_to_move.connected[1] = 1
                node_to_modify.connected[3] = 1
            elif adj_move_dir == -2:
                adj_to_move.connected[0] = 1
                node_to_modify.connected[2] = 1
            else:
                adj_to_move.connected[2] = 1
                node_to_modify.connected[0] = 1

            adj_to_move.term = False
            node_to_modify.color = adj_to_move.color
            adj_to_move.color = (255, 255, 255)
            terms.remove(adj_to_move)

            terms.append(new_term)

        for node in self.nodes:
            node.connected = [0, 0, 0, 0]



    def update_nodes(self, size):
        x_offset = 0
        y_offset = 0
        x_node_size = self.surf.get_width() / size[0]
        y_node_size = self.surf.get_height() / size[1]

        if x_node_size < y_node_size:
            node_size = x_node_size
            y_offset = (self.surf.get_height() - size[1] * node_size) / 2
        else:
            node_size = y_node_size
            x_offset = (self.surf.get_width() - size[0]*node_size)/2

        self.nodes = [Node(self.surf, self.font, node_size, (x_ind*node_size + x_offset, y_ind*node_size + y_offset), (x_ind, y_ind)) for y_ind in range(size[1]) for x_ind in range(size[0])]

    def check_win(self):
        if all([any(node.connected) for node in self.nodes]):
            Element.element_dict["win_screen"].show = True

    def draw(self):
        for node in self.nodes:
            node.draw()

    def event(self, event):
        for node in self.nodes:
            node.event(event)
