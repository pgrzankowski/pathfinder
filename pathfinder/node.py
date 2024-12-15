from typing import Self

class Node:
    def __init__(self, pos, map_array):
        self._pos = pos
        self._g = float("inf")
        self._h = 0
        self._f = self._g
        self._connection = None
        self._walkable = self._calculate_walkable(map_array)
        self._neighbors = self._calculate_neighbors(map_array)

    @property
    def pos(self):
        return self._pos

    @property
    def value(self):
        return self._value

    @property
    def g(self):
        return self._g

    @property
    def h(self):
        return self._h

    @property
    def f(self):
        return self._f

    @property
    def connection(self):
        return self._connection

    @property
    def walkable(self):
        return self._walkable

    @property
    def neighbors(self):
        return self._neighbors

    @g.setter
    def g(self, g):
        self._g = g
        self._f = self._g + self._h

    @h.setter
    def h(self, h):
        self._h = h
        self._f = self._g + self._h

    @connection.setter
    def connection(self, node_base):
        self._connection = node_base

    def _calculate_walkable(self, map_array):
        value = map_array[self._pos[1]][self._pos[0]]
        return False if value else True

    def _calculate_neighbors(self, map_array):
        max_width = len(map_array[0])
        max_height = len(map_array)
        neighbors_list = []
        deltas = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in deltas:
            nx, ny = self._pos[0] + dx, self._pos[1] + dy
            if 0 <= nx < max_width and 0 <= ny < max_height:
                neighbors_list.append((nx, ny))
        return neighbors_list

    def get_distance(self, other: Self):
        # Manhattan distance
        x1, y1 = self._pos
        x2, y2 = other.pos
        d = abs(x2 - x1) + abs(y2 - y1)
        return d
