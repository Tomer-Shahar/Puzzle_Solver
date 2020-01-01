

class PuzzlePiece:
    """
    A class that represents a single puzzle piece
    """

    def __init__(self, shape, idx):
        """
        :param shape: A 2d list describing the shape.
        :param idx: The number of the shape.
        """
        self.shape = shape
        self.idx = idx
        self.width = len(shape[0])  # the widest part in the shape
        self.height = len(shape)  # the longest part of the shape
        self.val = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] != 0:
                    self.val += 1
