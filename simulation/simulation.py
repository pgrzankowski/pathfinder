import pygame
from pathfinder import Pathfinder
from utils import get_map_array
import time

class Simulation:
    def __init__(self, map_path='maps/empty_map.csv'):
        self._map_array = get_map_array(map_path)
        shape = (len(self._map_array[0])*10, len(self._map_array)*10)
        pygame.init()
        self._screen = pygame.display.set_mode(shape)
        self._clock = pygame.time.Clock()
        self._running = False
        self._start_pos = None
        self._end_pos = None
        self._mouse_dragging = False

    def run(self):
        print("CONTROLS")
        print("TARGET POSITIONS:")
        print("\tSTART:\ts")
        print("\tEND:\te")
        print("PLAN ROUTE:\tSPACE")
        print("DRAW BORDERS:\tHOLD AND PRESS MOUSE")
        self.render_scene()
        self._running = True
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = mouse_pos[0] // 10, mouse_pos[1] // 10
                    if event.key == pygame.K_s:
                        x, y = mouse_pos
                        if self._map_array[y][x] == 0:
                            self._start_pos = mouse_pos
                            self.render_scene()
                            print(f"Start pos set to: {mouse_pos}")
                        else:
                            print("Can't set start on the border")
                    if event.key == pygame.K_e:
                        x, y = mouse_pos
                        if self._map_array[y][x] == 0:
                            self._end_pos = mouse_pos
                            self.render_scene()
                            print(f"End pos set to: {mouse_pos}")
                        else:
                            print("Can't set end on the border")
                    if event.key == pygame.K_SPACE:
                        if self.can_plan():
                            print('Planning route:')
                            print(f"\tFrom: {self._start_pos}")
                            print(f"\tTo: {self._end_pos}")
                            planner = Pathfinder(self._map_array,
                                                  self._start_pos,
                                                  self._end_pos)
                            path = planner.plan(step_callback=self.update_realtime)
                            if path:
                                print("Planned path:")
                                [print(node.get_pos(), end=", ") for node in path]
                                self.render_path(path)
                                self.render_pos()
                            else:
                                print("There's no possible path there!")
                    if event.key == pygame.K_c:
                        self.clear_scene()
                    if event.key == pygame.K_r:
                        self.reset_scene()
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.render_scene()
                    self._mouse_dragging = True
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = mouse_pos[0] // 10, mouse_pos[1] // 10
                    self.draw_border(mouse_pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    self._mouse_dragging = False
                if event.type == pygame.MOUSEMOTION and self._mouse_dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = mouse_pos[0] // 10, mouse_pos[1] // 10
                    self.draw_border(mouse_pos)

            # self.render_pos()
            pygame.display.flip()
            self._clock.tick(60)
        pygame.quit()

    def can_plan(self):
        return self._start_pos and self._end_pos

    def render_scene(self):
        self._screen.fill("black")
        self.render_pos()
        for y, line in enumerate(self._map_array):
            for x, cell in enumerate(line):
                if cell == 1:
                    self._screen.fill("white",
                                      (x*10, y*10, 10, 10))

    def clear_scene(self):
        self._start_pos = None
        self._end_pos = None
        self.render_scene()

    def reset_scene(self):
        for y in range(len(self._map_array)):
            for x in range(len(self._map_array[0])):
                self._map_array[y][x] = 0
        self.clear_scene()

    def render_pos(self):
        if self._start_pos:
            self._screen.fill("green",
                              (self._start_pos[0]*10, self._start_pos[1]*10, 10, 10))
        if self._end_pos:
            self._screen.fill("red",
                              (self._end_pos[0]*10, self._end_pos[1]*10, 10, 10))

    def draw_border(self, pos):
        if pos == self._start_pos or pos == self._end_pos:
            print("Can't draw on start/end position!")
            return
        x, y = pos
        self._map_array[y][x] = 1
        self._screen.fill("white", (x*10, y*10, 10, 10))

    def render_path(self, path):
        if path:
            for tile in path:
                x, y = tile.get_pos()
                self._screen.fill("yellow", (x*10, y*10, 10, 10))
                pygame.display.flip()
                time.sleep(0.01)
        else:
            print("Path from START to END is not possible")

    def update_realtime(self, pos, node_type):
        x, y = pos
        color = "blue" if node_type == "neighbor" else "purple"
        self._screen.fill(color, (x*10, y*10, 10, 10))
        self.render_pos()
        pygame.display.flip()
        time.sleep(0.001)