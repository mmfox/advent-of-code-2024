from dataclasses import dataclass
from typing import Generator


FILENAME = "data.txt"


@dataclass
class Map:
    num_rows: int
    num_cols: int
    data: list[list[int]]
    trailheads: list[tuple[int, int]]


def get_data_values() -> Generator[list[int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.split()[0]
            yield [int(num) for num in nums]


def parse_map() -> Map:
    map_data = []
    trailheads = []
    for row in get_data_values():
        for col in range(len(row)):
            if row[col] == 0:
                trailheads.append((len(map_data), col))
        map_data.append(row)

    return Map(len(map_data[0]), len(map_data), map_data, trailheads)


def get_trail_ends(
    node: tuple[int, int],
    top_map: Map,
    memoized_paths: dict[tuple[int, int], set[tuple[int, int]]],
) -> set[tuple[int, int]]:
    if node in memoized_paths:
        return memoized_paths[node]

    curr_value = top_map.data[node[0]][node[1]]
    if curr_value == 9:
        return {node}

    trail_ends = set()
    potential_next_nodes = [
        (node[0] - 1, node[1]),
        (node[0] + 1, node[1]),
        (node[0], node[1] - 1),
        (node[0], node[1] + 1),
    ]
    for next_node in potential_next_nodes:
        if (
            next_node[0] >= 0
            and next_node[0] < top_map.num_rows
            and next_node[1] >= 0
            and next_node[1] < top_map.num_cols
            and top_map.data[next_node[0]][next_node[1]] == curr_value + 1
        ):
            trail_ends.update(get_trail_ends(next_node, top_map, memoized_paths))

    memoized_paths[node] = trail_ends
    return trail_ends


def get_trail_rating(
    node: tuple[int, int], top_map: Map, memoized_paths: dict[tuple[int, int], int]
) -> int:
    if node in memoized_paths:
        return memoized_paths[node]

    curr_value = top_map.data[node[0]][node[1]]
    if curr_value == 9:
        return 1

    rating = 0
    potential_next_nodes = [
        (node[0] - 1, node[1]),
        (node[0] + 1, node[1]),
        (node[0], node[1] - 1),
        (node[0], node[1] + 1),
    ]
    for next_node in potential_next_nodes:
        if (
            next_node[0] >= 0
            and next_node[0] < top_map.num_rows
            and next_node[1] >= 0
            and next_node[1] < top_map.num_cols
            and top_map.data[next_node[0]][next_node[1]] == curr_value + 1
        ):
            rating += get_trail_rating(next_node, top_map, memoized_paths)

    memoized_paths[node] = rating
    return rating


def part1() -> int:
    top_map = parse_map()

    memoized_paths = {}

    score_sum = 0
    for trailhead in top_map.trailheads:
        score_sum += len(get_trail_ends(trailhead, top_map, memoized_paths))

    return score_sum


def part2() -> int:
    top_map = parse_map()

    memoized_paths = {}

    score_sum = 0
    for trailhead in top_map.trailheads:
        score_sum += get_trail_rating(trailhead, top_map, memoized_paths)

    return score_sum


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
