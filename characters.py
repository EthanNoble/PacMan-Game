from typing import List, Set, Tuple
from graph import Graph
from pygame import Color
from enum import Enum
import pygame as pg
import assets

import common

class Direction(Enum):
    NONE = ''
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class GhostName(Enum):
    BLINKY = 'Blinky'
    PINKY = 'Pinky'
    INKY = 'Inky'
    CLYDE = 'Clyde'

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
    def __init__(self, name: GhostName, current_node: int):
        self.name: GhostName = name
        self.current_node: int = current_node
        self.target_node: int | None = None
        self.direction: Direction = Direction.NONE
        self.path: List[int] | None = []

        node_pos = common.node_number_to_cursor_pos(self.current_node)
        self.pixel_pos = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos = self.pixel_pos[:]

        self.animation_speed: int = 5 # Every so and so frames
        self.animation_frame: int = 0

        self.scale: float = 1.5
        self.body_animation_frame: int = 0
        self.body_animation: List[List[pg.Surface]] = []
        match self.name:
            case GhostName.BLINKY:
                self.color = pg.Color('red')
                self.body_animation = [
                    [
                        common.load_asset(assets.BLINKY1_RIGHT, scale=self.scale),
                        common.load_asset(assets.BLINKY1_DOWN, scale=self.scale),
                        common.load_asset(assets.BLINKY1_LEFT, scale=self.scale),
                        common.load_asset(assets.BLINKY1_UP, scale=self.scale),
                    ],
                    [
                        common.load_asset(assets.BLINKY2_RIGHT, scale=self.scale),
                        common.load_asset(assets.BLINKY2_DOWN, scale=self.scale),
                        common.load_asset(assets.BLINKY2_LEFT, scale=self.scale),
                        common.load_asset(assets.BLINKY2_UP, scale=self.scale),
                    ]
                ]
            case GhostName.PINKY:
                self.color = pg.Color('pink')
                self.body_animation = [
                    [
                        common.load_asset(assets.PINKY1_RIGHT, scale=self.scale),
                        common.load_asset(assets.PINKY1_DOWN, scale=self.scale),
                        common.load_asset(assets.PINKY1_LEFT, scale=self.scale),
                        common.load_asset(assets.PINKY1_UP, scale=self.scale),
                    ],
                    [
                        common.load_asset(assets.PINKY2_RIGHT, scale=self.scale),
                        common.load_asset(assets.PINKY2_DOWN, scale=self.scale),
                        common.load_asset(assets.PINKY2_LEFT, scale=self.scale),
                        common.load_asset(assets.PINKY2_UP, scale=self.scale),
                    ]
                ]
            case GhostName.INKY:
                self.color = pg.Color('cyan')
                self.body_animation = [
                    [
                        common.load_asset(assets.INKY1_RIGHT, scale=self.scale),
                        common.load_asset(assets.INKY1_DOWN, scale=self.scale),
                        common.load_asset(assets.INKY1_LEFT, scale=self.scale),
                        common.load_asset(assets.INKY1_UP, scale=self.scale),
                    ],
                    [
                        common.load_asset(assets.INKY2_RIGHT, scale=self.scale),
                        common.load_asset(assets.INKY2_DOWN, scale=self.scale),
                        common.load_asset(assets.INKY2_LEFT, scale=self.scale),
                        common.load_asset(assets.INKY2_UP, scale=self.scale),
                    ]
                ]
            case GhostName.CLYDE:
                self.color = pg.Color('orange')
                self.body_animation = [
                    [
                        common.load_asset(assets.CLYDE1_RIGHT, scale=self.scale),
                        common.load_asset(assets.CLYDE1_DOWN, scale=self.scale),
                        common.load_asset(assets.CLYDE1_LEFT, scale=self.scale),
                        common.load_asset(assets.CLYDE1_UP, scale=self.scale),
                    ],
                    [
                        common.load_asset(assets.CLYDE2_RIGHT, scale=self.scale),
                        common.load_asset(assets.CLYDE2_DOWN, scale=self.scale),
                        common.load_asset(assets.CLYDE2_LEFT, scale=self.scale),
                        common.load_asset(assets.CLYDE2_UP, scale=self.scale),
                    ]
                ]
    def render(self, screen: pg.Surface):
        # Body
        body_position: Tuple[int, int] = (int(self.pixel_pos[0] - common.OFFSET[0]*self.scale), int(self.pixel_pos[1] - common.OFFSET[1]*self.scale))
        common.place_image(screen, self.get_body_image(), body_position)

    def get_body_image(self) -> pg.Surface:
        return self.body_animation[self.body_animation_frame][self.direction_to_index()]
    
    def direction_to_index(self) -> int:
        match self.direction:
            case Direction.UP:
                return 3
            case Direction.DOWN:
                return 1
            case Direction.LEFT:
                return 2
            case Direction.RIGHT:
                return 0
            case _:
                return 0

    def animate(self):
        self.animation_frame = (self.animation_frame + 1) % self.animation_speed
        if self.animation_frame == 0:
            self.body_animation_frame = (self.body_animation_frame + 1) % len(self.body_animation)

    def get_current_node(self) -> int:
        return self.current_node
    
    def get_target_node(self) -> int | None:
        return self.target_node
    
    def set_target_node(self, new_target: int, map: Graph, ignored_nodes: Set[int] = set()):
        self.target_node = new_target
        self.path = map.BFS(self.current_node, self.target_node, ignored_nodes)
        if len(self.path) == 0:
            self.path = map.BFS(self.current_node, self.target_node) # Retry without ignored nodes
    
    def get_color(self) -> Color:
        return self.color

    def get_path(self) -> List[int] | None:
        return self.path

    def move_to_next_node(self) -> int:
        if self.path:
            self.current_node = self.path.pop(0)
        return self.current_node
