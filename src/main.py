import sys

from core.crossword import Crossword

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [number_of_words]")
        sys.exit(1)

    num_words = int(sys.argv[1])
    crossword = Crossword(num_words)

    crossword.generate()

    if crossword.generate():
        crossword.print()
    else:
        print(f"Failed to generate crossword with {num_words} words")
