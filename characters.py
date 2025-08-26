from typing import List, Set, Tuple
from enum import Enum
import pygame as pg
import assets
import common

class Character:
    class Direction(Enum):
        NONE = ''
        UP = 'up'
        DOWN = 'down'
        LEFT = 'left'
        RIGHT = 'right'
        
    def __init__(self, current_tile: int, animation_speed: int, direction: 'Character.Direction' = Direction.NONE):
        self.current_tile: int = current_tile
        self.direction: Character.Direction = direction
        self.color: Tuple[int, int, int, int]

        node_pos = common.node_number_to_cursor_pos(self.current_tile)
        self.pixel_pos: Tuple[int, int] = (node_pos[0] + common.OFFSET[0], node_pos[1] + common.OFFSET[1])
        self.target_pixel_pos: Tuple[int, int] = self.pixel_pos[:]

        self.speed: float = 0.8

        self._animation_speed: int = animation_speed
        self._animation_frame: int = 0
    
    # Implemented Methods #
    def direction_to_index(self) -> int:
        match self.direction:
            case Character.Direction.UP:
                return 3
            case Character.Direction.DOWN:
                return 1
            case Character.Direction.LEFT:
                return 2
            case Character.Direction.RIGHT:
                return 0
            case _:
                return 0
    
    # Abstract Methods #
    def render(self, screen: pg.Surface) -> None:
        raise NotImplementedError("Subclasses must implement render method")
    
    def animate(self) -> None:
        raise NotImplementedError("Subclasses must implement animate method")

    def smooth_move(self, legal_space: Set[int] | None = None) -> None:
        raise NotImplementedError("Subclasses must implement smooth_move method")
    
    def move_to_next_node(self, legal_tiles: Set[int] | None = None) -> int:
        raise NotImplementedError("Subclasses must implement move_to_next_node method")

    def get_image(self) -> pg.Surface:
        raise NotImplementedError("Subclasses must implement get_image method")

class PacMan(Character):
    def __init__(self, current_tile: int, legal_tiles: Set[int]):
        super().__init__(current_tile, animation_speed=3)

        self.legal_tiles: Set[int] = legal_tiles

        self._dying: bool = False
        self._dead: bool = False

        self._body_animation_frame: int = 0
        self._death_animation_frame: int = 0

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
        self._death_animation: List[pg.Surface] = [
            common.load_asset(assets.PACMAN_DEATH_1),
            common.load_asset(assets.PACMAN_DEATH_2),
            common.load_asset(assets.PACMAN_DEATH_3),
            common.load_asset(assets.PACMAN_DEATH_4),
            common.load_asset(assets.PACMAN_DEATH_5),
            common.load_asset(assets.PACMAN_DEATH_6),
            common.load_asset(assets.PACMAN_DEATH_7),
            common.load_asset(assets.PACMAN_DEATH_8),
            common.load_asset(assets.PACMAN_DEATH_9),
            common.load_asset(assets.PACMAN_DEATH_10),
            common.load_asset(assets.PACMAN_DEATH_11)
        ]

    def render(self, screen: pg.Surface) -> None:
        if self._dead:
            return
        
        position: Tuple[int, int] = (self.pixel_pos[0] - common.TILE_SIZE[0], self.pixel_pos[1] - common.TILE_SIZE[1])
        common.place_image(screen=screen, image=self.get_image(), position=position)

    def get_image(self) -> pg.Surface:
        if not self._dying:
            return self._body_animation[self._body_animation_frame][self.direction_to_index()]
        return self._death_animation[self._death_animation_frame]
 
    def animate(self) -> None:
        if self._dead:
            return
        
        self._animation_frame = (self._animation_frame + 1) % self._animation_speed
        if self._animation_frame == 0:
            if not self._dying:
                self._body_animation_frame = (self._body_animation_frame + 1) % len(self._body_animation)
            else:
                self._death_animation_frame += 1
                if self._death_animation_frame >= len(self._death_animation):
                    self._dead = True

    def slowly_kill(self) -> None:
        self._dying = True
        self._animation_speed = 8
    
    def is_dying(self) -> bool:
        return self._dying

    def smooth_move(self, legal_space: Set[int] | None = None) -> None:
        if self._dying:
            return
        
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

    def move_to_next_node(self, legal_tiles: Set[int] | None = None) -> int:
        if self.direction == Character.Direction.UP:
            node_above: int | None = self.current_tile - (common.TILE_DIMS[0]) if self.current_tile >= common.TILE_DIMS[0] else None
            if node_above in self.legal_tiles:
                self.current_tile = node_above
        elif self.direction == Character.Direction.DOWN:
            node_below: int | None = self.current_tile + (common.TILE_DIMS[0]) if self.current_tile < (common.TILE_DIMS[0] * (common.TILE_DIMS[1] - 1)) else None
            if node_below in self.legal_tiles:
                self.current_tile = node_below
        elif self.direction == Character.Direction.LEFT:
            node_left: int | None = self.current_tile - 1 if self.current_tile % common.TILE_DIMS[0] > 0 else None
            if node_left in self.legal_tiles:
                self.current_tile = node_left
        elif self.direction == Character.Direction.RIGHT:
            node_right: int | None = self.current_tile + 1 if self.current_tile % common.TILE_DIMS[0] < (common.TILE_DIMS[0] - 1) else None
            if node_right in self.legal_tiles:
                self.current_tile = node_right

        return self.current_tile

