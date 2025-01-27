from typing import Optional, List
import random

from src.core.grid import CrosswordGrid
from src.api.datamuse import DatamuseAPI
from src.config.config import Config
from src.utils.generators import coordinate_generator


class Crossword:
    def __init__(self, num_words: int):
        self.num_words = num_words
        self.grid: Optional[CrosswordGrid] = None
        self.api = DatamuseAPI()
        self.attempt_limit = 3

    @property
    def grid_size(self) -> int:
        if self.grid is not None:
            return self.grid.size
        return 0

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

        # fill in the grid with blank words
        if not self._generate_layout(word_lengths):
            return False

        self.print()

        # fill in the blank words with certain words
        if not self._fill_words():
            return False

        return True

    def _generate_word_lengths(self) -> List[int]:
        lengths = []
        for _ in range(self.num_words):
            length = random.randint(Config.MIN_WORD_LENGTH, Config.MAX_WORD_LENGTH)
            lengths.append(length)

        return sorted(lengths, reverse=True)

    def _generate_layout(self, word_lengths: List[int]) -> bool:
        first_length = word_lengths[0]
        start_row = self.grid_size // 2
        start_col = (self.grid_size - first_length) // 2

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
        if row < 0 or col < 0:
            return False
        if direction == "horizontal":
            if col + len(word) > self.grid_size:
                return False
        else:
            if row + len(word) > self.grid_size:
                return False

        # check the overlap
        if not self._check_overlap(row, col, direction, len(word)):
            return False

        self.grid.words.append((word, row, col, direction, number))
        for i, (x, y) in enumerate(coordinate_generator(word, direction, row, col)):
            self.grid.grid[x, y] = word[i]

        # fill in occupied
        short_direction = direction[0]

        # for the first position and the last position
        if direction == "horizontal":
            start = col - 1
            end = col + len(word)
            if start >= 0:
                self.grid.occupied[row, start].update(["v", "h"])
            if end < self.grid_size:
                self.grid.occupied[row, end].update(["v", "h"])
        else:
            start = row - 1
            end = row + len(word)
            if start >= 0:
                self.grid.occupied[start, col].update(["v", "h"])
            if end < self.grid_size:
                self.grid.occupied[end, col].update(["v", "h"])

        # for all positions
        for i in range(len(word)):
            if direction == "horizontal":
                x, y = row, col + i
                if x > 0:
                    self.grid.occupied[x - 1, y].update(["h", "ve"])
                if x < self.grid_size - 1:
                    self.grid.occupied[x + 1, y].update(["h", "vs"])
            else:
                x, y = row + i, col
                if y > 0:
                    self.grid.occupied[x, y - 1].update(["v", "he"])
                if y < self.grid_size - 1:
                    self.grid.occupied[x, y + 1].update(["v", "hs"])

            self.grid.occupied[x, y].add(short_direction)

        self.grid.numbering[row, col].append(number)

        return True

    def _place_word_in_layout(self, word: str, number: int) -> bool:
        # shuffle words
        random.shuffle(self.grid.words)

        # collect the possible positions of the new word
        word_positions = [i for i in range(len(word))]

        for placed_word in self.grid.words:
            # collect and shuffle the possible positions of the placed word
            placed_word_positions = [i for i in range(len(placed_word))]
            random.shuffle(placed_word_positions)

            for placed_word_pos in placed_word_positions:
                # shuffle the possible positions of the new word
                random.shuffle(word_positions)

                for word_pos in word_positions:
                    if placed_word[3] == "horizontal":
                        new_row = placed_word[1] - word_pos
                        new_col = placed_word[2] + placed_word_pos
                        direction = "vertical"
                    else:
                        new_row = placed_word[1] + placed_word_pos
                        new_col = placed_word[2] - word_pos
                        direction = "horizontal"

                    if self._try_place_word(word, new_row, new_col, direction, number):
                        return True

        return False

    def _check_overlap(
        self, row: int, col: int, direction: str, word_length: int
    ) -> bool:
        short_direction = direction[0]

        # check the first letter
        if f"{short_direction}s" in self.grid.occupied[col, row]:
            return False

        # check the last letter
        if short_direction == "h":
            x, y = row, col + word_length - 1
        else:
            x, y = row + word_length - 1, col
        if f"{short_direction}e" in self.grid.occupied[x, y]:
            return False

        for i in range(word_length):
            if short_direction == "h":
                x, y = row, col + i
            else:
                x, y = row + i, col
            if short_direction in self.grid.occupied[x, y]:
                return False

        return True

    def _fill_words(self) -> bool:
        return self._backtrack(0)

    def _backtrack(self, index: int) -> bool:
        if index >= len(self.grid.words):
            return True

        word_info = self.grid.words[index]
        word, row, col, direction, number = word_info
        pattern = self._get_pattern(word, row, col, direction)

        # Получаем все возможные слова для текущего паттерна
        possible_words = self._fetch_words(pattern)

        print(f"index: {index}, count_candidates: {len(possible_words)}")

        for candidate in possible_words:
            # Сохраняем текущее состояние затронутых ячеек
            saved_cells = self._save_cells_state(row, col, direction, len(candidate))

            # Обновляем сетку кандидатом
            self._update_grid(index, candidate, row, col, direction, number)

            # Рекурсивно пытаемся заполнить следующие слова
            if self._backtrack(index + 1):
                return True

            # Если не получилось - восстанавливаем состояние
            self._restore_cells_state(saved_cells)

        return False

    def _save_cells_state(
        self, row: int, col: int, direction: str, length: int
    ) -> list:
        saved = []
        for i in range(length):
            if direction == "horizontal":
                r = row
                c = col + i
            else:
                r = row + i
                c = col
            saved.append((r, c, self.grid.grid[r, c]))
        return saved

    def _restore_cells_state(self, saved_cells: list):
        for r, c, char in saved_cells:
            self.grid.grid[r, c] = char

    def _get_possible_words(self, pattern: str) -> list:
        # Ваша реализация получения ВСЕХ подходящих слов для паттерна
        # Например, из базы данных или другого источника
        return []

    def _get_pattern(self, word: str, row: int, col: int, direction: str) -> str:
        pattern = ""

        for x, y in coordinate_generator(word, direction, row, col):
            pattern += self.grid.grid[x, y]

        return pattern

    def _fetch_words(self, pattern: str) -> str:
        for _ in range(self.attempt_limit):
            words = self.api.get_words(pattern)
            if words:
                return words
        return []

    def _update_grid(
        self,
        index: int,
        actual_word: str,
        row: int,
        col: int,
        direction: str,
        number: int,
    ):
        self.grid.words[index] = (actual_word, row, col, direction, number)
        for i, (x, y) in enumerate(
            coordinate_generator(actual_word, direction, row, col)
        ):
            self.grid.grid[x, y] = actual_word[i].upper()

    def print(self):
        """Print crossword"""
        self.grid.print()
