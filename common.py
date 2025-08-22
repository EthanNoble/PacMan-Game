from typing import Tuple
import pygame as pg

# Number of nodes in graph (W, H)
GRPH_SIZE = (28, 36)
# Size of each node in pixels
NODE_SIZE = (26, 26)
# Offset for game map graph
OFFSET = (NODE_SIZE[0]//2, NODE_SIZE[1]//2)

DEBUG_MODE = True
SHOW_GRID_LINES = False
DEBUG_GRAPH_NODES = False

def node_number_to_cursor_pos(node_number: int) -> Tuple[int, int]:
    node_x: int = (node_number % GRPH_SIZE[0]) * NODE_SIZE[0]
    node_y: int = (node_number // GRPH_SIZE[0]) * NODE_SIZE[1]
    return node_x, node_y

def load_asset(asset_path: str = '', scale: float = 1.0) -> pg.Surface:
    asset_image: pg.Surface = pg.image.load(asset_path)

    ratio: float = asset_image.get_height() / asset_image.get_width()
    width: int = int(NODE_SIZE[0] * scale)
    height: int = int(ratio * NODE_SIZE[1] * scale)

    scaled_image: pg.Surface = pg.transform.scale(asset_image, (width, height))
    return scaled_image

def place_image(screen: pg.Surface, image: pg.Surface | None, position: Tuple[int, int]) -> None:
    if image:
        screen.blit(image, (position[0], position[1]))