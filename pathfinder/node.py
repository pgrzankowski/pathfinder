import math


class Node:
    def __init__(self, pos, start_pos, end_pos, map_array):
        self._pos = pos
        self._value = map_array[pos[1]][pos[0]]
        self.G = self.get_distance(start_pos)
        self.H = self.get_distance(end_pos)
        self.F = self.G + self.H
        self._connection = None
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._MAX_WIDTH = len(map_array[0])
        self._MAX_HEIGHT = len(map_array)

    def get_pos(self):
        return self._pos

    def set_g(self, new_G):
        self.G = new_G

    def set_h(self, new_H):
        self.H = new_H

    def set_connection(self, node_base):
        self._connection = node_base

    def get_connections(self):
        return self._connection

    def get_value(self):
        return self._value

    def walkable(self):
        return False if self._value else True

    def neighbors(self):
        neighbors_list = []
        deltas = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in deltas:
            nx, ny = self._pos[0] + dx, self._pos[1] + dy
            if 0 <= nx < self._MAX_WIDTH and 0 <= ny < self._MAX_HEIGHT:
                neighbors_list.append((nx, ny))
        return neighbors_list

    def get_distance(self, other_pos):
        x1, y1 = self._pos
        x2, y2 = other_pos
        d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return d
