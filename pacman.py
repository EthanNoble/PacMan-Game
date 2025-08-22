import pygame as pg
from graph import Graph
from typing import Tuple, List, Set
from characters import Ghost, PacMan, Direction, GhostName
import common

# Size of the window in pixels
SCR_SIZE = (common.GRPH_SIZE[0] * common.NODE_SIZE[0], common.GRPH_SIZE[1] * common.NODE_SIZE[1])

def init_map(map_assets: List[Tuple[pg.Surface | None, bool]]) -> Tuple[Graph, Set[int]]:
    game_map = Graph()
    graph_node_cache: Set[int] = set()

    for _ in range(common.GRPH_SIZE[0] * common.GRPH_SIZE[1]):
        game_map.add_node()

    for node in range(len(map_assets)):
        if map_assets[node][1]:
            graph_node_cache.add(node) # This will give us a direct way to determine which nodes are part of the graph
            node_above: int | None = node - (common.GRPH_SIZE[0]) if node >= common.GRPH_SIZE[0] else None
            node_below: int | None = node + (common.GRPH_SIZE[0]) if node < (common.GRPH_SIZE[0]*common.GRPH_SIZE[1] - common.GRPH_SIZE[0]) else None
            node_left: int | None = node - 1 if node % common.GRPH_SIZE[0] > 0 else None
            node_right: int | None = node + 1 if node % common.GRPH_SIZE[0] < (common.GRPH_SIZE[0]-1) else None
            if node_left is not None and map_assets[node_left][1]:
                game_map.add_edge_between(node, node_left)
            if node_right is not None and map_assets[node_right][1]:
                game_map.add_edge_between(node, node_right)
            if node_above is not None and map_assets[node_above][1]:
                game_map.add_edge_between(node, node_above)
            if node_below is not None and map_assets[node_below][1]:
                game_map.add_edge_between(node, node_below)
    return game_map, graph_node_cache

def draw_map(screen, game_map):
    for node_num in game_map.adj_list:
        if len(game_map.neighbors_of(node_num)) > 0:
            draw_node(screen, pg.Color('gray33'), node_num)
            for neighbor in game_map.neighbors_of(node_num):
                node_x, node_y = common.node_number_to_cursor_pos(node_num)
                x_neighbor, y_neighbor = common.node_number_to_cursor_pos(neighbor)
                pg.draw.line(screen, pg.Color('gray33'), (node_x+common.OFFSET[0], node_y+common.OFFSET[1]), (x_neighbor+common.OFFSET[0], y_neighbor+common.OFFSET[1]), 1)

def draw_path(screen, path, color: pg.Color):
    for i in range(len(path)):
        if i < len(path)-1:
            position = common.node_number_to_cursor_pos(path[i])
            x_n = path[i+1] % common.GRPH_SIZE[0]
            y_n = path[i+1] // common.GRPH_SIZE[0]
            pg.draw.line(screen, color, (position[0]+common.OFFSET[0], position[1]+common.OFFSET[1]), (x_n*common.NODE_SIZE[0]+common.OFFSET[0], y_n*common.NODE_SIZE[1]+common.OFFSET[1]), 1)

def draw_node(screen, col, node_num):
        x, y = common.node_number_to_cursor_pos(node_num)
        pg.draw.circle(screen, col, (x+common.OFFSET[0], y+common.OFFSET[1]), 3, 0)
        
        # Prints every so or so node number (degrades performance significantly)
        if node_num % 5 == 0 and common.DEBUG_GRAPH_NODES:
            font = pg.font.Font(None, 14)
            text = font.render(str(node_num), True, pg.Color('white'))
            screen.blit(text, (x, y))

