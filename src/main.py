import collections
import os
from typing import (
    Dict,
    List,
    Tuple,
)

import matplotlib.pyplot as plt
from dotenv import (
    find_dotenv,
    load_dotenv,
)

from ant import Ant
from cell import Cell

load_dotenv(find_dotenv())


PATH_TO_DATA = os.environ.get("PATH_TO_DATA")
with open(PATH_TO_DATA, "r") as file:
    maze = [row.split() for row in file]


cells: Dict[Tuple[int, int], Cell] = {
    (i, j): Cell((i, j))
    for i in range(len(maze))
    for j in range(len(maze))
    if maze[i][j] != "0"
}

dim: int = len(maze)
for cell in cells:
    for x, y in [
        (cell[0], cell[1] - 1),
        (cell[0], cell[1] + 1),
        (cell[0] - 1, cell[1]),
        (cell[0] + 1, cell[1]),
    ]:
        if x >= 0 and y >= 0 and x <= dim - 1 and y <= dim - 1:
            if maze[x][y] != "0":
                cells[cell].add_connected_cell(cells[(x, y)])


entry: Tuple[int, int] = (0, 0)
exit: Tuple[int, int] = (0, 0)
for i in range(len(maze)):
    for j in range(len(maze)):
        if maze[i][j] == "2":
            entry = (i, j)
        if maze[i][j] == "3":
            exit = (i, j)


rho: float = 0.1
alpha: float = 3
n_ant: int = 50
initial_pheromone: float = 0.1
max_iterations: int = 50
entry_cell: Cell = cells[entry]
exit_cell: Cell = cells[exit]


for key in cells:
    cells[key].set_pheromone(initial_pheromone)

ants: List[Ant] = [Ant() for _ in range(n_ant)]
iteration: int = 0
while iteration < max_iterations:
    for ant in ants:
        ant.reset_path()
        ant.get_path(entry_cell, exit_cell, alpha)

    for key in cells:
        cells[key].update_pheromone(ants, rho)

    iteration += 1
    print("Iteration : ", iteration)


paths = collections.Counter([tuple(ant.path) for ant in ants])
max_count = max(paths.values())
solutions = [path for path, count in paths.items() if count == max_count]
solution = list(solutions[0])


X = []
Y = []
for i in range(len(solution)):
    X.append(solution[i].coordinates[0])
    Y.append(solution[i].coordinates[1])
data = []
for i in range(len(maze)):
    newlist = []
    for j in range(len(maze)):
        if maze[i][j] == "1" or maze[i][j] == "2" or maze[i][j] == "3":
            newlist.append(1)
        else:
            newlist.append(0)
    data.append(newlist)
plt.figure(figsize=(7, 7))
plt.title("Path from " + str(entry) + " To " + str(exit))
plt.imshow(data, cmap="gray")
plt.plot(Y, X, color="red")
plt.scatter([entry[1]], [entry[0]], color="green")
plt.scatter([exit[1]], [exit[0]], color="blue")

plt.show()
