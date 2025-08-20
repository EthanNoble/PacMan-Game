from typing import List
from graph import Graph
from pygame import Color

class Ghost:
    def __init__(self, color: Color, position: int, target: int, map: Graph):
        self.color: Color = color
        self.position: int = position
        self.target: int = target
        self.path: List[int] = map.BFS(self.position, self.target)

    def move(self) -> int:
        if self.path:
            self.position = self.path.pop(0)
        return self.position

    def update_target(self, new_target: int, map: Graph):
        self.target = new_target
        self.path = map.BFS(self.position, self.target)

    def get_path(self) -> List[int]:
        return self.path

    def get_color(self) -> Color:
        return self.color