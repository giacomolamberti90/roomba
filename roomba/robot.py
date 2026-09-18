from dataclasses import dataclass
from typing import Tuple

from .direction import Direction


@dataclass
class Roomba:
    x: int = 0
    y: int = 0
    facing: Direction = Direction.NORTH

    def turn_right(self) -> None:
        self.facing = self.facing.turn_right()

    def cell_ahead(self) -> Tuple[int, int]:
        dx, dy = self.facing.delta
        return self.x + dx, self.y + dy

    def move_to(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
