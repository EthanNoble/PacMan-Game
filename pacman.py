import pygame as pg
from graph import Graph
from typing import Tuple, List
from ghost import Ghost

# Number of nodes in graph (W, H)
GRPH_SIZE = (28, 36)
# Size of each node in pixels
NODE_SIZE = (26, 26)
# Size of the window in pixels
SCR_SIZE = (GRPH_SIZE[0] * NODE_SIZE[0], GRPH_SIZE[1] * NODE_SIZE[1])
# Offset for game map graph
OFFSET = (NODE_SIZE[0]//2, NODE_SIZE[1]//2)

def init_map(map_assets: List[Tuple[str, bool]]) -> Graph:
    game_map = Graph()
    for _ in range(GRPH_SIZE[0] * GRPH_SIZE[1]):
        game_map.add_node()

    for node in range(len(map_assets)):
        if map_assets[node][1]:
            node_above: int | None = node - (GRPH_SIZE[0]) if node >= GRPH_SIZE[0] else None
            node_below: int | None = node + (GRPH_SIZE[0]) if node < (GRPH_SIZE[0]*GRPH_SIZE[1] - GRPH_SIZE[0]) else None
            node_left: int | None = node - 1 if node % GRPH_SIZE[0] > 0 else None
            node_right: int | None = node + 1 if node % GRPH_SIZE[0] < (GRPH_SIZE[0]-1) else None
            if node_left is not None and map_assets[node_left][1]:
                game_map.add_edge_between(node, node_left)
            if node_right is not None and map_assets[node_right][1]:
                game_map.add_edge_between(node, node_right)
            if node_above is not None and map_assets[node_above][1]:
                game_map.add_edge_between(node, node_above)
            if node_below is not None and map_assets[node_below][1]:
                game_map.add_edge_between(node, node_below)
    return game_map

def draw_map(screen, game_map):
    for node_num in game_map.adj_list:
        if len(game_map.neighbors_of(node_num)) > 0:
            draw_node(screen, pg.Color('gray33'), node_num)
            for neighbor in game_map.neighbors_of(node_num):
                node_x, node_y = node_number_to_cursor_pos(node_num)
                x_neighbor, y_neighbor = node_number_to_cursor_pos(neighbor)
                pg.draw.line(screen, pg.Color('gray33'), (node_x+OFFSET[0], node_y+OFFSET[1]), (x_neighbor+OFFSET[0], y_neighbor+OFFSET[1]), 1)

def draw_path(screen, path, color: pg.Color):
    for i in range(len(path)):
        draw_node(screen, color, path[i])
        if i < len(path)-1:
            position = node_number_to_cursor_pos(path[i])
            x_n = path[i+1] % GRPH_SIZE[0]
            y_n = path[i+1] // GRPH_SIZE[0]
            pg.draw.line(screen, color, (position[0]+OFFSET[0], position[1]+OFFSET[1]), (x_n*NODE_SIZE[0]+OFFSET[0], y_n*NODE_SIZE[1]+OFFSET[1]), 1)

def draw_node(screen, col, node_num):
        x, y = node_number_to_cursor_pos(node_num)
        pg.draw.circle(screen, col, (x+OFFSET[0], y+OFFSET[1]), 3, 0)
        # draw node number on screen
        # font = pg.font.Font(None, 18)
        # text = font.render(str(node_num), True, pg.Color('white'))
        # screen.blit(text, (x, y))

def draw_grid(screen: pg.Surface, map_assets: List[Tuple[str, bool]]) -> None:
    screen.fill(pg.Color('black'))

    for i in range(len(map_assets)):
        position: Tuple[int, int] = node_number_to_cursor_pos(i)

        # Draw image asset
        if map_assets[i][0]:
            place_image(screen, load_asset(asset_path=map_assets[i][0]), position)


        # # Draw graph node
        # if map_assets[i][1]:
        #     draw_rect_alpha(screen, (0, 255, 0, 100), (position[0], position[1], NODE_SIZE[0], NODE_SIZE[1]))

def cursor_pos_to_selection(cursor_pos: Tuple[int, int]) -> Tuple[int, int]:
    node_x = int((cursor_pos[0] / SCR_SIZE[0]) * GRPH_SIZE[0]) * NODE_SIZE[0]
    node_y = int((cursor_pos[1] / SCR_SIZE[1]) * GRPH_SIZE[1]) * NODE_SIZE[1]
    return node_x, node_y

def cursor_pos_to_node_number(cursor_pos: Tuple[int, int]) -> int:
    node_x, node_y = cursor_pos_to_selection(cursor_pos)
    return node_x // NODE_SIZE[0] + (node_y // NODE_SIZE[1]) * GRPH_SIZE[0]

def node_number_to_cursor_pos(node_number: int) -> Tuple[int, int]:
    node_x = (node_number % GRPH_SIZE[0]) * NODE_SIZE[0]
    node_y = (node_number // GRPH_SIZE[0]) * NODE_SIZE[1]
    return node_x, node_y

def load_asset(*, group: List[str] = [], index: int = -1, asset_path: str = '') -> pg.Surface:
        if group and index > -1:
            asset_image = pg.image.load(group[index])
        elif asset_path:
            asset_image = pg.image.load(asset_path)
        else:
            raise ValueError("No valid asset path or group provided.")

        scaled_image = pg.transform.scale(asset_image, (NODE_SIZE[0], NODE_SIZE[1]))
        return scaled_image

def place_image(screen: pg.Surface, image: pg.Surface, position: Tuple[int, int]) -> None:
    screen.blit(image, (position[0], position[1]))

def draw_rect_alpha(screen: pg.Surface, color: Tuple[int, int, int, int], rect: Tuple[int, int, int, int]) -> None:
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)

def load_map_from_file(file_path: str) -> List[Tuple[str, bool]]:
    with open(file_path, 'r') as f:
        lines: List[str] = f.readlines()
        map_assets: List[Tuple[str, bool]] = []
        for line in lines:
            asset_path, is_graph_node = line.strip().split(',')
            map_assets.append((asset_path, is_graph_node == 'True'))
        return map_assets

def main() -> None:
    pg.init()
    screen: pg.Surface = pg.display.set_mode((SCR_SIZE[0]+1, SCR_SIZE[1]+1))
    pg.display.set_caption('PacMan')
    clock: pg.time.Clock = pg.time.Clock()

    map_assets: List[Tuple[str, bool]] = load_map_from_file('maps/pacmap.txt')

    # For player and enemy movement
    map: Graph = init_map(map_assets)

    ghosts: List[Ghost] = [
        Ghost(color=pg.Color('cyan'), position=113, target=830, map=map),
        Ghost(color=pg.Color('red'), position=897, target=138, map=map)
    ]

    running: bool = True
    while running:
        draw_grid(screen, map_assets)
        draw_map(screen, map)
        # draw_path(screen, map.BFS(113, 830))

        for ghost in ghosts:
            new_node: int = ghost.move()
            position: Tuple[int, int] = node_number_to_cursor_pos(new_node)
            pg.draw.circle(screen, ghost.get_color(), (position[0]+OFFSET[0], position[1]+OFFSET[1]), 10, 0)
            # draw_path(screen, ghost.get_path(), ghost.get_color())

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                pass
                

        pg.display.flip()
        clock.tick(60)

    pg.quit()