def draw_grid(screen: pg.Surface, map_assets: List[Tuple[pg.Surface | None, bool]]) -> None:
    screen.fill(pg.Color('black'))

    for i in range(len(map_assets)):
        position: Tuple[int, int] = common.node_number_to_cursor_pos(i)
        # Draw image asset
        if map_assets[i][0]:
            common.place_image(screen, map_assets[i][0], position)
    
    if common.DEBUG_MODE:
        for i in range(common.GRPH_SIZE[0]+1):
            for j in range(common.GRPH_SIZE[1]+1):
                pg.draw.line(screen, pg.Color('gray33'), (i*common.NODE_SIZE[0], j*common.NODE_SIZE[1]), (i*common.NODE_SIZE[0]+common.NODE_SIZE[0], j*common.NODE_SIZE[1]), 1)
                pg.draw.line(screen, pg.Color('gray33'), (i*common.NODE_SIZE[0], j*common.NODE_SIZE[1]), (i*common.NODE_SIZE[0], j*common.NODE_SIZE[1]+common.NODE_SIZE[1]), 1)

def cursor_pos_to_selection(cursor_pos: Tuple[int, int]) -> Tuple[int, int]:
    node_x = int((cursor_pos[0] / SCR_SIZE[0]) * common.GRPH_SIZE[0]) * common.NODE_SIZE[0]
    node_y = int((cursor_pos[1] / SCR_SIZE[1]) * common.GRPH_SIZE[1]) * common.NODE_SIZE[1]
    return node_x, node_y

def cursor_pos_to_node_number(cursor_pos: Tuple[int, int]) -> int:
    node_x, node_y = cursor_pos_to_selection(cursor_pos)
    return node_x // common.NODE_SIZE[0] + (node_y // common.NODE_SIZE[1]) * common.GRPH_SIZE[0]

def draw_rect_alpha(screen: pg.Surface, color: Tuple[int, int, int, int], rect: Tuple[int, int, int, int]) -> None:
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)

def load_map_from_file(file_path: str) -> List[Tuple[pg.Surface | None, bool]]:
    
    with open(file_path, 'r') as f:
        lines: List[str] = f.readlines()
        map_assets: List[Tuple[pg.Surface | None, bool]] = []
        for line in lines:
            asset_path, is_graph_node = line.strip().split(',')
            asset: pg.Surface | None = common.load_asset(asset_path) if asset_path else None
            map_assets.append((asset, is_graph_node == 'True'))
        return map_assets

