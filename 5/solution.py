from collections import defaultdict
from dataclasses import dataclass
from typing import Generator


FILENAME = "data.txt"


@dataclass
class PrinterInput:
    rules: dict[int, set[int]]
    valid_orderings: list[list[int]]
    invalid_orderings: list[list[int]]


def get_data_values() -> Generator[tuple[list[int], bool], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            # Check if we're using rule notation
            if "|" in line:
                nums = line.split("|")
                assert len(nums) == 2, f"Invalid rule format: {line}"
                yield ([int(num) for num in nums], True)
            # Check for printing notation
            elif "," in line:
                nums = line.split(",")
                yield ([int(num) for num in nums], False)


def get_validated_printer_input() -> PrinterInput:
    must_have_been_seen_before = defaultdict(set)
    valid_orderings = []
    invalid_orderings = []
    for nums, is_rule in get_data_values():
        if is_rule:
            must_have_been_seen_before[nums[1]].add(nums[0])
        else:
            is_valid = True
            all_nums = set(nums)
            seen_nums = set()
            for num in nums:
                seen_nums.add(num)
                for required_num in must_have_been_seen_before[num]:
                    if required_num in all_nums and required_num not in seen_nums:
                        is_valid = False
                        break
            if is_valid:
                valid_orderings.append(nums)
            else:
                invalid_orderings.append(nums)

    return PrinterInput(must_have_been_seen_before, valid_orderings, invalid_orderings)


def part1() -> int:
    printer_input = get_validated_printer_input()
    sum_of_valid_middle_values = 0
    for valid_ordering in printer_input.valid_orderings:
        sum_of_valid_middle_values += valid_ordering[len(valid_ordering) // 2]
    return sum_of_valid_middle_values


def part2() -> int:
    printer_input = get_validated_printer_input()
    sum_of_middle_values = 0
    for invalid_ordering in printer_input.invalid_orderings:
        middle_index = len(invalid_ordering) // 2
        condensed_rules = defaultdict(set)
        nums_blocked_by = defaultdict(set)
        invalid_nums = set(invalid_ordering)
        curr_num = None
        for num in invalid_ordering:
            blocked_by = printer_input.rules[num].intersection(invalid_nums)
            condensed_rules[num] = blocked_by

            if blocked_by == set():
                curr_num = num

            for blocking_num in blocked_by:
                nums_blocked_by[blocking_num].add(num)

        valid_order = [curr_num]
        while len(valid_order) <= middle_index:
            next_num = None
            for blocked_num in nums_blocked_by[curr_num]:
                condensed_rules[blocked_num].remove(curr_num)
                if condensed_rules[blocked_num] == set():
                    next_num = blocked_num

            valid_order.append(next_num)
            curr_num = next_num

        sum_of_middle_values += valid_order[-1]

    return sum_of_middle_values


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
