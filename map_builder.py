import pygame as pg
import assets
from tk import tk_save_dialog

from typing import Tuple, List, IO


# Number of nodes in graph (W, H)
GRPH_SIZE = (28, 36)
# Size of each node in pixels
NODE_SIZE = (26, 26)
# Size of the window in pixels
SCR_SIZE = (GRPH_SIZE[0] * NODE_SIZE[0], GRPH_SIZE[1] * NODE_SIZE[1])

def draw_grid(screen: pg.Surface, map_assets: List[Tuple[str, bool]]) -> None:
    screen.fill(pg.Color('black'))

    for i in range(len(map_assets)):
        position: Tuple[int, int] = node_number_to_cursor_pos(i)

        # Draw image asset
        if map_assets[i][0]:
            place_image(screen, load_asset(asset_path=map_assets[i][0]), position)

        # Draw graph node
        if map_assets[i][1]:
            draw_rect_alpha(screen, (0, 255, 0, 100), (position[0], position[1], NODE_SIZE[0], NODE_SIZE[1]))
    
    for i in range(GRPH_SIZE[0]+1):
        for j in range(GRPH_SIZE[1]+1):
            pg.draw.line(screen, pg.Color('gray33'), (i*NODE_SIZE[0], j*NODE_SIZE[1]), (i*NODE_SIZE[0]+NODE_SIZE[0], j*NODE_SIZE[1]), 1)
            pg.draw.line(screen, pg.Color('gray33'), (i*NODE_SIZE[0], j*NODE_SIZE[1]), (i*NODE_SIZE[0], j*NODE_SIZE[1]+NODE_SIZE[1]), 1)

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

def save_map_to_file(map_assets: List[Tuple[str, bool]], file_path: str) -> None:
    with open(file_path, 'w') as f:
        for asset in map_assets:
            f.write(f'{asset[0]},{asset[1]}\n')

def load_map_from_file(file_path: str) -> List[Tuple[str, bool]]:
    with open(file_path, 'r') as f:
        lines: List[str] = f.readlines()
        map_assets: List[Tuple[str, bool]] = []
        for line in lines:
            asset_path, is_graph_node = line.strip().split(',')
            map_assets.append((asset_path, is_graph_node == 'True'))
        return map_assets

def main(map_file_path: str | None = None) -> None:
    pg.init()
    screen: pg.Surface = pg.display.set_mode((SCR_SIZE[0]+1, SCR_SIZE[1]+1))
    pg.mouse.set_visible(False)
    pg.display.set_caption('PacMan Map Builder (Ctr+S to Save to File)')
    clock: pg.time.Clock = pg.time.Clock()

    asset_group: List[str] = assets.PELLETS
    asset_index: int = 0
    asset_image: pg.Surface = load_asset(group=asset_group, index=asset_index)

    if not map_file_path:
        map_assets: List[Tuple[str, bool]] = [('', False) for _ in range(GRPH_SIZE[0]*GRPH_SIZE[1])]
    else:
        map_assets: List[Tuple[str, bool]] = load_map_from_file(map_file_path)
    draw_grid(screen, map_assets)

    running: bool = True
    while running:
        draw_grid(screen, map_assets)

        cursor_pos: Tuple[int, int] = pg.mouse.get_pos()
        node_x, node_y = cursor_pos_to_selection(cursor_pos)

        # Draw hovering asset image
        if asset_index > -1:
            place_image(screen, asset_image, (node_x, node_y))
        # Draw hovering graph node
        elif asset_index == -1: 
            draw_rect_alpha(screen, (0, 255, 0, 100), (node_x, node_y, NODE_SIZE[0], NODE_SIZE[1]))
        
        # Draw current selection area
        pg.draw.rect(screen, pg.Color('gray40'), (node_x, node_y, NODE_SIZE[0]+1, NODE_SIZE[1]+1), 2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                # Ctrl+S to save the map to a file
                if event.key == pg.K_s and (pg.key.get_mods() & pg.KMOD_CTRL):
                    save: IO[str] | None = tk_save_dialog()
                    if save:
                        file_path = save.name
                        save_map_to_file(map_assets, file_path)
                # Graph asset (allows placement of graph nodes)
                if event.key == pg.K_1:
                    asset_index = -1
                # Image assets
                if event.key == pg.K_2:
                    asset_index = 0
                    asset_group = assets.PELLETS
                    asset_image = load_asset(group=asset_group, index=asset_index)
                if event.key == pg.K_3:
                    asset_index = 0
                    asset_group = assets.SINGLE_WALLS
                    asset_image = load_asset(group=asset_group, index=asset_index)
                elif event.key == pg.K_4:
                    asset_index = 0
                    asset_group = assets.DOUBLE_WALLS
                    asset_image = load_asset(group=asset_group, index=asset_index)
                elif event.key == pg.K_5:
                    asset_index = 0
                    asset_group = assets.SMALL_CORNER_WALLS
                    asset_image = load_asset(group=asset_group, index=asset_index)
                elif event.key == pg.K_6:
                    asset_index = 0
                    asset_group = assets.LARGE_CORNER_WALLS
                    asset_image = load_asset(group=asset_group, index=asset_index)
                elif event.key == pg.K_7:
                    asset_index = 0
                    asset_group = assets.DOUBLE_CORNER_WALLS
                    asset_image = load_asset(group=asset_group, index=asset_index)

            # Asset rotation
            if event.type == pg.MOUSEWHEEL:
                if event.y < 0:
                    asset_index = (asset_index + 1) % len(asset_group)
                else:
                    asset_index = (asset_index - 1) % len(asset_group)
                asset_image = load_asset(group=asset_group, index=asset_index)

            # Drag and drop insert (left mouse hold)
            if pg.mouse.get_pressed()[0]:
                cursor_pos: Tuple[int, int] = pg.mouse.get_pos()
                node_x, node_y = cursor_pos_to_selection(cursor_pos)
                node_num: int = cursor_pos_to_node_number(cursor_pos)
                if asset_index > -1:
                    map_assets[node_num] = (asset_group[asset_index], map_assets[node_num][1])
                elif asset_index == -1: # Placing graph nodes
                    map_assets[node_num] = (map_assets[node_num][0], True)

            # Drag and drop clear (right mouse hold)
            if pg.mouse.get_pressed()[2]:
                cursor_pos: Tuple[int, int] = pg.mouse.get_pos()
                node_num: int = cursor_pos_to_node_number(cursor_pos)
                map_assets[node_num] = ('', False)

        pg.display.flip()
        clock.tick(60)

    pg.quit()
