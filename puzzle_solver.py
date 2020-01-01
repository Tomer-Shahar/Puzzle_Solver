import time

from file_parser import FileParser
from custom_heap import OpenListHeap
from board import BoardState


class PuzzleSolver:
    """
    Python Class for solving the 16-piece puzzle.
    """
    def __init__(self, filepath):
        """
        The constructor must receive a file path to work with. It begins by parsing it using the FileParser class.
        :param filepath: The path to the piece file.
        """

        self.pieces = []  # A field for the actual pieces
        self.__parse_pieces_file(filepath)

    def __parse_pieces_file(self, filepath):
        """
        Parses the file using the FileParser class.
        :param filepath: The path to the piece file.
        :return: updates the self.pieces value.
        """
        self.pieces = FileParser.parse_pieces_file(filepath)

    def solve_puzzle(self, height=10, width=10):
        """
        The main function that solves a puzzle: using the pieces we previously parsed, this function tries to place
        them on a board of given dimensions using as many tiles as possible. Optimally, we'd want to place all pieces
        on the board. I assume this is the case, otherwise the implementation must be very different.

        I will implement this using a straightforward approach: solving it iteratively as a search problem using A*.

        :param height: The height of the board to be solved on
        :param width: The width of the board
        :return: The solved board with a different number for each piece (1-16).
        """
        # ToDo: Give each tile a degree (the number of surrounding free tiles) and try to fill tiles with lowest degree
        open_list = OpenListHeap()
        # Sort the pieces by size. We should fit large pieces first
        self.pieces = sorted(self.pieces, key=lambda x: (x.width*x.height, x.val), reverse=True)
        root = BoardState(pieces_left=self.pieces, height=height, width=width)
        open_list.push(root, -root.f, -root.h)  # Total score -> highest h

        max_score = height*width  # in case the board isn't 10x10
        start = time.time()

        while len(open_list.internal_heap) > 0:
            if time.time() - start > 300:
                print('out of time')
            best_node = open_list.pop()

            if best_node.g == max_score:
                end = time.time()
                print(f'Solution Found in {end - start} seconds')
                return self.get_solution(best_node, open_list)

            possible_boards = best_node.expand()
            for board in possible_boards:
                open_list.push(board, -board.f, -board.g)

        print('No optimal solution found.')

    @staticmethod
    def get_solution(best_node, open_list):
        """
        Retrieves the solution found and prints it.
        :param best_node: The node with the solution
        :param open_list: The open list
        :return: The found board
        """
        print(f'Found solution')
        print(f'Open List size: {len(open_list.internal_heap)}')
        best_node.print_board()
        return best_node.board  # ToDo: make this return a nicer value
