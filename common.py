from typing import Tuple
import pygame as pg

# Number of tiles on screen (W, H)
TILE_DIMS = (28, 36)

# Size of each tile in pixels
TILE_SIZE = (26, 26)

# Size of the window in pixels
SCR_SIZE = (TILE_DIMS[0] * TILE_SIZE[0], TILE_DIMS[1] * TILE_SIZE[1])

# Offset for game map graph
OFFSET = (TILE_SIZE[0]//2, TILE_SIZE[1]//2)

DEBUG_MODE = False
SHOW_GRID_LINES = False
SHOW_TILE_NUMS = False
SHOW_TARGET_NODES = False
SHOW_FPS = True

def node_number_to_cursor_pos(node_number: int) -> Tuple[int, int]:
    node_x: int = (node_number % TILE_DIMS[0]) * TILE_SIZE[0]
    node_y: int = (node_number // TILE_DIMS[0]) * TILE_SIZE[1]
    return node_x, node_y

def cursor_pos_to_node_number(cursor_pos: Tuple[int, int]) -> int:
    node_x, node_y = cursor_pos_to_selection(cursor_pos)
    return node_x // TILE_SIZE[0] + (node_y // TILE_SIZE[1]) * TILE_DIMS[0]

def cursor_pos_to_selection(cursor_pos: Tuple[int, int]) -> Tuple[int, int]:
    node_x = int((cursor_pos[0] / SCR_SIZE[0]) * TILE_DIMS[0]) * TILE_SIZE[0]
    node_y = int((cursor_pos[1] / SCR_SIZE[1]) * TILE_DIMS[1]) * TILE_SIZE[1]
    return node_x, node_y

def load_asset(asset_path: str = '', scale: float = 1.0) -> pg.Surface:
    asset_image: pg.Surface = pg.image.load(asset_path)

    ratio: float = asset_image.get_height() / asset_image.get_width()
    width: int = int(TILE_SIZE[0] * scale)
    height: int = int(ratio * TILE_SIZE[1] * scale)

    scaled_image: pg.Surface = pg.transform.scale(asset_image, (width, height))
    return scaled_image

def place_image(screen: pg.Surface, image: pg.Surface | None, position: Tuple[int, int]) -> None:
    if image:
        screen.blit(image, (position[0], position[1]))

def draw_rect(screen: pg.Surface, color: Tuple[int, int, int, int], rect: Tuple[int, int, int, int], width: int = 0) -> None:
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect(), width)
    screen.blit(shape_surf, rect)