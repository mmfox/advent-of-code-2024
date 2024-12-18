from typing import Generator


FILENAME = "data.txt"


def get_data_values() -> Generator[list[int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.split()
            yield [int(num) for num in nums]


def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        return [
            int(str_stone[: (len(str_stone) // 2)]),
            int(str_stone[(len(str_stone) // 2) :]),
        ]

    return [stone * 2024]


def dfs(
    stone_counts: dict[tuple[int, int], int],
    curr_node: int,
    path: list[int],
    remaining_depth: int,
) -> int:
    if (curr_node, remaining_depth) in stone_counts:
        return stone_counts[(curr_node, remaining_depth)]

    next_nodes = blink(curr_node)
    stone_counts[(curr_node, 1)] = len(next_nodes)

    if remaining_depth == 1:
        return len(next_nodes)

    total_stones = 0
    for next_node in next_nodes:
        next_node_total_stones = dfs(
            stone_counts, next_node, path + [curr_node], remaining_depth - 1
        )

        total_stones += next_node_total_stones

    stone_counts[(curr_node, remaining_depth)] = total_stones

    for i in range(1, remaining_depth):
        node_depth_count = 0
        for next_node in next_nodes:
            node_depth_count += stone_counts[(next_node, i)]
        stone_counts[(curr_node, i + 1)] = node_depth_count

    return total_stones


def count_stones(num_blinks: int) -> int:
    stone_counts = {}

    stones = []
    for data in get_data_values():
        stones = data

    total_count = 0
    for stone in stones:
        total_count += dfs(stone_counts, stone, [], num_blinks)

    return total_count


def part1() -> int:
    return count_stones(25)


def part2() -> int:
    return count_stones(75)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
