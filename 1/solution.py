from collections import defaultdict
from typing import Generator


FILENAME = "data.txt"


def get_data_values() -> Generator[tuple[int, int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.strip().split("   ")
            assert len(nums) == 2, "Expected to find two numbers in each line"
            yield (int(nums[0]), int(nums[1]))


def part1() -> int:
    list1 = []
    list2 = []
    for num1, num2 in get_data_values():
        list1.append(num1)
        list2.append(num2)

    list1.sort()
    list2.sort()

    sum = 0
    for i in range(len(list1)):
        sum += abs(list1[i] - list2[i])

    return sum


def part2() -> int:
    list1_counts = defaultdict(int)
    list2_counts = defaultdict(int)

    for num1, num2 in get_data_values():
        list1_counts[num1] += 1
        list2_counts[num2] += 1

    similarity_score = 0
    for num, count in list1_counts.items():
        similarity_score += num * count * list2_counts[num]

    return similarity_score


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
