import pygame as pg
from element import Element


class Node:
    def __init__(self, surf, font, size, position, inds, color=(255, 255, 255), term=False, connected=None):
        if connected is None:
            connected = [0, 0, 0, 0]
        self.color = color
        self.term = term
        self.connected = connected
        self.surf = surf
        self.font = font
        self.rect = pg.Rect(*position, size, size)
        self.inds = inds
        self.graph = Element.element_dict["graph"]

    def is_adj(self, node):
        if abs(node.inds[0] - self.inds[0]) + abs(node.inds[1] - self.inds[1]) == 1:
            return (node.inds[0] - self.inds[0]) + 2*(node.inds[1] - self.inds[1])
        return None

    def draw(self):
        pg.draw.rect(self.surf, (50, 50, 50), self.rect, width=2)
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and self.graph.path and not (self.term and self.color != self.graph.path[0].color) and not Element.element_dict["win_screen"].show:
            if not any(self.connected) and not (len(self.graph.path) > 1 and self.graph.path[-1].term):
                prev = self.graph.path[-1]
                adj = self.is_adj(prev)
                if adj is not None:
                    self.color = prev.color
                    if adj == -1:
                        prev.connected[1] = 1
                        self.connected[3] = 1
                    elif adj == 1:
                        prev.connected[3] = 1
                        self.connected[1] = 1
                    elif adj == -2:
                        prev.connected[2] = 1
                        self.connected[0] = 1
                    else:
                        prev.connected[0] = 1
                        self.connected[2] = 1
                    self.graph.path.append(self)
            else:
                if self in self.graph.path[:-1]:
                    ind = self.graph.path.index(self)

                    for node in self.graph.path[ind+1:]:
                        node.connected = [0, 0, 0, 0]
                        if not node.term:
                            node.color = (255, 255, 255)
                    self.graph.path = self.graph.path[:ind+1]
                    self.connected = [0, 0, 0, 0]
                    if len(self.graph.path) > 1:
                        prev = self.graph.path[-2]
                        adj = self.is_adj(prev)
                        if adj is not None:
                            self.color = prev.color
                            if adj == -1:
                                prev.connected[1] = 1
                                self.connected[3] = 1
                            elif adj == 1:
                                prev.connected[3] = 1
                                self.connected[1] = 1
                            elif adj == -2:
                                prev.connected[2] = 1
                                self.connected[0] = 1
                            else:
                                prev.connected[0] = 1
                                self.connected[2] = 1
                            self.graph.path.append(self)

        pipe_rect_w = self.rect.w / 2
        if self.connected[0]:
            pipe_rect = pg.Rect(self.rect.x + (self.rect.w/2) - (pipe_rect_w/2), self.rect.y, pipe_rect_w, (self.rect.h/2) + (pipe_rect_w/2))
            pg.draw.rect(self.surf, self.color, pipe_rect)
        if self.connected[1]:
            pipe_rect = pg.Rect(self.rect.x + self.rect.w/2 - pipe_rect_w/2, self.rect.y + (self.rect.h/2) - (pipe_rect_w/2), (self.rect.w/2) + pipe_rect_w/2, pipe_rect_w)
            pg.draw.rect(self.surf, self.color, pipe_rect)
        if self.connected[2]:
            pipe_rect = pg.Rect(self.rect.x + (self.rect.w/2) - (pipe_rect_w/2), self.rect.y + self.rect.h/2 - pipe_rect_w/2, pipe_rect_w, (self.rect.h/2) + pipe_rect_w/2)
            pg.draw.rect(self.surf, self.color, pipe_rect)
        if self.connected[3]:
            pipe_rect = pg.Rect(self.rect.x, self.rect.y + (self.rect.h/2) - (pipe_rect_w/2), (self.rect.w/2) + (pipe_rect_w/2), pipe_rect_w)
            pg.draw.rect(self.surf, self.color, pipe_rect)

        if self.term:
            circ_pos = (self.rect.x + (self.rect.w/2), self.rect.y + (self.rect.h/2))
            pg.draw.circle(self.surf, self.color, circ_pos, (self.rect.w/2)-10)

    def event(self, event):
        if Element.element_dict["win_screen"].show:
            return
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            for path in self.graph.all_paths:
                if self in path:
                    self.graph.path = path.copy()
                    self.graph.all_paths.remove(path)
            if self.term:
                for path in self.graph.all_paths:
                    if self in path:
                        for node in path:
                            node.connected = [0, 0, 0, 0]
                for node in self.graph.path:
                    node.connected = [0, 0, 0, 0]
                self.graph.path = [self]

        elif event.type == pg.MOUSEBUTTONUP and self.graph.path:
            self.graph.all_paths.append(self.graph.path.copy())
            self.graph.path = []
            self.graph.check_win()


