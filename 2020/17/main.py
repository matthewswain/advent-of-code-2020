#! /usr/bin/env python

from typing import Dict, Iterable, Tuple


def load_data(path: str) -> Dict[Tuple[int, int, int], bool]:
    with open(path) as in_f:
        lines = [l.strip() for l in in_f.readlines()]
    grid = {}
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            grid[(x, y, 0)] = c == "#"
    return grid


def list_neighbours(
    origin_x: int, origin_y: int, origin_z: int
) -> Iterable[Tuple[int, int, int]]:
    for x in range(origin_x - 1, origin_x + 2):
        for y in range(origin_y - 1, origin_y + 2):
            for z in range(origin_z - 1, origin_z + 2):
                if (x, y, z) != (origin_x, origin_y, origin_z):
                    yield x, y, z


def update_cube(grid: Dict[Tuple[int, int, int], bool], x: int, y: int, z: int) -> bool:
    cube = grid.get((x, y, z), False)

    neighbour_coordinates = list_neighbours(x, y, z)
    neighbour_values = [grid.get(c, False) for c in neighbour_coordinates]
    active_neighbours = len([v for v in neighbour_values if v])

    if cube and not 2 <= active_neighbours <= 3:
        return False

    if not cube and active_neighbours == 3:
        return True

    return cube


def get_bounds(
    grid: Dict[Tuple[int, int, int], bool], include_inactive=False
) -> (Tuple[int, int, int], Tuple[int, int, int]):
    active = [
        (x, y, z) for x, y, z in grid.keys() if grid.get((x, y, z)) or include_inactive
    ]

    min_x = min([x for x, y, z in active])
    min_y = min([y for x, y, z in active])
    min_z = min([z for x, y, z in active])

    max_x = max([x for x, y, z in active])
    max_y = max([y for x, y, z in active])
    max_z = max([z for x, y, z in active])

    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def expand_grid(
    grid: Dict[Tuple[int, int, int], bool]
) -> Dict[Tuple[int, int, int], bool]:
    (min_x, min_y, min_z), (max_x, max_y, max_z) = get_bounds(grid)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                if grid.get((x, y, z)) is None:
                    grid[(x, y, z)] = False
    return grid


def update_grid(
    grid: Dict[Tuple[int, int, int], bool]
) -> Dict[Tuple[int, int, int], bool]:
    before = grid.copy()
    grid = expand_grid(grid)
    for k in grid.keys():
        grid[k] = update_cube(before, *k)
    return grid


if __name__ == "__main__":
    grid = load_data("data")

    # Part 1
    for _ in range(0, 6):
        grid = update_grid(grid)

    print(len([k for k, v in grid.items() if grid.get(k)]))
