from typing import List

DIR: str = 'images/walls/'
DIR2: str = 'images/pellets/'
DIR3: str = 'images/characters/'
DIR4: str = 'images/characters/pacman/'

# CHARACTERS
PACMAN1: str = DIR4 + 'pacman1.png'
PACMAN2_LEFT: str = DIR4 + 'pacman2_left.png'
PACMAN2_RIGHT: str = DIR4 + 'pacman2_right.png'
PACMAN2_UP: str = DIR4 + 'pacman2_up.png'
PACMAN2_DOWN: str = DIR4 + 'pacman2_down.png'
PACMAN3_LEFT: str = DIR4 + 'pacman3_left.png'
PACMAN3_RIGHT: str = DIR4 + 'pacman3_right.png'
PACMAN3_UP: str = DIR4 + 'pacman3_up.png'
PACMAN3_DOWN: str = DIR4 + 'pacman3_down.png'

BLINKY1_RIGHT: str = DIR3 + 'blinky1_right.png'
BLINKY1_LEFT: str = DIR3 + 'blinky1_left.png'
BLINKY1_UP: str = DIR3 + 'blinky1_up.png'
BLINKY1_DOWN: str = DIR3 + 'blinky1_down.png'
BLINKY2_RIGHT: str = DIR3 + 'blinky2_right.png'
BLINKY2_LEFT: str = DIR3 + 'blinky2_left.png'
BLINKY2_UP: str = DIR3 + 'blinky2_up.png'
BLINKY2_DOWN: str = DIR3 + 'blinky2_down.png'

PINKY1_RIGHT: str = DIR3 + 'pinky1_right.png'
PINKY1_LEFT: str = DIR3 + 'pinky1_left.png'
PINKY1_UP: str = DIR3 + 'pinky1_up.png'
PINKY1_DOWN: str = DIR3 + 'pinky1_down.png'
PINKY2_RIGHT: str = DIR3 + 'pinky2_right.png'
PINKY2_LEFT: str = DIR3 + 'pinky2_left.png'
PINKY2_UP: str = DIR3 + 'pinky2_up.png'
PINKY2_DOWN: str = DIR3 + 'pinky2_down.png'

INKY1_RIGHT: str = DIR3 + 'inky1_right.png'
INKY1_LEFT: str = DIR3 + 'inky1_left.png'
INKY1_UP: str = DIR3 + 'inky1_up.png'
INKY1_DOWN: str = DIR3 + 'inky1_down.png'
INKY2_RIGHT: str = DIR3 + 'inky2_right.png'
INKY2_LEFT: str = DIR3 + 'inky2_left.png'
INKY2_UP: str = DIR3 + 'inky2_up.png'
INKY2_DOWN: str = DIR3 + 'inky2_down.png'

CLYDE1_RIGHT: str = DIR3 + 'clyde1_right.png'
CLYDE1_LEFT: str = DIR3 + 'clyde1_left.png'
CLYDE1_UP: str = DIR3 + 'clyde1_up.png'
CLYDE1_DOWN: str = DIR3 + 'clyde1_down.png'
CLYDE2_RIGHT: str = DIR3 + 'clyde2_right.png'
CLYDE2_LEFT: str = DIR3 + 'clyde2_left.png'
CLYDE2_UP: str = DIR3 + 'clyde2_up.png'
CLYDE2_DOWN: str = DIR3 + 'clyde2_down.png'

EYE1: str = DIR3 + 'eyes1.png'
EYE2: str = DIR3 + 'eyes2.png'
EYE3: str = DIR3 + 'eyes3.png'
EYE4: str = DIR3 + 'eyes4.png'

# PELLETS
PELLET: str = DIR2 + 'small_pellet.jpg'
POWER_PELLET: str = DIR2 + 'pellet_power.jpg'

PELLETS: List[str] = [
    PELLET,
    POWER_PELLET
]

# WALLS #
SINGLE_WALL_LEFT: str = DIR + 'single_wall_left.jpg'
SINGLE_WALL_RIGHT: str = DIR + 'single_wall_right.jpg'
SINGLE_WALL_UP: str = DIR + 'single_wall_up.jpg'
SINGLE_WALL_DOWN: str = DIR + 'single_wall_down.jpg'
DOUBLE_WALL_LEFT: str = DIR + 'double_wall_left.jpg'
DOUBLE_WALL_RIGHT: str = DIR + 'double_wall_right.jpg'
DOUBLE_WALL_UP: str = DIR + 'double_wall_up.jpg'
DOUBLE_WALL_DOWN: str = DIR + 'double_wall_down.jpg'

# CORNER WALLS #
SMALL_CORNER_WALL_UP_LEFT: str = DIR + 'small_corner_wall_up_left.jpg'
SMALL_CORNER_WALL_UP_RIGHT: str = DIR + 'small_corner_wall_up_right.jpg'
SMALL_CORNER_WALL_DOWN_LEFT: str = DIR + 'small_corner_wall_down_left.jpg'
SMALL_CORNER_WALL_DOWN_RIGHT: str = DIR + 'small_corner_wall_down_right.jpg'
LARGE_CORNER_WALL_UP_LEFT: str = DIR + 'large_corner_wall_up_left.jpg'
LARGE_CORNER_WALL_UP_RIGHT: str = DIR + 'large_corner_wall_up_right.jpg'
LARGE_CORNER_WALL_DOWN_LEFT: str = DIR + 'large_corner_wall_down_left.jpg'
LARGE_CORNER_WALL_DOWN_RIGHT: str = DIR + 'large_corner_wall_down_right.jpg'
DOUBLE_CORNER_WALL_UP_LEFT: str = DIR + 'double_corner_wall_up_left.jpg'
DOUBLE_CORNER_WALL_UP_RIGHT: str = DIR + 'double_corner_wall_up_right.jpg'
DOUBLE_CORNER_WALL_DOWN_LEFT: str = DIR + 'double_corner_wall_down_left.jpg'
DOUBLE_CORNER_WALL_DOWN_RIGHT: str = DIR + 'double_corner_wall_down_right.jpg'

# WALL ROTATIONS #
SINGLE_WALLS: List[str] = [
    SINGLE_WALL_LEFT,
    SINGLE_WALL_UP,
    SINGLE_WALL_RIGHT,
    SINGLE_WALL_DOWN
]

DOUBLE_WALLS: List[str] = [
    DOUBLE_WALL_LEFT,
    DOUBLE_WALL_UP,
    DOUBLE_WALL_RIGHT,
    DOUBLE_WALL_DOWN
]

# CORNER WALL ROTATIONS #
SMALL_CORNER_WALLS: List[str]  = [
    SMALL_CORNER_WALL_UP_LEFT,
    SMALL_CORNER_WALL_UP_RIGHT,
    SMALL_CORNER_WALL_DOWN_RIGHT,
    SMALL_CORNER_WALL_DOWN_LEFT
]

LARGE_CORNER_WALLS: List[str]  = [
    LARGE_CORNER_WALL_UP_LEFT,
    LARGE_CORNER_WALL_UP_RIGHT,
    LARGE_CORNER_WALL_DOWN_RIGHT,
    LARGE_CORNER_WALL_DOWN_LEFT
]

DOUBLE_CORNER_WALLS: List[str]  = [
    DOUBLE_CORNER_WALL_UP_LEFT,
    DOUBLE_CORNER_WALL_UP_RIGHT,
    DOUBLE_CORNER_WALL_DOWN_RIGHT,
    DOUBLE_CORNER_WALL_DOWN_LEFT
]
