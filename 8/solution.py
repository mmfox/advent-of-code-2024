from collections import defaultdict
from dataclasses import dataclass
from typing import Generator


FILENAME = "data.txt"


@dataclass
class AntennaMap:
    antennas: dict[str, list[tuple[int, int]]]
    num_rows: int
    num_cols: int


def get_data_values() -> Generator[str, None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            yield line.strip()


def parse_map() -> AntennaMap:
    antennas = defaultdict(list)
    row = 0
    num_cols = 0
    for data in get_data_values():
        for col, freq in enumerate(data):
            if freq == ".":
                continue
            antennas[freq].append((row, col))
        num_cols = len(data)
        row += 1

    return AntennaMap(antennas, row, num_cols)


def print_map(antinodes: set[tuple[int, int]]) -> None:
    row = 0
    extra_antinodes = set()
    for data in get_data_values():
        row_repr = ""
        for col, freq in enumerate(data):
            if freq != "." and (row, col) in antinodes:
                extra_antinodes.add((row, col))
                row_repr += freq
                continue

            if (row, col) in antinodes:
                row_repr += "#"
            else:
                row_repr += freq
        row += 1
        print(row_repr)

    print(f"Extra_antinodes: {extra_antinodes}")


def is_on_map(point: tuple[int, int], num_rows: int, num_cols: int) -> bool:
    return (
        point[0] > -1 and point[0] < num_rows and point[1] > -1 and point[1] < num_cols
    )


def get_valid_antinodes(
    node1: tuple[int, int],
    node2: tuple[int, int],
    num_rows: int,
    num_cols: int,
    resonate: bool = False,
) -> set[tuple[int, int]]:
    valid_antinodes = {node1, node2} if resonate else set()

    row_diff = node2[0] - node1[0]
    col_diff = node2[1] - node1[1]

    antinode1 = (node1[0] - row_diff, node1[1] - col_diff)
    antinode2 = (node2[0] + row_diff, node2[1] + col_diff)

    for direction, antinode in [(-1, antinode1), (1, antinode2)]:
        next_antinode = antinode
        while is_on_map(next_antinode, num_rows, num_cols):
            valid_antinodes.add(next_antinode)
            if not resonate:
                break

            next_antinode = (
                next_antinode[0] + (direction * row_diff),
                next_antinode[1] + (direction * col_diff),
            )

    return valid_antinodes


def get_antinodes(resonate: bool, print: bool = False) -> int:
    antenna_map = parse_map()
    antinodes = set()
    for freq, nodes in antenna_map.antennas.items():
        for i in range(len(nodes) - 1):
            for j in range(i + 1, len(nodes)):
                antinodes.update(
                    get_valid_antinodes(
                        nodes[i],
                        nodes[j],
                        antenna_map.num_rows,
                        antenna_map.num_cols,
                        resonate,
                    )
                )

    if print:
        print_map(antinodes)

    return len(antinodes)


def part1() -> int:
    return get_antinodes(resonate=False)


def part2() -> int:
    return get_antinodes(resonate=True)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
