import pygame as pg
from graph import Graph
import assets

from typing import Tuple, List


# Number of nodes in graph (W, H)
GRPH_SIZE = (28, 36)
# Size of each node in pixels
NODE_SIZE = (20, 20)
# Size of the window in pixels
SCR_SIZE = (GRPH_SIZE[0] * NODE_SIZE[0], GRPH_SIZE[1] * NODE_SIZE[1])

def init_map():
    game_map = Graph()
    for _ in range(GRPH_SIZE[0] * GRPH_SIZE[1]):
        game_map.add_node()

    for i in range(GRPH_SIZE[0]):
        for j in range(GRPH_SIZE[1]):
            # Straight edges
            if j < GRPH_SIZE[1]-1:
                game_map.add_edge_between(i*GRPH_SIZE[1]+j, i*GRPH_SIZE[1]+j+1)
            if i < GRPH_SIZE[0]-1:
                game_map.add_edge_between(i*GRPH_SIZE[1]+j, (i+1)*GRPH_SIZE[1]+j)

def draw_grid(screen: pg.Surface) -> None:
    screen.fill(pg.Color('black'))
    for i in range(GRPH_SIZE[0]+1):
        for j in range(GRPH_SIZE[1]+1):
            pg.draw.line(screen, pg.Color('gray33'), (i*NODE_SIZE[0], j*NODE_SIZE[1]), (i*NODE_SIZE[0]+NODE_SIZE[0], j*NODE_SIZE[1]), 1)
            pg.draw.line(screen, pg.Color('gray33'), (i*NODE_SIZE[0], j*NODE_SIZE[1]), (i*NODE_SIZE[0], j*NODE_SIZE[1]+NODE_SIZE[1]), 1)

def cursor_pos_to_selection(cursor_pos: Tuple[int, int]) -> Tuple[int, int]:
    node_x = int((cursor_pos[0] / SCR_SIZE[0]) * GRPH_SIZE[0]) * NODE_SIZE[0]
    node_y = int((cursor_pos[1] / SCR_SIZE[1]) * GRPH_SIZE[1]) * NODE_SIZE[1]
    return node_x, node_y

def load_asset(asset_group: List[str], asset_index: int) -> pg.Surface:
    asset_image = pg.image.load(asset_group[asset_index]).convert_alpha()
    print(f"Original asset size: {asset_image.get_size()}")
    scaled_image = pg.transform.scale(asset_image, (NODE_SIZE[0]-2, NODE_SIZE[1]-2))
    print(f"Scaled asset size: {scaled_image.get_size()}")
    return scaled_image

pg.init()
screen: pg.Surface = pg.display.set_mode((SCR_SIZE[0]+1, SCR_SIZE[1]+1))
draw_grid(screen)
pg.mouse.set_visible(False)
pg.display.set_caption('PacMan Map Builder')
clock: pg.time.Clock = pg.time.Clock()

asset_group: List[str] = assets.DOUBLE_WALLS
asset_index: int = 0
asset_image: pg.Surface = load_asset(asset_group, asset_index)

running: bool = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEWHEEL:
            if event.y < 0:
                asset_index = (asset_index + 1) % len(asset_group)
            else:
                asset_index = (asset_index - 1) % len(asset_group)
            asset_image: pg.Surface = load_asset(asset_group, asset_index)

    draw_grid(screen)
    
    cursor_pos: Tuple[int, int] = pg.mouse.get_pos()
    node_x, node_y = cursor_pos_to_selection(cursor_pos)
    screen.blit(asset_image, (node_x, node_y))
    # Draw a red rectangle around the asset for debugging
    rect = pg.Rect(node_x, node_y, NODE_SIZE[0]-2, NODE_SIZE[1]-2)
    pg.draw.rect(screen, (255, 0, 0), rect, 1)
    
    pg.display.flip()
    clock.tick(60)

pg.quit()
