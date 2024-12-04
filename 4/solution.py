from typing import Generator


FILENAME = "data.txt"


def get_data_values() -> Generator[list[str], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            yield line


def check_mas(chars: list[str], reverse_allowed=False) -> bool:
    allowed = {"MAS"}
    if reverse_allowed:
        allowed.add("SAM")
    return "".join(chars) in allowed


def part1() -> int:
    data = []
    for line in get_data_values():
        data.append(line.strip())

    allowed_directions = []
    for row_delta in range(-1, 2):
        for col_delta in range(-1, 2):
            if row_delta == 0 and col_delta == 0:
                continue
            allowed_directions.append((row_delta, col_delta))

    count = 0
    for row in range(len(data)):
        for col in range(len(data[row])):
            char = data[row][col]
            if char == "X":
                for row_delta, col_delta in allowed_directions:
                    if 0 <= row + 3 * row_delta < len(
                        data
                    ) and 0 <= col + 3 * col_delta < len(data[row]):
                        if check_mas(
                            [
                                data[row + row_delta][col + col_delta],
                                data[row + 2 * row_delta][col + 2 * col_delta],
                                data[row + 3 * row_delta][col + 3 * col_delta],
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
                if check_mas(
                    [data[row - 1][col - 1], data[row][col], data[row + 1][col + 1]],
                    reverse_allowed=True,
                ) and check_mas(
                    [data[row - 1][col + 1], data[row][col], data[row + 1][col - 1]],
                    reverse_allowed=True,
                ):
                    count += 1

    return count


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
