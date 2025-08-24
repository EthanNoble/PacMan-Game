from typing import List, Set, Tuple
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

class GhostMode(Enum):
    CHASE = 'chase'
    SCATTER = 'scatter'
    FRIGHTENED = 'frightened'

class PacMan:
    def __init__(self, start_node: int, legal_tiles: Set[int]):
        self.current_node: int = start_node
        self.direction: Direction = Direction.NONE
        self.color: Tuple[int, int, int, int] = (255, 255, 0, 255)

        node_pos = common.node_number_to_cursor_pos(self.current_node)
        self.pixel_pos: Tuple[int, int] = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos: Tuple[int, int] = self.pixel_pos[:]

        self.speed: float = 0.8

        self.legal_tiles: Set[int] = legal_tiles

        self._animation_speed: int = 3 # Every so and so frames
        self._animation_frame: int = 0

        self._body_animation_frame: int = 0
        self._body_animation: List[List[pg.Surface]] = [
            [
                common.load_asset(assets.PACMAN1),
                common.load_asset(assets.PACMAN1),
                common.load_asset(assets.PACMAN1),
                common.load_asset(assets.PACMAN1),
            ],
            [
                common.load_asset(assets.PACMAN2_RIGHT),
                common.load_asset(assets.PACMAN2_DOWN),
                common.load_asset(assets.PACMAN2_LEFT),
                common.load_asset(assets.PACMAN2_UP),
            ],
            [
                common.load_asset(assets.PACMAN3_RIGHT),
                common.load_asset(assets.PACMAN3_DOWN),
                common.load_asset(assets.PACMAN3_LEFT),
                common.load_asset(assets.PACMAN3_UP),
            ]
        ]

    def render(self, screen: pg.Surface):
        position: Tuple[int, int] = (self.pixel_pos[0] - common.TILE_SIZE[0] + 2, self.pixel_pos[1] - common.TILE_SIZE[1] + 1)
        common.place_image(screen=screen, image=self.get_body_image(), position=position)

    def get_body_image(self) -> pg.Surface:
        return self._body_animation[self._body_animation_frame][self.direction_to_index()]
    
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
        self._animation_frame = (self._animation_frame + 1) % self._animation_speed
        if self._animation_frame == 0:
            self._body_animation_frame = (self._body_animation_frame + 1) % len(self._body_animation)

    def smooth_move(self) -> None:
        if self.pixel_pos == self.target_pixel_pos:
            new_node: int = self.move_to_next_node()
            target_pos = common.node_number_to_cursor_pos(new_node)
            self.target_pixel_pos = (target_pos[0] + common.OFFSET[0], target_pos[1] + common.OFFSET[1])

        dx = self.target_pixel_pos[0] - self.pixel_pos[0]
        dy = self.target_pixel_pos[1] - self.pixel_pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > self.speed:
            self.pixel_pos = (self.pixel_pos[0] + self.speed * dx / dist, self.pixel_pos[1] + self.speed * dy / dist)
        else:
            self.pixel_pos = self.target_pixel_pos[:]

    def move_to_next_node(self) -> int:
        if self.direction == Direction.UP:
            node_above: int | None = self.current_node - (common.TILE_DIMS[0]) if self.current_node >= common.TILE_DIMS[0] else None
            if node_above in self.legal_tiles:
                self.current_node = node_above
        elif self.direction == Direction.DOWN:
            node_below: int | None = self.current_node + (common.TILE_DIMS[0]) if self.current_node < (common.TILE_DIMS[0] * (common.TILE_DIMS[1] - 1)) else None
            if node_below in self.legal_tiles:
                self.current_node = node_below
        elif self.direction == Direction.LEFT:
            node_left: int | None = self.current_node - 1 if self.current_node % common.TILE_DIMS[0] > 0 else None
            if node_left in self.legal_tiles:
                self.current_node = node_left
        elif self.direction == Direction.RIGHT:
            node_right: int | None = self.current_node + 1 if self.current_node % common.TILE_DIMS[0] < (common.TILE_DIMS[0] - 1) else None
            if node_right in self.legal_tiles:
                self.current_node = node_right
        
        return self.current_node