def main() -> None:
    pg.init()
    screen: pg.Surface = pg.display.set_mode((SCR_SIZE[0]+1, SCR_SIZE[1]+1))
    pg.display.set_caption('PacMan')
    clock: pg.time.Clock = pg.time.Clock()

    map_assets: List[Tuple[pg.Surface | None, bool]] = load_map_from_file('maps/pacmap.txt')

    # For player and enemy movement
    map, graph_nodes = init_map(map_assets)


    pacman: PacMan = PacMan(color=pg.Color('yellow'), start_node=574, graph_nodes=graph_nodes)

    ghosts: List[Ghost] = [
        Ghost(name=GhostName.BLINKY, current_node=113),
        Ghost(name=GhostName.PINKY, current_node=897),
        # Ghost(name=GhostName.INKY, current_node=922),
        # Ghost(name=GhostName.CLYDE, current_node=901)
    ]

    running: bool = True
    while running:
        draw_grid(screen, map_assets)
        if common.DEBUG_MODE:
            draw_map(screen, map)
        
        # Smooth PacMan movement
        if pacman.pixel_pos == pacman.target_pixel_pos:
            next_node: int = pacman.move_to_next_node()
            target_pos: Tuple[int, int] = common.node_number_to_cursor_pos(next_node)
            pacman.target_pixel_pos = (target_pos[0] + common.OFFSET[0], target_pos[1] + common.OFFSET[1])

        pacman_speed = 2
        dx = pacman.target_pixel_pos[0] - pacman.pixel_pos[0]
        dy = pacman.target_pixel_pos[1] - pacman.pixel_pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > pacman_speed:
            pacman.pixel_pos = (pacman.pixel_pos[0] + pacman_speed * dx / dist, pacman.pixel_pos[1] + pacman_speed * dy / dist)
        else:
            pacman.pixel_pos = pacman.target_pixel_pos[:]

        pg.draw.circle(screen, pacman.get_color(), (int(pacman.pixel_pos[0]), int(pacman.pixel_pos[1])), 10, 0)

        for ghost in ghosts:
            # Targeting PacMan directly
            if ghost.name == GhostName.BLINKY:
                if ghost.get_target_node() != pacman.get_current_node():
                    ghost.set_target_node(pacman.get_current_node(), map)
            # Targeting PacMan from the front (two nodes ahead)
            if ghost.name == GhostName.PINKY:
                pacman_node: int = pacman.get_current_node()
                ignored_nodes: Set[int] = set()

                dx = ghost.pixel_pos[0] - pacman.pixel_pos[0]
                dy = ghost.pixel_pos[1] - pacman.pixel_pos[1]
                dist_to_pacman = (dx ** 2 + dy ** 2) ** 0.5
                
                # If the distance to pacman is greater than some amount,
                # then ignore some nodes during pathfinding to ambush in
                # front of pacman instead of directly behind. Else, if
                # Pinky is close to pacman, just go straight for it.
                if dist_to_pacman > 100:
                    if pacman.direction == Direction.UP:
                        # Ignore the node directly below PacMan when pathfinding
                        ignored_nodes.add(pacman_node + (common.GRPH_SIZE[0]))
                    elif pacman.direction == Direction.DOWN:
                        # Ignore the node directly above PacMan when pathfinding
                        ignored_nodes.add(pacman_node - (common.GRPH_SIZE[0]))
                    elif pacman.direction == Direction.LEFT:
                        # Ignore the node directly to the right of PacMan when pathfinding
                        ignored_nodes.add(pacman_node + 1)
                    elif pacman.direction == Direction.RIGHT:
                        # Ignore the node directly to the right of PacMan when pathfinding
                        ignored_nodes.add(pacman_node - 1)
                
                if ghost.get_target_node() != pacman.get_current_node():
                    ghost.set_target_node(pacman.get_current_node(), map, ignored_nodes=ignored_nodes)
                    ignored_nodes.clear()  # Clear ignored nodes after setting target

            # Only move to next node when ghost has reached its target pixel position
            if ghost.pixel_pos == ghost.target_pixel_pos:
                new_node: int = ghost.move_to_next_node()
                target_pos = common.node_number_to_cursor_pos(new_node)
                ghost.target_pixel_pos = (target_pos[0] + common.OFFSET[0], target_pos[1] + common.OFFSET[1])

            # Set speed in pixels per frame
            speed = 2

            # Calculate direction vector
            dx = ghost.target_pixel_pos[0] - ghost.pixel_pos[0]
            dy = ghost.target_pixel_pos[1] - ghost.pixel_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist > speed:
                ghost.pixel_pos = (ghost.pixel_pos[0] + speed * dx / dist, ghost.pixel_pos[1] + speed * dy / dist)
            else:
                ghost.pixel_pos = ghost.target_pixel_pos[:]

            # pg.draw.circle(screen, pg.Color('red'), (int(ghost.pixel_pos[0]), int(ghost.pixel_pos[1])), 10, 0)
            common.place_image(
                screen,
                ghost.get_body_image(),
                (int(ghost.pixel_pos[0] - common.OFFSET[0]*ghost.scale), int(ghost.pixel_pos[1] - common.OFFSET[1]*ghost.scale)))
            ghost.animate()

            if common.DEBUG_MODE:
                draw_path(screen, ghost.get_path(), ghost.get_color())

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    pacman.set_direction(Direction.UP)
                elif event.key == pg.K_DOWN:
                    pacman.set_direction(Direction.DOWN)
                elif event.key == pg.K_LEFT:
                    pacman.set_direction(Direction.LEFT)
                elif event.key == pg.K_RIGHT:
                    pacman.set_direction(Direction.RIGHT)

        if common.DEBUG_MODE:
            pg.display.set_caption(f'PacMan (FPS: {clock.get_fps():.0f})')

        pg.display.flip()
        clock.tick(60)

    pg.quit()
