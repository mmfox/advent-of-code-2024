from collections import defaultdict
import copy
from dataclasses import dataclass
from typing import Generator


FILENAME = "example_data.txt"


@dataclass
class ObstacleMap:
    num_rows: int
    num_cols: int
    row_obstacles: dict[int, list[int]]
    col_obstacles: dict[int, list[int]]
    guard_pos: tuple[int, int]


def get_data_values() -> Generator[list[str], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            yield line.strip()


def print_map(
    visited: set[tuple[int, int]], new_obstacles: set[tuple[int, int]] = None
) -> None:
    new_obstacles = set() if new_obstacles is None else new_obstacles
    row = 0
    for chars in get_data_values():
        new_chars = ""
        for col, char in enumerate(chars):
            if (row, col) in new_obstacles:
                new_chars += "O"
            elif (row, col) in visited:
                new_chars += "X"
            else:
                new_chars += char
        print(new_chars)
        row += 1


def get_next_obstacle(
    obstacle_map: ObstacleMap, direction: tuple[int, int], guard_pos: tuple[int, int]
) -> int:
    # Could binary search, but not implementing that at the moment
    obstacles = (
        obstacle_map.col_obstacles[guard_pos[1]]
        if direction[0] != 0
        else obstacle_map.row_obstacles[guard_pos[0]]
    )
    start = guard_pos[0] if direction[0] != 0 else guard_pos[1]
    forward = all([diff >= 0 for diff in direction])
    if forward:
        for i in range(len(obstacles)):
            if obstacles[i] > start:
                return obstacles[i]
        return -1

    for i in range(len(obstacles) - 1, -1, -1):
        if obstacles[i] < start:
            return obstacles[i]
    return -1


def get_next_direction(direction: tuple[int, int]) -> tuple[int, int]:
    if direction[0] != 0:
        next_row_diff = 0
    else:
        next_row_diff = direction[1]

    if direction[1] != 0:
        next_col_diff = 0
    else:
        next_col_diff = -1 * direction[0]

    return (next_row_diff, next_col_diff)


def parse_map() -> ObstacleMap:
    row_obstacles = defaultdict(list)
    col_obstacles = defaultdict(list)
    guard_pos = None
    row = 0
    num_cols = 0
    for chars in get_data_values():
        num_cols = len(chars)
        for col, char in enumerate(chars):
            if char == "#":
                row_obstacles[row].append(col)
                col_obstacles[col].append(row)
            elif char == "^":
                guard_pos = (row, col)
        row += 1
    num_rows = row

    return ObstacleMap(num_rows, num_cols, row_obstacles, col_obstacles, guard_pos)


def part1() -> int:
    obstacle_map = parse_map()

    visited_cells = set()
    direction = (-1, 0)
    next_guard_pos = None
    while True:
        next_obstacle = get_next_obstacle(
            obstacle_map, direction, obstacle_map.guard_pos
        )

        if direction[0] == -1:
            next_guard_pos = (next_obstacle + 1, obstacle_map.guard_pos[1])
        elif direction[0] == 1:
            next_guard_pos = (
                next_obstacle - 1 if next_obstacle != -1 else obstacle_map.num_rows - 1,
                obstacle_map.guard_pos[1],
            )
        elif direction[1] == -1:
            next_guard_pos = (obstacle_map.guard_pos[0], next_obstacle + 1)
        elif direction[1] == 1:
            next_guard_pos = (
                obstacle_map.guard_pos[0],
                next_obstacle - 1 if next_obstacle != -1 else obstacle_map.num_cols - 1,
            )

        for row in range(
            min(obstacle_map.guard_pos[0], next_guard_pos[0]),
            max(obstacle_map.guard_pos[0], next_guard_pos[0]) + 1,
        ):
            for col in range(
                min(obstacle_map.guard_pos[1], next_guard_pos[1]),
                max(obstacle_map.guard_pos[1], next_guard_pos[1]) + 1,
            ):
                visited_cells.add((row, col))

        if next_obstacle == -1:
            # print_map(visited_cells)
            return len(visited_cells)

        obstacle_map.guard_pos = next_guard_pos
        direction = get_next_direction(direction)


def check_for_loops(obstacle_map) -> bool:
    visited_cells = set()
    direction = (-1, 0)
    next_guard_pos = None
    while True:
        next_obstacle = get_next_obstacle(
            obstacle_map, direction, obstacle_map.guard_pos
        )

        if direction[0] == -1:
            next_guard_pos = (next_obstacle + 1, obstacle_map.guard_pos[1])
        elif direction[0] == 1:
            next_guard_pos = (
                next_obstacle - 1 if next_obstacle != -1 else obstacle_map.num_rows - 1,
                obstacle_map.guard_pos[1],
            )
        elif direction[1] == -1:
            next_guard_pos = (obstacle_map.guard_pos[0], next_obstacle + 1)
        elif direction[1] == 1:
            next_guard_pos = (
                obstacle_map.guard_pos[0],
                next_obstacle - 1 if next_obstacle != -1 else obstacle_map.num_cols - 1,
            )

        for row in range(
            min(obstacle_map.guard_pos[0], next_guard_pos[0]),
            max(obstacle_map.guard_pos[0], next_guard_pos[0]) + 1,
        ):
            for col in range(
                min(obstacle_map.guard_pos[1], next_guard_pos[1]),
                max(obstacle_map.guard_pos[1], next_guard_pos[1]) + 1,
            ):
                if (row, col, direction) in visited_cells:
                    return True

                visited_cells.add((row, col, direction))

        if next_obstacle == -1:
            return False

        obstacle_map.guard_pos = next_guard_pos
        direction = get_next_direction(direction)


def part2() -> int:
    num_loops = 0
    obstacle_map = parse_map()
    for row in range(0, obstacle_map.num_rows):
        for col in range(0, obstacle_map.num_cols):
            if (
                row,
                col,
            ) == obstacle_map.guard_pos or col in obstacle_map.row_obstacles[row]:
                continue

            new_obstacle_map = copy.deepcopy(obstacle_map)
            new_obstacle_map.row_obstacles[row].append(col)
            new_obstacle_map.row_obstacles[row].sort()
            new_obstacle_map.col_obstacles[col].append(row)
            new_obstacle_map.col_obstacles[col].sort()

            if check_for_loops(new_obstacle_map):
                num_loops += 1
    return num_loops


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
