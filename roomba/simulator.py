from .robot import Roomba

GRID_SIZE = 10


class Grid:
    def __init__(self, size: int = GRID_SIZE):
        self.size = size

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def render(self, roomba: Roomba) -> str:
        rows = []
        for y in range(self.size - 1, -1, -1):
            cells = []
            for x in range(self.size):
                if x == roomba.x and y == roomba.y:
                    cells.append(roomba.facing.symbol)
                else:
                    cells.append(".")
            rows.append(" ".join(cells))
        return "\n".join(rows)


class Simulator:
    def __init__(self, roomba: Roomba = None, grid: Grid = None):
        self.grid = grid if grid is not None else Grid()
        self.roomba = roomba if roomba is not None else Roomba()

    def can_enter(self, x: int, y: int) -> bool:
        return self.grid.in_bounds(x, y)

    def turn_right(self) -> None:
        self.roomba.turn_right()

    def forward(self) -> None:
        for _ in range(4):
            nx, ny = self.roomba.cell_ahead()
            if self.can_enter(nx, ny):
                self.roomba.move_to(nx, ny)
                return
            self.roomba.turn_right()

    def render(self) -> str:
        return self.grid.render(self.roomba)
