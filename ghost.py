from typing import List, Tuple
from graph import Graph
from pygame import Color

import common

class Ghost:
    def __init__(self, color: Color, current_node: int, target_node: int, map: Graph):
        self.color: Color = color
        self.current_node: int = current_node
        self.target_node: int = target_node
        self.path: List[int] = map.BFS(self.current_node, self.target_node)

        self.pixel_pos: Tuple[float, float] = (0.0, 0.0)
        self.target_pixel_pos: Tuple[float, float] = (0.0, 0.0)

        node_pos = common.node_number_to_cursor_pos(self.current_node)
        self.pixel_pos = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos = self.pixel_pos[:]

    def get_color(self) -> Color:
        return self.color

    def get_current_node(self) -> int:
        return self.current_node
    
    def get_target_node(self) -> int:
        return self.target_node
    
    def set_target_node(self, new_target: int, map: Graph):
        self.target_node = new_target
        self.path = map.BFS(self.current_node, self.target_node)

    def get_path(self) -> List[int]:
        return self.path

    def move_to_next_node(self) -> int:
        if self.path:
            self.current_node = self.path.pop(0)
        return self.current_node
