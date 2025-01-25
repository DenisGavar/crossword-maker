from typing import Optional, List
import random

from src.core.grid import CrosswordGrid
from src.api.datamuse import DatamuseAPI
from src.config.config import Config


class Crossword:
    def __init__(self, num_words: int):
        self.num_words = num_words
        self.grid: Optional[CrosswordGrid] = None
        self.api = DatamuseAPI()
        self.attempt_limit = 3

    def calculate_grid_size(self) -> int:
        base_size = max(
            Config.MAX_WORD_LENGTH + Config.GRID_PADDING,
            int(self.num_words**0.5 * Config.MAX_WORD_LENGTH),
        )
        return min(base_size, 20)

    def generate(self) -> bool:
        """Generate a grid"""
        # create a blank grid
        size = self.calculate_grid_size()
        self.grid = CrosswordGrid(size)

        # word lenght generation
        word_lengths = self._generate_word_lengths()
        if not word_lengths:
            return False

        if not self._generate_layout(word_lengths):
            return False

        # fill in the blank words with certain words
        pass

        return True

    def _generate_word_lengths(self) -> List[int]:
        lengths = []
        for _ in range(self.num_words):
            length = random.randint(Config.MIN_WORD_LENGTH, Config.MAX_WORD_LENGTH)
            lengths.append(length)

        return sorted(lengths, reverse=True)

    def _generate_layout(self, word_lengths: List[int]) -> bool:
        first_length = word_lengths[0]
        start_row = self.grid.size // 2
        start_col = (self.grid.size - first_length) // 2

        if not self._try_place_word(
            "?" * first_length, start_row, start_col, "horizontal", 1
        ):
            return False

        for i, length in enumerate(word_lengths[1:], 2):
            if not self._place_word_in_layout("?" * length, i):
                return False

        return True

    def _try_place_word(
        self, word: str, row: int, col: int, direction: str, number: int
    ) -> bool:
        # check the borders
        if direction == "horizontal":
            if col + len(word) > self.grid.size:
                return False
        else:
            if row + len(word) > self.grid.size:
                return False

        # check the overlap
        if not self._check_overlap(row, col, direction, len(word)):
            return False

        # TODO:replace with a grid methods
        self.grid.words.append((word, row, col, direction, number))
        for i in range(len(word)):
            if direction == "horizontal":
                x, y = row, col + i
            else:
                x, y = row + i, col
            self.grid.grid[x, y] = word[i]

        # fill in occupied
        short_direction = direction[0]

        # for the first position and the last position
        if direction == "horizontal":
            start = col - 1
            end = col + len(word)
            if start >= 0:
                self.grid.occupied[row, start].update(["v", "h"])
            if end < self.grid.size:
                self.grid.occupied[row, end].update(["v", "h"])
        else:
            start = row - 1
            end = row + len(word)
            if start >= 0:
                self.grid.occupied[start, col].update(["v", "h"])
            if end < self.grid.size:
                self.grid.occupied[end, col].update(["v", "h"])

        # for all positions
        for i in range(len(word)):
            if direction == "horizontal":
                x, y = row, col + i
                if x > 0:
                    self.grid.occupied[x - 1, y].add(short_direction)
                if x < self.grid.size - 1:
                    self.grid.occupied[x + 1, y].add(short_direction)
            else:
                x, y = row + i, col
                if y > 0:
                    self.grid.occupied[x, y - 1].add(short_direction)
                if y < self.grid.size - 1:
                    self.grid.occupied[x, y + 1].add(short_direction)

            self.grid.occupied[x, y].add(short_direction)

        self.grid.numbering[row, col].append(number)

        return True

    def _place_word_in_layout(self, word: str, number: int) -> bool:
        random.shuffle(self.grid.words)
        for placed_word in self.grid.words:
            for _ in range(50):
                word_pos = random.randint(0, len(word) - 1)
                # print(word_pos)
                placed_word_pos = random.randint(0, len(placed_word) - 1)
                # print(placed_word_pos)
                if placed_word[3] == "horizontal":
                    new_row = placed_word[1] - word_pos
                    new_col = placed_word[2] + placed_word_pos
                    direction = "vertical"
                else:
                    new_row = placed_word[1] + placed_word_pos
                    new_col = placed_word[2] - word_pos
                    direction = "horizontal"

                # print(new_row, new_col)
                if self._try_place_word(word, new_row, new_col, direction, number):
                    return True

        return False

    def _check_overlap(
        self, row: int, col: int, direction: str, word_length: int
    ) -> bool:
        short_direction = direction[0]

        for i in range(word_length):
            if short_direction == "h":
                x, y = row, col + i
            else:
                x, y = row + i, col
            if short_direction in self.grid.occupied[x, y]:
                return False

        return True

    def print(self):
        """Print crossword"""
        self.grid.print()
