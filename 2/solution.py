from typing import Generator


FILENAME = "data.txt"
MIN_DIFF = 1
MAX_DIFF = 3


def get_data_values() -> Generator[list[int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.split()
            yield [int(num) for num in nums]


def is_safe(nums: list[int], can_remove=False) -> bool:
    assert len(nums) > 1, "Expected at least 2 nums"

    increasing = nums[1] > nums[0]
    for i in range(len(nums) - 1):
        left = nums[i]
        right = nums[i + 1]
        diff = abs(right - left)
        if (
            (increasing and right <= left)
            or (not increasing and right >= left)
            or diff > MAX_DIFF
            or diff < MIN_DIFF
        ):
            if can_remove:
                to_try_removing = [0] if i == 1 else []
                to_try_removing.extend([i, i + 1])
                for to_remove_index in to_try_removing:
                    if is_safe(nums[:to_remove_index] + nums[to_remove_index + 1 :]):
                        return True
            return False
    return True


def part1() -> int:
    num_safe = 0
    for nums in get_data_values():
        if is_safe(nums):
            num_safe += 1

    return num_safe


def part2() -> int:
    num_safe = 0
    for nums in get_data_values():
        if is_safe(nums, can_remove=True):
            num_safe += 1

    return num_safe


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