class Ghost:
    def __init__(self, name: GhostName, current_node: int, scatter_target_node: int):
        self.name: GhostName = name
        self.current_node: int = current_node
        self.target_node: int = -1
        self.direction: Direction = Direction.NONE
        self.color: Tuple[int, int, int, int] = (0, 0, 0, 0)

        self._mode: GhostMode = GhostMode.CHASE
        self._scatter_target_node: int = scatter_target_node

        node_pos = common.node_number_to_cursor_pos(self.current_node)
        self.pixel_pos: Tuple[int, int] = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos: Tuple[int, int] = self.pixel_pos[:]

        self.speed: float = 0.8

        self._previous_tile: int = -1

        self._animation_speed: int = 5 # Every so and so frames
        self._animation_frame: int = 0

        self._body_animation_frame: int = 0
        self._body_animation: List[List[pg.Surface]] = []
        match self.name:
            case GhostName.BLINKY:
                self.color = (255, 0, 0, 255)
                self._body_animation = [
                    [
                        common.load_asset(assets.BLINKY1_RIGHT),
                        common.load_asset(assets.BLINKY1_DOWN),
                        common.load_asset(assets.BLINKY1_LEFT),
                        common.load_asset(assets.BLINKY1_UP),
                    ],
                    [
                        common.load_asset(assets.BLINKY2_RIGHT),
                        common.load_asset(assets.BLINKY2_DOWN),
                        common.load_asset(assets.BLINKY2_LEFT),
                        common.load_asset(assets.BLINKY2_UP),
                    ]
                ]
            case GhostName.PINKY:
                self.color = (255, 192, 203, 255)
                self._body_animation = [
                    [
                        common.load_asset(assets.PINKY1_RIGHT),
                        common.load_asset(assets.PINKY1_DOWN),
                        common.load_asset(assets.PINKY1_LEFT),
                        common.load_asset(assets.PINKY1_UP),
                    ],
                    [
                        common.load_asset(assets.PINKY2_RIGHT),
                        common.load_asset(assets.PINKY2_DOWN),
                        common.load_asset(assets.PINKY2_LEFT),
                        common.load_asset(assets.PINKY2_UP),
                    ]
                ]
            case GhostName.INKY:
                self.color = (0, 255, 255, 255)
                self._body_animation = [
                    [
                        common.load_asset(assets.INKY1_RIGHT),
                        common.load_asset(assets.INKY1_DOWN),
                        common.load_asset(assets.INKY1_LEFT),
                        common.load_asset(assets.INKY1_UP),
                    ],
                    [
                        common.load_asset(assets.INKY2_RIGHT),
                        common.load_asset(assets.INKY2_DOWN),
                        common.load_asset(assets.INKY2_LEFT),
                        common.load_asset(assets.INKY2_UP),
                    ]
                ]
            case GhostName.CLYDE:
                self.color = (255, 165, 0, 255)
                self._body_animation = [
                    [
                        common.load_asset(assets.CLYDE1_RIGHT),
                        common.load_asset(assets.CLYDE1_DOWN),
                        common.load_asset(assets.CLYDE1_LEFT),
                        common.load_asset(assets.CLYDE1_UP),
                    ],
                    [
                        common.load_asset(assets.CLYDE2_RIGHT),
                        common.load_asset(assets.CLYDE2_DOWN),
                        common.load_asset(assets.CLYDE2_LEFT),
                        common.load_asset(assets.CLYDE2_UP),
                    ]
                ]

    def render(self, screen: pg.Surface):
        position: Tuple[int, int] = (self.pixel_pos[0] - common.TILE_SIZE[0] + 1, self.pixel_pos[1] - common.TILE_SIZE[1] + 1)
        common.place_image(screen=screen, image=self.get_body_image(), position=position)

        if common.SHOW_TARGET_NODES and self.target_node != -1:
            target_position: Tuple[int, int] = common.node_number_to_cursor_pos(self.target_node)
            common.draw_rect(screen=screen, color=self.color, rect=(target_position[0], target_position[1], common.TILE_SIZE[0]+1, common.TILE_SIZE[1]+1), width=1)

    def get_body_image(self) -> pg.Surface:
        return self._body_animation[self._body_animation_frame][self.direction_to_index()]

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
        self._animation_frame = (self._animation_frame + 1) % self._animation_speed
        if self._animation_frame == 0:
            self._body_animation_frame = (self._body_animation_frame + 1) % len(self._body_animation)

    def get_color(self) -> Tuple[int, int, int, int]:
        return self.color

    def set_mode(self, mode: GhostMode) -> None:
        self._mode = mode
        if self._mode == GhostMode.SCATTER:
            self.target_node = self._scatter_target_node

    def choose_target_tile(self, blinky: 'Ghost', pacman: PacMan) -> None:
        if self._mode == GhostMode.SCATTER:
            return
        
        match self.name:
            case GhostName.BLINKY:
                self.target_node = pacman.current_node
            case GhostName.PINKY:
                match pacman.direction:
                    case Direction.UP:
                        self.target_node = pacman.current_node - common.TILE_DIMS[0]*4
                    case Direction.DOWN:
                        self.target_node = pacman.current_node + common.TILE_DIMS[0]*4
                    case Direction.LEFT:
                        self.target_node = pacman.current_node - 4
                    case Direction.RIGHT:
                        self.target_node = pacman.current_node + 4
                    case _:
                        self.target_node = pacman.current_node
            case GhostName.INKY:
                blinky_pos: Tuple[int, int] = common.node_number_to_cursor_pos(blinky.current_node)
                offset_tile: Tuple[int, int] = (0, 0)

                match pacman.direction:
                    case Direction.UP:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_node - common.TILE_DIMS[0]*2)
                    case Direction.DOWN:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_node + common.TILE_DIMS[0]*2)
                    case Direction.LEFT:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_node - 2)
                    case Direction.RIGHT:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_node + 2)
                    case _:
                        offset_tile = common.node_number_to_cursor_pos(pacman.current_node)

                dx: int = offset_tile[0] - blinky_pos[0]
                dy: int = offset_tile[1] - blinky_pos[1]
                target_x = blinky_pos[0] + 2*dx
                target_y = blinky_pos[1] + 2*dy
                self.target_node = common.cursor_pos_to_node_number((target_x, target_y))
                
                if common.SHOW_TARGET_NODES:
                    # Drawing the vector from Blinky through the offset tile to Inky's target tile
                    pg.draw.line(
                        pg.display.get_surface(),
                        self.color,
                        start_pos=(blinky_pos[0] + common.OFFSET[0], blinky_pos[1] + common.OFFSET[1]),
                        end_pos=(target_x + common.OFFSET[0], target_y + common.OFFSET[1]),
                        width=1)

            case GhostName.CLYDE:
                pacman_pos: Tuple[int, int] = common.node_number_to_cursor_pos(pacman.current_node)
                ghost_pos: Tuple[int, int] = common.node_number_to_cursor_pos(self.current_node)

                dx: int = pacman_pos[0] - ghost_pos[0]
                dy: int = pacman_pos[1] - ghost_pos[1]
                dist: float = (dx ** 2 + dy ** 2) ** 0.5
                tile_dist: float = dist / common.TILE_SIZE[0]
                
                if tile_dist >= 8:
                    self.target_node = pacman.current_node
                else:
                    self.target_node = self._scatter_target_node

    def smooth_move(self, legal_space: Set[int]) -> None:
        if self.pixel_pos == self.target_pixel_pos:
            new_node: int = self.move_to_next_node(legal_space)
            target_pos = common.node_number_to_cursor_pos(new_node)
            self.target_pixel_pos = (target_pos[0] + common.OFFSET[0], target_pos[1] + common.OFFSET[1])

        dx = self.target_pixel_pos[0] - self.pixel_pos[0]
        dy = self.target_pixel_pos[1] - self.pixel_pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dx < 0:
            self.direction = Direction.LEFT
        elif dx > 0:
            self.direction = Direction.RIGHT
        elif dy < 0:
            self.direction = Direction.UP
        elif dy > 0:
            self.direction = Direction.DOWN

        if dist > self.speed:
            self.pixel_pos = (self.pixel_pos[0] + self.speed * dx / dist, self.pixel_pos[1] + self.speed * dy / dist)
        else:
            self.pixel_pos = self.target_pixel_pos[:]

    def move_to_next_node(self, legal_tiles: Set[int]) -> int:
        ghost_position: Tuple[int, int] = common.node_number_to_cursor_pos(self.current_node)
        target_position: Tuple[int, int] = common.node_number_to_cursor_pos(self.target_node)

        # Get tiles above, below, left, and right of ghost
        above_tile_pos: Tuple[int, int] = (ghost_position[0], ghost_position[1] - common.TILE_SIZE[1])
        below_tile_pos: Tuple[int, int] = (ghost_position[0], ghost_position[1] + common.TILE_SIZE[1])
        left_tile_pos: Tuple[int, int] = (ghost_position[0] - common.TILE_SIZE[0], ghost_position[1])
        right_tile_pos: Tuple[int, int] = (ghost_position[0] + common.TILE_SIZE[0], ghost_position[1])
        candidate_tiles: List[Tuple[int, int]] = [right_tile_pos, below_tile_pos, left_tile_pos, above_tile_pos]

        legal_moves: List[Tuple[int, int]] = []
        for tile in candidate_tiles:
            node_number: int = common.cursor_pos_to_node_number(tile)
            if node_number in legal_tiles and node_number != self._previous_tile:
                legal_moves.append(tile)
        
        self._previous_tile = common.cursor_pos_to_node_number(ghost_position)

        # Determine the legal move that is closest to target position
        min_dist: float = float('inf')
        move_to_node: int = -1
        for move in legal_moves:
            dx: int = move[0] - target_position[0]
            dy: int = move[1] - target_position[1]
            dist: float = (dx ** 2 + dy ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                move_to_node = common.cursor_pos_to_node_number(move)

        self.current_node = move_to_node if move_to_node != -1 else self.current_node
        return self.current_node
