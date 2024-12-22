from enum import Enum
import uuid

from dataclasses import dataclass, field
from typing import Generator


FILENAME = "data.txt"


class SideType(Enum):
    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"


@dataclass
class Region:
    id: str
    plant: str
    size: int = 0
    perimeter: int = 0
    fences: set[tuple[SideType, tuple[int, int]]] = field(default_factory=set)
    side_count: int = 0
    contained_cells: set[tuple[int, int]] = field(default_factory=set)
    merge_count: int = 0

    def fence_price(self) -> int:
        return self.size * self.perimeter

    def side_fence_price(self) -> int:
        return self.size * self.side_count

    def plot(self, graph: list[list[str]]) -> None:
        for row, row_data in enumerate(graph):
            new_row = []
            for col, plant in enumerate(row_data):
                if (row, col) in self.contained_cells:
                    new_row.append("\033[31m" + plant + "\033[0m")
                else:
                    new_row.append(plant)
            print("".join(new_row))


def get_data_values() -> Generator[list[str], None, None]:
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            yield [c for c in line.strip()]


def is_valid_coord(graph: list[list[str]], row: int, col: int) -> bool:
    return 0 <= row < len(graph) and 0 <= col < len(graph[0])


def get_region_by_id(region_by_id: dict[str, Region], region_id) -> Region:
    region = region_by_id[region_id]
    while region_by_id[region.id].id != region.id:
        region = region_by_id[region.id]
    return region


def get_fence_price() -> int:
    graph = []
    for row in get_data_values():
        graph.append(row)

    all_region_ids: set[str] = set()
    region_by_id: dict[str, Region] = {}
    region_id_by_coord: dict[tuple[int, int], str] = {}
    for row, row_data in enumerate(graph):
        for col, plant in enumerate(row_data):
            col_match = None
            row_match = None
            if (
                row > 0
                and get_region_by_id(
                    region_by_id, region_id_by_coord[(row - 1, col)]
                ).plant
                == plant
            ):
                col_match = get_region_by_id(
                    region_by_id, region_id_by_coord[(row - 1, col)]
                )

            if (
                col > 0
                and get_region_by_id(
                    region_by_id, region_id_by_coord[(row, col - 1)]
                ).plant
                == plant
            ):
                row_match = get_region_by_id(
                    region_by_id, region_id_by_coord[(row, col - 1)]
                )

            if (
                col_match is not None
                and row_match is not None
                and col_match.id != row_match.id
            ):
                all_region_ids.remove(col_match.id)
                region_by_id[col_match.id] = row_match
                row_match.size += col_match.size
                row_match.perimeter += col_match.perimeter
                row_match.side_count += col_match.side_count
                row_match.fences.update(col_match.fences)
                row_match.contained_cells.update(col_match.contained_cells)
                row_match.merge_count += col_match.merge_count + 1

            if row_match is not None:
                region = row_match
            elif col_match is not None:
                region = col_match
            else:
                region = Region(uuid.uuid4(), plant)
                region_by_id[region.id] = region
                all_region_ids.add(region.id)

            for coord_row, coord_col, (side_type, (side_row, side_col), check_cell) in [
                (
                    row - 1,
                    col,
                    (SideType.HORIZONTAL, (row - 1, col), (row - 1, col - 1)),
                ),
                (row + 1, col, (SideType.HORIZONTAL, (row, col), (row + 1, col - 1))),
                (row, col - 1, (SideType.VERTICAL, (row, col - 1), (row - 1, col - 1))),
                (row, col + 1, (SideType.VERTICAL, (row, col), (row - 1, col + 1))),
            ]:
                if (
                    not is_valid_coord(graph, coord_row, coord_col)
                    or graph[coord_row][coord_col] != plant
                ):
                    if side_type == SideType.HORIZONTAL and (
                        (side_type, (side_row, side_col - 1)) not in region.fences
                        or check_cell in region.contained_cells
                    ):
                        region.side_count += 1
                    elif side_type == SideType.VERTICAL and (
                        (side_type, (side_row - 1, side_col)) not in region.fences
                        or check_cell in region.contained_cells
                    ):
                        region.side_count += 1
                    region.fences.add((side_type, (side_row, side_col)))
                    region.perimeter += 1

            region.size += 1
            region_id_by_coord[(row, col)] = region.id
            region.contained_cells.add((row, col))

    total_fence_price = 0
    side_fence_price = 0
    for region_id in all_region_ids:
        region = region_by_id[region_id]
        total_fence_price += region.fence_price()
        side_fence_price += region.side_fence_price()

    return (total_fence_price, side_fence_price)


def part1() -> int:
    return get_fence_price()[0]


def part2() -> int:
    return get_fence_price()[1]


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
