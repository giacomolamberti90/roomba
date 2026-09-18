from typing import Dict, List, Optional, Tuple

from .robot import Roomba

GRID_SIZE = 10


class Grid:
    def __init__(self, size: int = GRID_SIZE):
        self.size = size

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def render(self, roombas: Dict[int, Roomba], selected_id: Optional[int] = None) -> str:
        occupants = {}  # type: Dict[Tuple[int, int], Roomba]
        for rid, roomba in sorted(roombas.items()):
            cell = (roomba.x, roomba.y)
            if cell not in occupants or rid == selected_id:
                occupants[cell] = roomba
        rows = []
        for y in range(self.size - 1, -1, -1):
            cells = []
            for x in range(self.size):
                roomba = occupants.get((x, y))
                cells.append(roomba.facing.symbol if roomba is not None else ".")
            rows.append(" ".join(cells))
        return "\n".join(rows)


class Simulator:
    def __init__(self, roomba: Roomba = None, grid: Grid = None):
        self.grid = grid if grid is not None else Grid()
        start = roomba if roomba is not None else Roomba()
        self._roombas = {1: start}  # type: Dict[int, Roomba]
        self.selected_id = 1  # type: Optional[int]
        self._next_id = 2

    @property
    def roomba(self) -> Optional[Roomba]:
        if self.selected_id is None:
            return None
        return self._roombas.get(self.selected_id)

    def create(self) -> int:
        rid = self._next_id
        self._next_id += 1
        self._roombas[rid] = Roomba()
        if self.selected_id is None:
            self.selected_id = rid
        return rid

    def select(self, rid: int) -> str:
        if rid not in self._roombas:
            return "not_found"
        self.selected_id = rid
        return "ok"

    def delete(self, rid: int) -> str:
        if rid not in self._roombas:
            return "not_found"
        del self._roombas[rid]
        if self.selected_id == rid:
            self.selected_id = min(self._roombas) if self._roombas else None
        return "ok"

    def list_roombas(self) -> List[Tuple[int, Roomba]]:
        return [(rid, self._roombas[rid]) for rid in sorted(self._roombas)]

    def can_enter(self, x: int, y: int) -> bool:
        return self.grid.in_bounds(x, y)

    def turn_right(self) -> str:
        if self.roomba is None:
            return "no_selection"
        self.roomba.turn_right()
        return "ok"

    def forward(self) -> str:
        if self.roomba is None:
            return "no_selection"
        nx, ny = self.roomba.cell_ahead()
        if self.can_enter(nx, ny):
            self.roomba.move_to(nx, ny)
        else:
            self.roomba.turn_right()
        return "ok"

    def render(self) -> str:
        return self.grid.render(self._roombas, self.selected_id)
