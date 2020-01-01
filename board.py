import copy


class BoardState:

    def __init__(self, pieces_left, parent=None, location=None, height=10, width=10):
        """
        A class representing a state of a board.
        :param parent: The state of the board previously.
        :param location: a tuple representing the location of the piece that is being placed. The location will be the
         top left corner of the piece, even if it's a 0.
        :param height: Height of board.
        :param width: Width of board.
        :param parent: The previous board
        :param pieces_left: a list of pieces left.
        """
        if parent:
            self.__place_piece(parent.board, location, pieces_left[0])
            self.g = parent.g + pieces_left[0].val
            self.pieces_left = pieces_left[1:]  # remove the first piece
        else:  # root node
            self.board = [[0 for i in range(height)] for j in range(width)]  # The board we will place the pieces on
            self.g = 0
            self.pieces_left = pieces_left
        self.parent = parent
        self.h = self.__calc_h()  # Boards with larger open spaces are better.
        self.f = self.g + self.h

    def expand(self):
        """
        returns a list of all possible states that we can reach from the current board. Will attempt to place the next
        piece available
        :return: A list of all possible boards.
        """
        piece = self.pieces_left[0]
        possible_boards = []

        for row, row_val in enumerate(self.board):
            for col, col_val in enumerate(row_val):
                if self.__is_placement_legal(row, col, piece):
                    new_board = BoardState(self.pieces_left, self, (row, col))
                    if new_board.__can_contain_remaining_pieces():
                        possible_boards.append(new_board)

        return possible_boards

    def __calc_h(self):
        """
        A heuristic for calculating how good this placement is. We will find the largest sub-matrix of 0s in the board,
        since a board that has more open space is likely to be better than one with spread pieces.
        :return: The calculated h value, b
        """
        return self.__max_rectangle(self.board) / 100  # normalize it so we dont keep searching empty boards


    @staticmethod
    def __max_rectangle(board):
        """
        Returns area of the largest rectangle with all 0s
        :return: int, the size of the rectangle.
        """
        rows = len(board)
        cols = len(board[0])
        ans = 0
        d = [-1 for i in range(cols)]
        left_border = [0 for i in range(cols)]
        right_border = [0 for i in range(cols)]
        st = []

        for i in range(rows):
            for j in range(cols):
                if board[i][j] != 0:  # isn't empty
                    d[j] = i

            for j in range(cols):
                while len(st) > 0 and d[st[-1]] <= d[j]:
                    st.pop(-1)
                left_border[j] = -1 if len(st) == 0 else st[-1]
                st.append(j)

            st = []

            for j in range(cols - 1, -1, -1):
                while len(st) > 0 and d[st[-1]] <= d[j]:
                    st.pop(-1)

                right_border[j] = cols if len(st) == 0 else st[-1]
                st.append(j)

            st = []

            for j in range(cols):
                ans = max(ans, (i - d[j]) * (right_border[j] - left_border[j] - 1))
        return ans

    def __place_piece(self, prev_board, location, piece):
        """
        Place the given piece on the board. placement contains a 2d list describing the dimensions, the location to
        place and piece number.
        :param piece: The piece being placed.
        :param prev_board: the current state of board (before placing a piece)
        :param location: a tuple (x, y) where the corner of the piece will be.
        :return: updates the self.board field
        """

        new_board = copy.deepcopy(prev_board)  # begin from parents board.
        start_x, start_y = location

        for row, row_val in enumerate(piece.shape):
            for col, col_val in enumerate(row_val):
                # We'll check if the piece spills out or the place isn't empty
                if (start_x + piece.height - 1 >= len(prev_board) or start_y + piece.width - 1 >= len(prev_board)) or \
                        (new_board[start_x + row][start_y + col] != 0 and piece.shape[row][col] != 0):
                    raise IndexError('The piece cannot be placed here.')
                if piece.shape[row][col] != 0:  # Not an empty tile
                    new_board[row + start_x][col + start_y] = piece.idx  # update it

        self.board = new_board

    def __is_placement_legal(self, start_x, start_y, piece):
        """
        Function that checks if a piece can be placed on this board. Useful for skipping bad boards.
        :param piece: A PuzzlePiece object.
        :return: True if it can be placed, false otherwise
        """

        max_row = start_x + piece.height - 1  # We decrement since the piece actually begins at start_x
        max_col = start_y + piece.width - 1

        if max_row >= len(self.board) or max_col >= len(self.board[0]):  # the piece spills out
            return False

        for row in range(piece.height):
            for col in range(piece.width):
                if self.board[row + start_x][col + start_y] != 0 and piece.shape[row][col] != 0:  # place isn't empty
                    return False

        return True

    def __can_contain_remaining_pieces(self):
        """
        important function for pruning unwanted boards. If the given board cannot contain at least one of the pieces
        left, we should discard it. Additionally, we check if the current placement leaves unusable spaces (impossible
        when we can fill the whole board). Long computation time but powerful pruning potential.
        :return: True if it can contain remaining pieces (supposedly), false otherwise.
        """
        for piece in self.pieces_left:
            if not self.__has_space(piece):
                return False

        return self.__no_unusable_space()

    def __has_space(self, piece):
        """
        Checks if the board has place to place this specific piece.
        :param piece: A piece.
        :return: True if it can, false otherwise.
        """
        for row, row_val in enumerate(self.board):  # ToDo: think of better way to do this
            for col, col_val in enumerate(row_val):
                if self.__is_placement_legal(row, col, piece):
                    return True

        return False

    def __no_unusable_space(self):
        """
        Function that checks if this board has any unusable cells, i.e small empty areas that no piece can fill.
        :return: True if has useless space, false otherwise.
        """
        fillable_tiles = set()  # all tiles that can be filled
        for row, rv in enumerate(self.board):  # add the already occupied tiles
            for col, cv in enumerate(rv):
                if cv != 0:
                    fillable_tiles.add((row, col))

        for row, rv in enumerate(self.board):
            for col, cv in enumerate(rv):
                for piece in self.pieces_left:
                    if self.__is_placement_legal(row, col, piece):
                        for i, i_val in enumerate(piece.shape):
                            for j, tile in enumerate(i_val):
                                if tile != 0:
                                    fillable_tiles.add((row + i, col + j))

        #poss_tiles = {(i, j) for i in range(10) for j in range(10)}
        #missing_tiles = poss_tiles - fillable_tiles
        return len(fillable_tiles) == len(self.board) * len(self.board[0])

    def print_board(self):
        print('-----------------------')
        for row in self.board:
            for tile in row:
                print(chr(ord('A') - 1 + tile), end='')
            print('\n', end='')
