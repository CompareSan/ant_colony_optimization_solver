from __future__ import annotations

from typing import (
    Any,
    List,
    Tuple,
)


class Cell:
    def __init__(
        self,
        coordinates: Tuple[int, int],
        pheromone: float = 0,
    ) -> None:
        self.coordinates = coordinates
        self.pheromone = pheromone
        self.connected_cells: List[Cell] = []

    def add_connected_cell(self, cell: Cell) -> None:
        if cell not in self.connected_cells:
            self.connected_cells.append(cell)

    def set_pheromone(self, pheromone: float) -> None:
        self.pheromone = pheromone

    def update_pheromone(self, ants: List[Any], rho: float = 0.1) -> None:
        self.pheromone = (1 - rho) * self.pheromone + sum(
            [1 / ant.get_path_length() for ant in ants if self in ant.path]
        )
