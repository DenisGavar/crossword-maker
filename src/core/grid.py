import numpy as np
from typing import List, Tuple


class CrosswordGrid:
    def __init__(self, size: int):
        # grid size
        self.size = size
        # grid with words
        self.grid = np.full((size, size), " ", dtype="U1")
        # word numbers (vertical and horizontal words may start from the same cell)
        self.numbering = np.empty((size, size), dtype=object)
        for i in range(size):
            for j in range(size):
                self.numbering[i, j] = []
        # word list (word, start_row, start_col, direction, number)
        # direction in (horizontal, vertical)
        self.words: List[Tuple[str, int, int, str, int]] = []
        # number for the next word
        self.next_number = 1
        # occupied cells for:
        # v - vertical
        # h - horizontal
        # vs - vertical start
        # hs - horizontal start
        # ve - vertical end
        # he - horizontal end
        self.occupied = np.empty((size, size), dtype=object)
        for i in range(size):
            for j in range(size):
                self.occupied[i, j] = set()

    def print(self):
        """Print grid"""
        print(self.grid)
