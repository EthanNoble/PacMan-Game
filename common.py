from typing import Tuple
import pygame as pg

# Number of nodes in graph (W, H)
GRPH_SIZE = (28, 36)
# Size of each node in pixels
NODE_SIZE = (26, 26)
# Offset for game map graph
OFFSET = (NODE_SIZE[0]//2, NODE_SIZE[1]//2)

DEBUG_MODE = True
DEBUG_GRAPH_NODES = False

def node_number_to_cursor_pos(node_number: int) -> Tuple[int, int]:
    node_x: int = (node_number % GRPH_SIZE[0]) * NODE_SIZE[0]
    node_y: int = (node_number // GRPH_SIZE[0]) * NODE_SIZE[1]
    return node_x, node_y

def load_asset(asset_path: str = '', scale: float = 1.0) -> pg.Surface:
    asset_image = pg.image.load(asset_path)
    scaled_image = pg.transform.scale(asset_image, (int(NODE_SIZE[0] * scale), int(NODE_SIZE[1] * scale)))
    return scaled_image

def place_image(screen: pg.Surface, image: pg.Surface | None, position: Tuple[int, int], scale: float = 1.0) -> None:
    if image:
        if scale > 1:
            scaled_image = pg.transform.scale(image, (int(NODE_SIZE[0] * scale), int(NODE_SIZE[1] * scale)))
        else:
            scaled_image = image

        screen.blit(scaled_image, (position[0], position[1]))