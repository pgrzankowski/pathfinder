from pathfinder.node import Node

class Pathfinder:
    def __init__(self, map_array, start_pos, end_pos):
        self._map_array = map_array
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._nodes = {}

    def get_node(self, pos):
        if pos not in self._nodes:
            self._nodes[pos] = Node(pos,
                                    self._start_pos,
                                    self._end_pos,
                                    self._map_array)
        return self._nodes[pos]

    def plan(self):
        start_node = self.get_node(self._start_pos)
        end_node = self.get_node(self._end_pos)
        to_search = [start_node]
        processed = []

        while len(to_search) > 0:
            current = to_search[0]

            for node in to_search:
                if node.F < current.F or node.F == current.F and node.H < current.H:
                    current = node

            processed.append(current)
            to_search.remove(current)

            if current.get_pos() == end_node.get_pos():
                current_path_tile = end_node
                path = []
                while current_path_tile.get_pos() != start_node.get_pos():
                    path.append(current_path_tile)
                    current_path_tile = current_path_tile.get_connections()

                return path

            for neighbor_pos in current.neighbors():
                neighbor = self.get_node(neighbor_pos)
                if neighbor.walkable() and neighbor not in processed:
                    in_search = neighbor in to_search

                    cost_to_neighbor = current.G + current.get_distance(neighbor.get_pos())

                    if not in_search or cost_to_neighbor < neighbor.G:
                        neighbor.set_g(cost_to_neighbor)
                        neighbor.set_connection(current)

                        if not in_search:
                            neighbor.set_h(neighbor.get_distance(end_node.get_pos()))
                            to_search.append(neighbor)

        return None
