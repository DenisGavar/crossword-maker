import numpy as np
from typing import List, Tuple


class CrosswordGrid:
    def __init__(self, size: int):
        # grid size
        self.size = size
        # grid with words
        self.grid = np.full((size, size), " ", dtype="U1")
        # word numbers
        self.numbering = np.zeros((size, size), dtype=int)
        # word list (word, start_row, start_col, direction, number)
        # direction in (horizontal, vertical)
        self.words: List[Tuple[str, int, int, str, int]] = []
        # number for the next word
        self.next_number = 1

    def print(self):
        """Print grid"""
        pass
