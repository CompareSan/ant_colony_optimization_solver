from random import random
from typing import List

from cell import Cell


class Ant:
    def __init__(self) -> None:
        self.path: List[Cell] = []

    def get_path_length(self) -> int:
        return len(self.path)

    def reset_path(self) -> None:
        self.path = []

    def get_path(
        self,
        entry_cell: Cell,
        exit_cell: Cell,
        alpha: float = 1,
    ) -> List[Cell]:
        self.path.append(entry_cell)

        options: List[Cell]
        while self.path[-1] != exit_cell:
            if self.path[-1] != entry_cell:
                if len(self.path[-1].connected_cells) > 1:
                    options = [
                        cell
                        for cell in self.path[-1].connected_cells
                        if cell != self.path[-2]
                    ]

                else:
                    options = self.path[-1].connected_cells
            else:
                options = self.path[-1].connected_cells

            total_pheromone: float = 0
            for connected_cell in options:
                total_pheromone += connected_cell.pheromone**alpha

            cumulative_prob: List[float] = []
            accumulator: float = 0
            for connected_cell in options:
                accumulator += (connected_cell.pheromone**alpha) / total_pheromone
                cumulative_prob.append(accumulator)

            random_number = random()
            for i in range(len(cumulative_prob)):
                if random_number <= cumulative_prob[i]:
                    cell_index = i
                    break

            self.path.append(options[cell_index])

        for i in range(len(self.path) - 1):
            for j in range(len(self.path) - 1, i, -1):
                if self.path[i] == self.path[j]:
                    del self.path[i:j]
                    break

        return self.path
