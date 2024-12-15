from pathfinder.node import Node
from typing import List


class Pathfinder:
    def __init__(self, map_array, start_pos, end_pos):
        self._map_array = map_array
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._nodes = {}

    def get_node(self, pos):
        if pos not in self._nodes:
            self._nodes[pos] = Node(pos, self._map_array)
        return self._nodes[pos]

    def plan(self, step_callback=None):
        start_node: Node = self.get_node(self._start_pos)
        end_node: Node = self.get_node(self._end_pos)
        start_node.g = 0
        start_node.h = start_node.get_distance(end_node)
        to_search: List[Node] = [start_node]
        processed: List[Node] = []

        while len(to_search) > 0:
            current: Node = to_search[0]

            for node in to_search:
                if node.f < current.f or node.f == current.f and node.h < current.h:
                    current = node

            if current.pos == end_node.pos:
                current_path_tile: Node = end_node
                path = []
                while current_path_tile.pos != start_node.pos:
                    path.append(current_path_tile)
                    current_path_tile = current_path_tile.connection
                return path

            processed.append(current)
            to_search.remove(current)

            for neighbor_pos in current.neighbors:
                neighbor: Node = self.get_node(neighbor_pos)
                if neighbor.walkable and neighbor not in processed:
                    in_search = neighbor in to_search

                    cost_to_neighbor = current.g + current.get_distance(neighbor)

                    if not in_search or cost_to_neighbor < neighbor.g:
                        neighbor.g = cost_to_neighbor
                        neighbor.connection = current

                        if not in_search:
                            neighbor.h = neighbor.get_distance(end_node)
                            to_search.append(neighbor)

                    if step_callback:
                        step_callback(neighbor.pos, "neighbor")

            if step_callback:
                step_callback(current.pos, "processed")

        return None
