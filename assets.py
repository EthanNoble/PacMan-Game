from typing import List

DIR: str = 'images/walls/'
DIR2: str = 'images/pellets/'
DIR3: str = 'images/characters/'

# CHARACTERS
BLINKY1: str = DIR3 + 'blinky1.png'
BLINKY2: str = DIR3 + 'blinky2.png'

PINKY1: str = DIR3 + 'pinky1.png'
PINKY2: str = DIR3 + 'pinky2.png'

INKY1: str = DIR3 + 'inky1.png'
INKY2: str = DIR3 + 'inky2.png'

CLYDE1: str = DIR3 + 'clyde1.png'
CLYDE2: str = DIR3 + 'clyde2.png'

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
