from position import Position
from restriction_tile import TileRestriction


class Board:
    """ The game board manages the state of the board and the played
        positions.

        Attributes:
            board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.
            played_positions(:obj:`list` of :obj:`Position`): List of the positions played.

    """


    def __init__(self, board = [[0]]):
        """ The constructor can receive a board. Default board is empty.

            Args:
                board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.

        """
        self.board = board
        self.played_positions = []
        if board != [[0]]:
            self.played_positions = self.get_played_positions(board)


    def get_played_positions(self, board):
        """ Returns all played positions in a board.

            Args:
                board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.

            Returns:
                :obj:`list` of :obj:`Position`: List of played  positions.

        """
        played_positions = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col]:
                    played_position = Position(row, col)
                    played_positions.append(played_position)
        return played_positions


    def play_tile(self, tile, position):
        """ Determines if a tile move if valid. Checks vertically and horizontally.

            Args:
                tile(:obj:'Tile'): Played tile.
                position(:obj:'Position'): Board row and column to insert the tile.

        """
        self.board[position.row][position.col] = tile
        self.played_positions.append(position)
        self.adjust_padding()


    def adjust_padding(self):
        """ Inserts padding to the board if needed. Is needed when a tile is in
            at the most outer layer of the board (first or last column or row).
            Void spaces are needed always at the outer layer to make be able to
            make moves.
            The played positions adjust is called just for top and left padding,
            since they change the row and columns of the original placed tiles.

        """
        top = first = 0

        # check top padding
        if any(self.board[top]):  # any tile in first row?
            self.board.insert(0, [0] * len(self.board[0]))
            self.adjust_played_positions(1, 0)

            # check bottom padding
        bottom = len(self.board) - 1
        if any(self.board[bottom]):  # any tile in last row?
            self.board.append([0] * len(self.board[0]))

        # check left padding
        for row in self.board:
            if row[first]:  # any tile in first column?
                for i in range(len(self.board)):
                    self.board[i].insert(0, 0)
                self.adjust_played_positions(0, 1)
                break;

        # check right padding
        last = len(self.board[0]) - 1
        for row in self.board:
            if row[last]:  # any tile in last column?
                for i in range(len(self.board)):
                    self.board[i].append(0)
                break;


    def adjust_played_positions(self, row_offset, col_offset):
        """ Adjust the played positions by an offset, after a padding happens.

            Args:
                row_offset(int): row offset applied to get the updated position in the board.
                col_offset(int): col offset applied to get the updated position in the board.

        """
        for played_pos in self.played_positions:
            played_pos.row += row_offset
            played_pos.col += col_offset


    def get_state(self):
        """ Returns the board state as a shallow copy of its tile matrix.

        """
        # create null matrix of self.board dimensions
        copy = [ [ 0 for col in range(len(self.board[0])) ] for row in range(len(self.board)) ]
        # copy played tiles
        for pos in self.played_positions:
            copy[pos.row][pos.col] = self.board[pos.row][pos.col]
        return copy


    def restore_state(self, state):
        """ Restores the state of the board. Sets board and played_positions.

            Args:
                state(:obj:`list` of :obj:`Tile`): State as two-dimensional list of tiles or zeros.

        """
        self.board = state
        self.played_positions = self.get_played_positions(state)


    def __str__(self):
        to_string = ""
        for row in self.board:
            for tile in row:
                if tile == 0:
                    to_string += "0   "
                else:
                    to_string += str(tile) + " "
            to_string += "\n"
        return to_string


    def __len__(self):
        return len(self.board)
