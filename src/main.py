import sys

from src.core.crossword import Crossword


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py [number_of_words]")
        sys.exit(1)

    num_words = int(sys.argv[1])
    crossword = Crossword(num_words)

    if crossword.generate():
        crossword.print()
    else:
        print(f"Failed to generate crossword with {num_words} words")


if __name__ == "__main__":
    main()
