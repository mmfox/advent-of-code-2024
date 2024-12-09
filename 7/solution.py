from dataclasses import dataclass
from typing import Generator


FILENAME = "data.txt"


@dataclass
class Equation:
    test_value: int
    nums: list[int]


def get_data_values() -> Generator[Equation, None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.split()
            test_value = int(nums.pop(0)[:-1])
            yield Equation(test_value, [int(num) for num in nums])


def is_valid(equation: Equation, include_concat: bool = False) -> bool:
    if len(equation.nums) == 1:
        return equation.nums[0] == equation.test_value

    first = equation.nums.pop(0)
    next = equation.nums.pop(0)

    if first > equation.test_value:
        return False

    added = first + next
    multiplied = first * next
    concat = int(str(first) + str(next))

    if include_concat and is_valid(
        Equation(equation.test_value, [concat] + equation.nums), include_concat=True
    ):
        return True

    return is_valid(
        Equation(equation.test_value, [added] + equation.nums),
        include_concat=include_concat,
    ) or is_valid(
        Equation(equation.test_value, [multiplied] + equation.nums),
        include_concat=include_concat,
    )


def part1() -> int:
    total_sum = 0
    for eq in get_data_values():
        if is_valid(eq):
            total_sum += eq.test_value
    return total_sum


def part2() -> int:
    total_sum = 0
    for eq in get_data_values():
        if is_valid(eq, include_concat=True):
            total_sum += eq.test_value
    return total_sum


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
