from typing import Generator


FILENAME = "data.txt"


def get_data_values() -> Generator[list[str], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            yield line


def check_mas(chars: list[str]) -> bool:
    return "".join(chars) == "MAS"


def part1() -> int:
    data = []
    for line in get_data_values():
        data.append(line.strip())

    count = 0
    for row in range(len(data)):
        for col in range(len(data[row])):
            char = data[row][col]
            if char == "X":
                if row > 2:
                    if check_mas(
                        [data[row - 1][col], data[row - 2][col], data[row - 3][col]]
                    ):
                        count += 1
                if col > 2:
                    if check_mas(
                        [data[row][col - 1], data[row][col - 2], data[row][col - 3]]
                    ):
                        count += 1
                if col < len(data[row]) - 3:
                    if check_mas(
                        [data[row][col + 1], data[row][col + 2], data[row][col + 3]]
                    ):
                        count += 1
                if row > 2 and col > 2:
                    if check_mas(
                        [
                            data[row - 1][col - 1],
                            data[row - 2][col - 2],
                            data[row - 3][col - 3],
                        ]
                    ):
                        count += 1
                if row > 2 and col < len(data[row]) - 3:
                    if check_mas(
                        [
                            data[row - 1][col + 1],
                            data[row - 2][col + 2],
                            data[row - 3][col + 3],
                        ]
                    ):
                        count += 1
                if row < len(data) - 3:
                    if check_mas(
                        [data[row + 1][col], data[row + 2][col], data[row + 3][col]]
                    ):
                        count += 1
                if row < len(data) - 3 and col > 2:
                    if check_mas(
                        [
                            data[row + 1][col - 1],
                            data[row + 2][col - 2],
                            data[row + 3][col - 3],
                        ]
                    ):
                        count += 1
                if row < len(data) - 3 and col < len(data[row]) - 3:
                    if check_mas(
                        [
                            data[row + 1][col + 1],
                            data[row + 2][col + 2],
                            data[row + 3][col + 3],
                        ]
                    ):
                        count += 1

    return count


def part2() -> int:
    data = []
    for line in get_data_values():
        data.append(line.strip())

    count = 0
    for row in range(1, len(data) - 1):
        for col in range(1, len(data[row]) - 1):
            char = data[row][col]
            if char == "A":
                # Check for A being the center of MAS in an X pattern
                if (
                    check_mas(
                        [data[row - 1][col - 1], data[row][col], data[row + 1][col + 1]]
                    )
                    or check_mas(
                        [data[row + 1][col + 1], data[row][col], data[row - 1][col - 1]]
                    )
                ) and (
                    check_mas(
                        [data[row - 1][col + 1], data[row][col], data[row + 1][col - 1]]
                    )
                    or check_mas(
                        [data[row + 1][col - 1], data[row][col], data[row - 1][col + 1]]
                    )
                ):
                    count += 1

    return count


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
