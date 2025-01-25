from typing import Optional

from grid import CrosswordGrid
from ..api.datamuse import DatamuseAPI
from ..config.config import Config


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
        # fill in the table with blank words
        # word = '    ' (only spaces with the correct lenght)
        # start position
        # direction
        pass
        # fill in the blank words with certain words
        pass

    def print(self):
        """Print crossword"""
        self.grid.print()
