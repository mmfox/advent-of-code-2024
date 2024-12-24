from dataclasses import dataclass
from typing import Generator

import re

FILENAME = "data.txt"


@dataclass
class Button:
    x: int
    y: int


@dataclass
class Game:
    button_a: Button = None
    button_b: Button = None
    prize_x: int = None
    prize_y: int = None


def get_data_values() -> Generator[Game, None, None]:
    game = Game()
    with open(FILENAME) as file:
        data = file.readlines()
        for line in data:
            game_info = line.strip()
            button_a_match = re.match(r"Button A: X\+(\d+), Y\+(\d+)", game_info)
            button_b_match = re.match(r"Button B: X\+(\d+), Y\+(\d+)", game_info)
            prize_match = re.match(r"Prize: X=(\d+), Y=(\d+)", game_info)
            if button_a_match is not None:
                x, y = button_a_match.groups()
                game.button_a = Button(int(x), int(y))
            elif button_b_match is not None:
                x, y = button_b_match.groups()
                game.button_b = Button(int(x), int(y))
            elif prize_match is not None:
                x, y = prize_match.groups()
                game.prize_x = int(x)
                game.prize_y = int(y)
                yield game
                game = Game()


def solve_game(game: Game) -> int:
    b_presses = (
        (game.prize_y * game.button_a.x) - (game.button_a.y * game.prize_x)
    ) / ((game.button_b.y * game.button_a.x) - (game.button_b.x * game.button_a.y))
    if not b_presses.is_integer():
        return 0

    a_presses = (game.prize_x - b_presses * game.button_b.x) / game.button_a.x
    return int(b_presses + 3 * a_presses)


def part1() -> int:
    total_tokens = 0
    for game in get_data_values():
        total_tokens += solve_game(game)

    return total_tokens


def part2() -> int:
    total_tokens = 0
    for game in get_data_values():
        game.prize_x += 10000000000000
        game.prize_y += 10000000000000
        total_tokens += solve_game(game)

    return total_tokens


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
