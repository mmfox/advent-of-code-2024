import copy
from dataclasses import dataclass
from typing import Generator


FILENAME = "data.txt"


def get_data_values() -> Generator[list[int], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            nums = line.split()
            yield [int(num) for num in nums[0]]


@dataclass
class FileBlock:
    id: int | None
    is_empty: bool
    size: int


def parse_file_blocks(compressed_file_blocks: list[int]) -> list[FileBlock]:
    is_empty = False
    curr_id = 0
    file_blocks = []
    for block_size in compressed_file_blocks:
        if block_size != 0:
            file_blocks.append(
                FileBlock(curr_id if not is_empty else None, is_empty, block_size)
            )

        if not is_empty:
            curr_id += 1
        is_empty = not is_empty

    return file_blocks


def part1() -> int:
    compressed_file_blocks = None
    for data in get_data_values():
        compressed_file_blocks = data

    file_blocks = parse_file_blocks(compressed_file_blocks)

    checksum = 0
    file_index = 0
    fill_block_index = len(file_blocks) - 1
    curr_block_index = 0
    while curr_block_index <= fill_block_index:
        curr_file_block = file_blocks[curr_block_index]
        if not curr_file_block.is_empty:
            for _ in range(curr_file_block.size):
                checksum += file_index * curr_file_block.id
                file_index += 1
        else:
            for _ in range(curr_file_block.size):
                fill_block = file_blocks[fill_block_index]
                while fill_block.is_empty or fill_block.size == 0:
                    fill_block_index -= 1
                    fill_block = file_blocks[fill_block_index]

                if fill_block_index > curr_block_index:
                    checksum += file_index * fill_block.id
                    fill_block.size -= 1
                    file_index += 1

        curr_block_index += 1

    return checksum


def part2() -> int:
    compressed_file_blocks = None
    for data in get_data_values():
        compressed_file_blocks = data

    file_blocks = parse_file_blocks(compressed_file_blocks)

    final_file_blocks = copy.deepcopy(file_blocks)
    short_circuit_size = 10
    moved_block_ids = set()

    for i in range(len(file_blocks) - 1, -1, -1):
        file_block = file_blocks[i]
        if file_block.is_empty:
            continue

        if file_block.size >= short_circuit_size:
            continue

        for final_i in range(len(final_file_blocks)):
            potential_block = final_file_blocks[final_i]
            if potential_block.id == file_block.id:
                short_circuit_size = min(short_circuit_size, file_block.size)
                break

            if potential_block.is_empty and potential_block.size >= file_block.size:
                moved_block_ids.add(file_block.id)
                if potential_block.size == file_block.size:
                    potential_block.is_empty = False
                    potential_block.id = file_block.id
                else:
                    potential_block.size -= file_block.size
                    final_file_blocks.insert(final_i, file_block)

                break

    for i in range(len(final_file_blocks) - 1, -1, -1):
        if not moved_block_ids:
            break

        file_block = final_file_blocks[i]
        if file_block.id in moved_block_ids:
            moved_block_ids.remove(file_block.id)
            file_block.id = None
            file_block.is_empty = True

    checksum = 0
    file_index = 0
    for file_block in final_file_blocks:
        if not file_block.is_empty:
            for _ in range(file_block.size):
                checksum += file_index * file_block.id
                file_index += 1
        else:
            file_index += file_block.size
    return checksum


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
