from typing import Generator


FILENAME = "example_data.txt"


def get_data_values() -> Generator[list[int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.split()
            yield [int(num) for num in nums]


def part1() -> int:
    pass


def part2() -> int:
    pass


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