class Ghost(Character):
    class Name(Enum):
        BLINKY = 'Blinky'
        PINKY = 'Pinky'
        INKY = 'Inky'
        CLYDE = 'Clyde'

    class Mode(Enum):
        CHASE = 'chase'
        SCATTER = 'scatter'
        FRIGHTENED = 'frightened'

    def __init__(self, name: Name, current_tile: int, scatter_target_node: int, dot_limit: int, direction: Character.Direction = Character.Direction.NONE):
        super().__init__(current_tile, animation_speed=6, direction=direction)
        self.name: Ghost.Name = name
        self.target_node: int = -1
        self.dot_limit: int = dot_limit

        self._mode: Ghost.Mode = Ghost.Mode.CHASE
        self._scatter_target_node: int = scatter_target_node

        self._in_monster_pen: bool = True
        self._monster_pen_pos: Tuple[int, int]
        # y direction +/- movement while in pen
        self._monster_pen_y_oscillation: int = 10
        # Will be any value between +/- above integer,
        # is the current oscillation value being added
        # to the ghost's y position
        self._oscillation_y_pos: int = 0

        self._previous_tile: int = -1

        self._body_animation_frame: int = 0
        self._body_animation: List[List[pg.Surface]] = []
        match self.name:
            case Ghost.Name.BLINKY:
                self.color = (255, 0, 0, 255)
                self._monster_pen_pos = (105, 133)
                self._in_monster_pen = False
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
            case Ghost.Name.PINKY:
                self.color = (255, 192, 203, 255)
                self._monster_pen_pos = (105, 133)
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
            case Ghost.Name.INKY:
                self.color = (0, 255, 255, 255)
                self._monster_pen_pos = (89, 133)
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
            case Ghost.Name.CLYDE:
                self.color = (255, 165, 0, 255)
                self._monster_pen_pos = (121, 133)
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
        common.place_image(screen=screen, image=self.get_image(), position=position if not self._in_monster_pen else self._monster_pen_pos)

        if common.SHOW_TARGET_NODES and self.target_node != -1:
            target_position: Tuple[int, int] = common.node_number_to_cursor_pos(self.target_node)
            common.draw_rect(screen=screen, color=self.color, rect=(target_position[0], target_position[1], common.TILE_SIZE[0]+1, common.TILE_SIZE[1]+1), width=1)

    def get_image(self) -> pg.Surface:
        return self._body_animation[self._body_animation_frame][self.direction_to_index()]

    def animate(self) -> None:
        self._animation_frame = (self._animation_frame + 1) % self._animation_speed
        if self._animation_frame == 0:
            self._body_animation_frame = (self._body_animation_frame + 1) % len(self._body_animation)

    def checkDotCount(self, num_dots_eaten: int) -> None:
        if num_dots_eaten >= self.dot_limit:
            self._in_monster_pen = False

    def in_monster_pen(self) -> bool:
        return self._in_monster_pen
    
    def set_mode(self, mode: 'Ghost.Mode') -> None:
        self._mode = mode
        if self._mode == Ghost.Mode.SCATTER:
            self.target_node = self._scatter_target_node

    def choose_target_tile(self, blinky: 'Ghost', pacman: PacMan) -> None:
        if self._mode == Ghost.Mode.SCATTER or self._in_monster_pen:
            return
        
        match self.name:
            case Ghost.Name.BLINKY:
                self.target_node = pacman.current_tile
            case Ghost.Name.PINKY:
                match pacman.direction:
                    case Character.Direction.UP:
                        self.target_node = pacman.current_tile - common.TILE_DIMS[0]*4
                    case Character.Direction.DOWN:
                        self.target_node = pacman.current_tile + common.TILE_DIMS[0]*4
                    case Character.Direction.LEFT:
                        self.target_node = pacman.current_tile - 4
                    case Character.Direction.RIGHT:
                        self.target_node = pacman.current_tile + 4
                    case _:
                        self.target_node = pacman.current_tile
            case Ghost.Name.INKY:
                blinky_pos: Tuple[int, int] = common.node_number_to_cursor_pos(blinky.current_tile)
                offset_tile: Tuple[int, int] = (0, 0)

                match pacman.direction:
                    case Character.Direction.UP:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_tile - common.TILE_DIMS[0]*2)
                    case Character.Direction.DOWN:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_tile + common.TILE_DIMS[0]*2)
                    case Character.Direction.LEFT:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_tile - 2)
                    case Character.Direction.RIGHT:
                        offset_tile  = common.node_number_to_cursor_pos(pacman.current_tile + 2)
                    case _:
                        offset_tile = common.node_number_to_cursor_pos(pacman.current_tile)

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

            case Ghost.Name.CLYDE:
                pacman_pos: Tuple[int, int] = common.node_number_to_cursor_pos(pacman.current_tile)
                ghost_pos: Tuple[int, int] = common.node_number_to_cursor_pos(self.current_tile)

                dx: int = pacman_pos[0] - ghost_pos[0]
                dy: int = pacman_pos[1] - ghost_pos[1]
                dist: float = (dx ** 2 + dy ** 2) ** 0.5
                tile_dist: float = dist / common.TILE_SIZE[0]
                
                if tile_dist >= 8:
                    self.target_node = pacman.current_tile
                else:
                    self.target_node = self._scatter_target_node

    def smooth_move(self, legal_space: Set[int] | None = None) -> None:
        if self._in_monster_pen:
            # Oscillate the ghost's y position while in the pen
            if abs(self._oscillation_y_pos) >= self._monster_pen_y_oscillation:
                # Flip direction
                if self.direction == Character.Direction.UP:
                    self.direction = Character.Direction.DOWN
                elif self.direction == Character.Direction.DOWN:
                    self.direction = Character.Direction.UP

            if self.direction == Character.Direction.UP:
                self._oscillation_y_pos -= 1
            elif self.direction == Character.Direction.DOWN:
                self._oscillation_y_pos += 1

            if self._oscillation_y_pos % 2 == 0:
                dy: int = -1 if self.direction == Character.Direction.UP else (1 if self.direction == Character.Direction.DOWN else 0)
                self._monster_pen_pos = (self._monster_pen_pos[0], self._monster_pen_pos[1] + dy)
        else:
            if self.pixel_pos == self.target_pixel_pos:
                new_node: int = self.move_to_next_node(legal_space)
                target_pos = common.node_number_to_cursor_pos(new_node)
                self.target_pixel_pos = (target_pos[0] + common.OFFSET[0], target_pos[1] + common.OFFSET[1])

            dx = self.target_pixel_pos[0] - self.pixel_pos[0]
            dy = self.target_pixel_pos[1] - self.pixel_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dx < 0:
                self.direction = Character.Direction.LEFT
            elif dx > 0:
                self.direction = Character.Direction.RIGHT
            elif dy < 0:
                self.direction = Character.Direction.UP
            elif dy > 0:
                self.direction = Character.Direction.DOWN

            if dist > self.speed:
                self.pixel_pos = (self.pixel_pos[0] + self.speed * dx / dist, self.pixel_pos[1] + self.speed * dy / dist)
            else:
                self.pixel_pos = self.target_pixel_pos[:]

    def move_to_next_node(self, legal_tiles: Set[int] | None = None) -> int:
        if self._in_monster_pen:
            return self.current_tile
        
        ghost_position: Tuple[int, int] = common.node_number_to_cursor_pos(self.current_tile)
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
            if legal_tiles and node_number in legal_tiles and node_number != self._previous_tile:
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

        self.current_tile = move_to_node if move_to_node != -1 else self.current_tile
        return self.current_tile
