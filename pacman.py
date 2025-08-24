import pygame as pg
from typing import Tuple, List, Set, Dict
from characters import Ghost, PacMan, Direction, GhostName, GhostMode
import common

def legal_tiles(map_assets: List[Tuple[pg.Surface | None, bool]]) -> Set[int]:
    legal_tiles: Set[int] = set()

    for node_num in range(len(map_assets)):
        if map_assets[node_num][1]:
            # This will give us a direct way to determine
            # if a tile belongs to the set of legal tiles
            legal_tiles.add(node_num)
    return legal_tiles

def draw_tile_nums(screen) -> None:
    for tile_num in range(common.TILE_DIMS[0] * common.TILE_DIMS[1]):
        # Prints every so or so node number (degrades performance significantly)
        if tile_num % 5 == 0:
            x, y = common.node_number_to_cursor_pos(tile_num)
            font = pg.font.Font(None, 14)
            text = font.render(str(tile_num), True, pg.Color('white'))
            screen.blit(text, (x + common.OFFSET[0], y + common.OFFSET[1]))

def draw_path(screen, path, color: pg.Color):
    for i in range(len(path)):
        if i < len(path)-1:
            position = common.node_number_to_cursor_pos(path[i])
            x_n = path[i+1] % common.TILE_DIMS[0]
            y_n = path[i+1] // common.TILE_DIMS[0]
            pg.draw.line(screen, color, (position[0]+common.OFFSET[0], position[1]+common.OFFSET[1]), (x_n*common.TILE_SIZE[0]+common.OFFSET[0], y_n*common.TILE_SIZE[1]+common.OFFSET[1]), 1)

def draw_grid(screen: pg.Surface, map_assets: List[Tuple[pg.Surface | None, bool]]) -> None:
    screen.fill(pg.Color('black'))

    for i in range(len(map_assets)):
        position: Tuple[int, int] = common.node_number_to_cursor_pos(i)
        # Draw image asset
        if map_assets[i][0]:
            common.place_image(screen, map_assets[i][0], position)
    
    if common.SHOW_GRID_LINES:
        for i in range(common.TILE_DIMS[0]+1):
            for j in range(common.TILE_DIMS[1]+1):
                pg.draw.line(screen, pg.Color('gray33'), (i*common.TILE_SIZE[0], j*common.TILE_SIZE[1]), (i*common.TILE_SIZE[0]+common.TILE_SIZE[0], j*common.TILE_SIZE[1]), 1)
                pg.draw.line(screen, pg.Color('gray33'), (i*common.TILE_SIZE[0], j*common.TILE_SIZE[1]), (i*common.TILE_SIZE[0], j*common.TILE_SIZE[1]+common.TILE_SIZE[1]), 1)

def load_map_from_file(file_path: str) -> List[Tuple[pg.Surface | None, bool]]:
    with open(file_path, 'r') as f:
        lines: List[str] = f.readlines()
        map_assets: List[Tuple[pg.Surface | None, bool]] = []
        for line in lines:
            asset_path, is_graph_node = line.strip().split(',')
            asset: pg.Surface | None = common.load_asset(asset_path) if asset_path and 'pellet' not in asset_path else None
            map_assets.append((asset, is_graph_node == 'True'))
        return map_assets

def main() -> None:
    pg.init()
    screen: pg.Surface = pg.display.set_mode((common.SCR_SIZE[0]+1, common.SCR_SIZE[1]+1))
    pg.display.set_caption('PacMan')
    clock: pg.time.Clock = pg.time.Clock()

    # Data concerning the images drawn to the map
    # Each element is a tuple (surface, is_graph_node AKA is legal tile)
    map_assets: List[Tuple[pg.Surface | None, bool]] = load_map_from_file('maps/pacmap.txt')

    # Set of legal tiles (accessible by pacman or the ghosts)
    legal_space: Set[int] = legal_tiles(map_assets)

    pacman: PacMan = PacMan(start_node=574, legal_tiles=legal_space)

    ghosts: Dict[str, Ghost] = {
        'Blinky': Ghost(name=GhostName.BLINKY, current_node=138, scatter_target_node=25),
        'Pinky': Ghost(name=GhostName.PINKY, current_node=113, scatter_target_node=2),
        'Inky': Ghost(name=GhostName.INKY, current_node=922, scatter_target_node=979),
        'Clyde': Ghost(name=GhostName.CLYDE, current_node=897, scatter_target_node=952)
    }

    running: bool = True
    while running:
        draw_grid(screen, map_assets)
        if common.SHOW_TILE_NUMS:
            draw_tile_nums(screen)

        pacman.smooth_move()
        pacman.render(screen)

        for ghost in ghosts.values():
            ghost.choose_target_tile(blinky=ghosts['Blinky'], pacman=pacman)
            ghost.smooth_move(legal_space)
            ghost.render(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    pacman.direction = Direction.UP
                elif event.key == pg.K_DOWN:
                    pacman.direction = Direction.DOWN
                elif event.key == pg.K_LEFT:
                    pacman.direction = Direction.LEFT
                elif event.key == pg.K_RIGHT:
                    pacman.direction = Direction.RIGHT
                elif event.key == pg.K_s:
                    for ghost in ghosts.values():
                        ghost.set_mode(GhostMode.SCATTER)
                elif event.key == pg.K_c:
                    for ghost in ghosts.values():
                        ghost.set_mode(GhostMode.CHASE)

        if common.SHOW_FPS:
            pg.display.set_caption(f'PacMan (FPS: {clock.get_fps():.0f})')

        pg.display.flip()
        clock.tick(60)

    pg.quit()
