from position import Position
from restriction_tile import TileRestriction
from tile_combo import TileCombo

class Bot:
    """ Simple bot that plays the move that produces the most points
        in his turn.

        Attributes:
            hand(:obj:`list` of :obj:`Tile`): List of playable tiles.
            points(int): Bot current points.
    """


    def __init__(self):
        self.hand = []
        self.points = 0


    def get_best_combo(self, board):
        """ Decides combo to play in a turn for a given board, based on current tile hand.
            Uses find_valid_combos backtracking method to find all the possible plays and returns
            the one that scores the most points.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.

            Returns:
                :obj:`TileCombo`: Steps that indicates which tiles to play in which positions.
        """
        combos = []  # list of TileCombo objects

        self.find_valid_combos(board, combos)  # list is passed as reference to fill it

        if not combos:  # rare condition where nothing can be played with the current hand
            return None

        best_combo = combos[0]
        best_points = self.get_combo_points(board, best_combo)

        for combo_option in combos:
            if self.get_combo_points(board, combo_option) > best_points:
                best_combo = combo_option # update best combo
                best_points = self.get_combo_points(board, best_combo) # update its points

        return best_combo


    def find_valid_combos(self, board, combos, hand_index = 0, tile_combo = TileCombo()):
        """ Find all valid plays for a given tile hand and board using backtracking.
            Returns in its argument plays as a list of TileCombo objects.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.
                combos(:obj:`list` of :obj:`TileCombo`): List of all valid tile combos.
                hand_index(int): Current index of the position in the tile hand being verified.
                                 Goes from 0 to the last index in the hand
                tile_combo(:obj:`TileCombo`): TileCombo object used to permute all the valid solutions.

        """
        # all tiles were used for a tile_combo solution
        if hand_index >= len(self.hand):
            return

        # look for valid tile moves in the at the current hand index
        for i in range(hand_index, len(self.hand)):
            tile = self.hand[i]

            # iterate for all the playable positions for the given tile
            # with the current played turn moves
            playable_positions = self.get_playable_positions(board, tile_combo)

            for playable_position in playable_positions:

                # tile is valid in the playable position?
                if self.is_valid_move(board.board, tile, playable_position):
                    # save states to backtrack later
                    board_state = board.get_state()  # save board state
                    board.play_tile(tile, playable_position)  # move into board
                    tile_combo.add_move(tile, playable_position)  # move into turn moves

                    # at this point we have created a new valid play permutation
                    # this permutation don't use all hand tiles (that is caught in the first if statement)
                    combos.append(tile_combo.copy())  # add valid play

                    # swap to look for all other possible tile moves linked to this one
                    self.swap(self.hand, hand_index, i)

                    # search for bigger combos that include the current combo
                    self.find_valid_combos(board, combos, hand_index + 1, tile_combo)

                    # restore previous state / backtrack
                    board.restore_state(board_state)  # restore board
                    tile_combo.discard_last_move()  # restore combo
                    self.swap(self.hand, hand_index, i)  # restore hand


    def swap(self, list_, i, j):
        """ Swaps two the values of two positions in a list.

            Args:
                list_(:obj:`list`): List to swap positions.
                i(int): First position to swap.
                j(int): second position to swap.

            """
        list_[i], list_[j] = list_[j], list_[i]


    def get_playable_positions(self, board, tile_combo):
        """ Returns all playable positions of the board, given the player
            tile moves in the turn.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.
                tile_combo(:obj:`TileCombo`): Tile movements made by a player.

            Returns:
                :obj:`list` of :obj:`Position`: List of playable  positions.

        """
        # the only playable position on a empty board is (0, 0)
        if board.is_empty():
            return [Position(0, 0)]
                                                                           # Xrd(1,0) -> Xgr(2,1) -> ★rd(2,4)
        # current positions of the played tiles of the combo
        combo_positions = board.get_current_tiles_positions(tile_combo.tiles)

        restriction = None
        # if the combo isn't empty there are restrictions
        if len(tile_combo) >= 1:
            first_tile_position = combo_positions[0]
            if len(tile_combo) == 1:
                restriction = TileRestriction('same row or col', first_tile_position)
            if len(tile_combo) >= 2:
                if first_tile_position.row == combo_positions[1].row:
                    restriction = TileRestriction('same row', first_tile_position)
                else:
                    restriction = TileRestriction('same col', first_tile_position)

        playable_positions = []
        # if combo is not empty, search adjacent tiles to the already played tiles
        # else search adjacent to all the board tiles
        search_positions = combo_positions if len(tile_combo) >= 1 else board.played_positions

        for played_position in search_positions:
            adjacent_empty_positions = self.get_adjacent_empty_positions(board.board, played_position)
            playable_positions.extend(adjacent_empty_positions)

        playable_positions = self.filter_positions(playable_positions, restriction)

        return playable_positions


    def filter_positions(self, positions, tile_restriction):
        """ Filters a list of positions based on a tile restriction.

            Args:
                positions(:obj:`list` of :obj:`Position`): List of positions to filter.
                tile_restriction(:obj:'TileRestriction'): Restriction reference to filter.

            Returns:
                :obj:`list` of :obj:`Position`: List of filtered positions.

        """
        # not need to filter when restriction is None
        if not tile_restriction:
            return positions

        restriction = tile_restriction.restriction

        filtered_positions = []
        for position in positions:
            valid_tile = False

            if restriction == 'same row':
                valid_tile = (position.row == tile_restriction.position.row)
            elif restriction == 'same col':
                valid_tile = (position.col == tile_restriction.position.col)
            elif restriction == 'same row or col':
                valid_tile = (position.row == tile_restriction.position.row or position.col == tile_restriction.position.col)

            if valid_tile:
                filtered_positions.append(position)
        return filtered_positions


    def get_adjacent_empty_positions(self, board, position):
        """ Returns the empty positions adjacent to a position.
            Looks up, down, right and left of the position.

            Args:
                board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.
                position(:obj:'Position'): Board position of row and column.

            Returns:
                :obj:`list` of :obj:`Position`: List of adjacent empty positions.

        """
        adjacent_empty_positions = []
        row, col = position.row, position.col

        # left empty position?
        if col > 0 and not board[row][col - 1]:
            adjacent_empty_positions.append(Position(row, col - 1))

        # right empty position?
        if col < len(board[0]) - 1 and not board[row][col + 1]:
            adjacent_empty_positions.append(Position(row, col + 1))

        # up empty position?
        if row > 0 and not board[row - 1][col]:
            adjacent_empty_positions.append(Position(row - 1, col))

        # down empty position?
        if row < len(board) - 1 and not board[row + 1][col]:
            adjacent_empty_positions.append(Position(row + 1, col))

        return adjacent_empty_positions


    def is_valid_move(self, board, tile, position):
        """ Determines if a tile move if valid. Checks vertically and horizontally.

            Args:
                board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.
                tile(:obj:'Tile'): Tile used to know its shape and color.
                position(:obj:'Position'): Board position of row and column.

            Returns:
                bool: True if the move is valid, false otherwise.

        """
        row = position.row
        col = position.col

        if len(board[0]) == 1:
            valid_position = (row == 0 and col == 0)
            return valid_position

        rows = len(board)
        cols = len(board[0])

        out_of_index = (row < 0) or (row >= rows) or (col < 0) or (col >= cols)
        if out_of_index:
            #print("out of index")
            return False

        space_taken = board[row][col]
        if space_taken:
            #print("space taken")
            return False

        # at least 1 adjacent tile?
        adjacent_tile = row != 0 and board[row - 1][col] or \
                        row != rows - 1 and board[row + 1][col] or \
                        col != 0 and board[row][col - 1] or \
                        col != cols - 1 and board[row][col + 1]
        if not adjacent_tile:
            #print("no adjacent tile")
            return False

        # verify horizontal line
        horizontal_line = self.get_adjacent_horizontal_line(board, tile, row, col)
        if not self.is_valid_line(horizontal_line):
            #print("invalid horizontal line")
            #print(horizontal_line)
            return False

        # verify vertical line
        vertical_line = self.get_adjacent_vertical_line(board, tile, row, col)
        if not self.is_valid_line(vertical_line):
            #print("invalid vertical line")
            #print(vertical_line)
            return False

        # its a valid move, meets all rules
        return True


    def get_adjacent_horizontal_line(self, board, tile, row, col):
        """ Returns the tiles linked vertically to a tile and its position.
            Searches up and down from the given position.

            Args:
                board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.
                tile(:obj:'Tile'): Reference tile to determine the adjacent tiles.
                row(int): Board row to determine the adjacent tiles.
                col(int): Board column to determine the adjacent tiles.

            Returns:
                :obj:`list` of :obj:`Tile`: List of tiles linked vertically to the tile.

        """
        horizontal_line = [tile]

        # append right side
        col_index = col + 1
        while col_index < len(board[0]) and board[row][col_index]:
            horizontal_line.append(board[row][col_index])
            col_index += 1

        # append left side
        col_index = col - 1
        while col_index >= 0 and board[row][col_index]:
            horizontal_line.append(board[row][col_index])
            col_index -= 1
        return horizontal_line


    def get_adjacent_vertical_line(self, board, tile, row, col):
        """ Returns the tiles linked horizontally to a tile and its position.
            Searches to the right and left from the given position

            Args:
                board(:obj:`list` of :obj:`Tile`): Two-dimensional list of tiles or zeros.
                tile(:obj:'Tile'): Reference tile to determine the adjacent tiles.
                row(int): Board row to determine the adjacent tiles.
                col(int): Board column to determine the adjacent tiles.

            Returns:
                :obj:`list` of :obj:`Tile`: List of tiles linked horizontally to the tile.

        """
        vertical_line = [tile]

        # append upper side
        row_index = row + 1
        while row_index < len(board) and board[row_index][col]:
            vertical_line.append(board[row_index][col])
            row_index += 1

        # append lower side
        row_index = row - 1
        while row_index >= 0 and board[row_index][col]:
            vertical_line.append(board[row_index][col])
            row_index -= 1
        return vertical_line


    def is_valid_line(self, line):
        """ Indicates if a line of tiles is valid. A line is valid when
            all the tiles share either shape or color.

            Args:
                line(:obj:`list` of :obj:`Tile`): The first parameter.

            Returns:
                True if the line is valid, false otherwise.

        """
        # lines of 1 or 0 tiles are valid
        if len(line) <= 1:
            return True

        # use first two tiles to determine common aspect
        common_aspect = None
        common_value = None
        if line[0].shape == line[1].shape:
            common_aspect = 'shape'
            common_value = line[0].shape
        if line[0].color == line[1].color:
            common_aspect = 'color'
            common_value = line[0].color

        # first 2 tiles are incompatible
        if not common_aspect:
            return False

        # set to look for duplicates
        seen_tiles = set()
        for tile in line:
            # duplicate tile?
            duplicate = str(tile) in seen_tiles

            # has same color or shape as the rest of the line?
            invalid_tile = False
            if common_aspect == 'shape':
                invalid_tile = tile.shape != common_value
            else:
                invalid_tile = tile.color != common_value

            if duplicate or invalid_tile:
                return False
            else:
                seen_tiles.add(str(tile))
        return True


    def get_combo_points(self, board_object, tile_combo):
        """ Calculates the total points of a tile turn combo.

            Args:
                board_object(:obj:`Board`): Board object instance with the current game state.
                tile_combo(:obj:`TileCombo`): Tile movements made by a player.

            Returns:
                int: Turn steps' points.

        """
        board_state = board_object.get_state()  # save to restore later

        self.play_combo(board_object, tile_combo)
        # recover the updated positions of the played tiles
        played_positions = board_object.get_current_tiles_positions(tile_combo.tiles)

        board = board_object.board
        points = 0
        seen_lines = [] # list of lines as python sets
        for step_index in range(len(tile_combo)):
            played_tile = tile_combo.tiles[step_index]
            played_pos = played_positions[step_index]

            horizontal_line = self.get_adjacent_horizontal_line(board, played_tile, played_pos.row, played_pos.col)
            line_set = set(horizontal_line)
            # lines of length 1 are omitted since they aren't combos
            # seen lines are omitted to avoid counting twice the same line points
            if len(line_set) > 1 and not line_set in seen_lines:
                seen_lines.append(line_set) # append to seen lines
                points += self.get_tile_line_points(line_set) # add points

            vertical_line = self.get_adjacent_vertical_line(board, played_tile, played_pos.row, played_pos.col)
            line_set = set(vertical_line)
            if len(line_set) > 1 and not line_set in seen_lines:
                seen_lines.append(line_set)
                points += self.get_tile_line_points(line_set)

        board_object.restore_state(board_state)
        return points


    @staticmethod
    def play_combo(board, tile_combo):
        """ Plays all the moves in a tile_combo object on a given board.

            Args:
                board(:obj:`Board`): Board object with the current game state.
                tile_combo(:obj:`TileCombo`): Tile movements.

        """
        for step_index in range(len(tile_combo)):
            tile = tile_combo.tiles[step_index]
            pos = tile_combo.positions[step_index]
            board.play_tile(tile, pos)


    @staticmethod
    def get_tile_line_points(tile_line):
        """ Calculates the total points of a line of tiles. A lines of length 6 is
            a qwirkle and its points are doubled (that's 12 always).

            Args:
                tile_line(:obj:`list` of :obj:`Tile`): List of tiles.

            Returns:
                int: Tile line' points.

        """
        if len(tile_line) == 6:
            #print("qwirkle")
            return 12
        else:
            return len(tile_line)


    def draw_tiles(self, bag):
        """ Calculates the total points of a line of tiles. A lines of length 6 is
                    a qwirkle and its points are doubled (that's 12 always).

                    Args:
                        tile_line(:obj:`list` of :obj:`Tile`): List of tiles.

                    Returns:
                        int: Tile line' points.

        """
        while len(self.hand) < 6 and not bag.is_empty():
            self.hand.append(bag.draw())


    def out_of_tiles(self):
        """ Indicates if the bot is out of tiles.

            Returns:
                bool: True if hand is empty, false otherwise.

        """
        return len(self.hand) == 0


    def remove_tiles_from_hand(self, tiles):
        """ Removes a list of tiles from the hand. Though to be used after a combo is played.

            Args:
                tiles(:obj:`list` of :obj:`Tile`): List of tiles.

        """
        for tile in tiles:
            self.hand.remove(tile)


    def __str__(self):
        return "Points bot: " + str(self.points) + "pts " + str(self.hand)

