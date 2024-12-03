from typing import Generator

import re

FILENAME = "data.txt"


def get_data_values() -> Generator[list[int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            yield line


def part1() -> int:
    product = 0
    for line in get_data_values():
        match = re.findall(r"mul\((\d+),(\d+)\)", line)
        for mul in match:
            product += int(mul[0]) * int(mul[1])
    return product


def part2() -> int:
    product = 0
    enabled = True
    for line in get_data_values():
        match = re.findall(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", line)
        for cmd, first, second in match:
            if cmd == "don't()":
                enabled = False
            elif cmd == "do()":
                enabled = True
            elif enabled:
                product += int(first) * int(second)
    return product


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
