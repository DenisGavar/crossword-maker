def coordinate_generator(word, direction, row, col):
    for i in range(len(word)):
        if direction == "horizontal":
            yield row, col + i
        else:
            yield row + i, col
