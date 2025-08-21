from typing import List, Set
from graph import Graph
from pygame import Color
from enum import Enum

import common

class Direction(Enum):
    NONE = ''
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class PacMan:
    def __init__(self, color: Color, start_node: int, graph_nodes: Set[int]):
        self.color: Color = color
        self.current_node: int = start_node
        self.graph_nodes: Set[int] = graph_nodes

        self.direction: Direction = Direction.NONE

        node_pos = common.node_number_to_cursor_pos(self.current_node)
        self.pixel_pos = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos = self.pixel_pos[:]

    def get_color(self) -> Color:
        return self.color

    def get_current_node(self) -> int:
        return self.current_node

    def set_current_node(self, new_node: int):
        self.current_node = new_node

    def set_direction(self, direction: Direction):
        self.direction = direction

    def move_to_next_node(self) -> int:
        if self.direction == Direction.UP:
            node_above: int | None = self.current_node - (common.GRPH_SIZE[0]) if self.current_node >= common.GRPH_SIZE[0] else None
            if node_above in self.graph_nodes:
                self.current_node = node_above
        elif self.direction == Direction.DOWN:
            node_below: int | None = self.current_node + (common.GRPH_SIZE[0]) if self.current_node < (common.GRPH_SIZE[0] * (common.GRPH_SIZE[1] - 1)) else None
            if node_below in self.graph_nodes:
                self.current_node = node_below
        elif self.direction == Direction.LEFT:
            node_left: int | None = self.current_node - 1 if self.current_node % common.GRPH_SIZE[0] > 0 else None
            if node_left in self.graph_nodes:
                self.current_node = node_left
        elif self.direction == Direction.RIGHT:
            node_right: int | None = self.current_node + 1 if self.current_node % common.GRPH_SIZE[0] < (common.GRPH_SIZE[0] - 1) else None
            if node_right in self.graph_nodes:
                self.current_node = node_right
        return self.current_node

class Ghost:
    def __init__(self, name: str, color: Color, current_node: int):
        self.name: str = name
        self.color: Color = color
        self.current_node: int = current_node
        self.target_node: int | None = None
        self.path: List[int] | None = []
        self.ignore_nodes_relative_to_target: List[int] = []

        node_pos = common.node_number_to_cursor_pos(self.current_node)
        self.pixel_pos = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos = self.pixel_pos[:]


    def get_color(self) -> Color:
        return self.color

    def get_current_node(self) -> int:
        return self.current_node
    
    def get_target_node(self) -> int | None:
        return self.target_node
    
    def set_target_node(self, new_target: int, map: Graph, ignored_nodes: Set[int] = set()):
        self.target_node = new_target
        self.path = map.BFS(self.current_node, self.target_node, ignored_nodes)

    def get_path(self) -> List[int] | None:
        return self.path

    def move_to_next_node(self) -> int:
        if self.path:
            self.current_node = self.path.pop(0)
        return self.current_node
