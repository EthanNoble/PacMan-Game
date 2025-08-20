from typing import Tuple
import pygame as pg

# Number of nodes in graph (W, H)
GRPH_SIZE = (28, 36)
# Size of each node in pixels
NODE_SIZE = (26, 26)
# Offset for game map graph
OFFSET = (NODE_SIZE[0]//2, NODE_SIZE[1]//2)

DEBUG_MODE = False
DEBUG_GRAPH_NODES = False

def node_number_to_cursor_pos(node_number: int) -> Tuple[int, int]:
    node_x: int = (node_number % GRPH_SIZE[0]) * NODE_SIZE[0]
    node_y: int = (node_number // GRPH_SIZE[0]) * NODE_SIZE[1]
    return node_x, node_y