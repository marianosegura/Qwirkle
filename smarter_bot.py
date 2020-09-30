from bot import Bot

class SmarterBot(Bot):
    """ Smart bot that take into account combo points, qwirkle chances caused and
        possible lines killed to play combo.

        Attributes:
            hand(:obj:`list` of :obj:`Tile`): List of playable tiles.
            points(int): Bot current points.
    """

    def get_smartest_combo(self, board):
        """ Returns the smartest tile combo it founds for a turn.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.

            Returns:
                :obj:`TileCombo`: Smartest combo found.

        """
        combos = [] # list of TileCombo objects
        self.find_valid_plays(board, combos) # list is passed as reference to fill it

        smartest_combo = combos[0]
        for combo_option in combos:
            smartest_combo = self.pick_smarter_combo(board, smartest_combo, combo_option)

        #print(smartest_combo)
        return smartest_combo


    def pick_smarter_combo(self, board, combo1, combo2):
        """ Picks the smarter combo between two options. In descending order of smartness are
            considered: less qwirkle chances caused, more combo points and less possible lines killed.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.
                combo1(:obj:`TileCombo`): First combo option.
                combo2(:obj:`TileCombo`): Second combo option.

            Returns:
                :obj:`TileCombo`: Smarter combo option.

        """
        points1 = self.get_combo_points(board, combo1)
        chances1 = self.get_qwirkle_chances_caused(board, combo1)
        kills1 = self.get_possible_lines_killed(board, combo1)

        points2 = self.get_combo_points(board, combo2)
        chances2 = self.get_qwirkle_chances_caused(board, combo2)
        kills2 = self.get_possible_lines_killed(board, combo2)

        smarter = combo2
        if points1 > points2 and chances1 <= chances2 and kills1 <= kills2:
            smarter = combo1
        elif points1 > points2 and chances1 <= chances2:
            smarter = combo1
        elif chances1 < chances2 and kills1 <= kills2:
            smarter = combo1
        elif chances1 < chances2:
            smarter = combo1
        return smarter


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
        played_positions = board_object.played_positions[(len(board_object.played_positions) - len(tile_combo)):]

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
    def get_tile_line_points(tile_line):
        """ Calculates the total points of a line of tiles. A lines of length 6 is
            a qwirkle and its points are doubled (that's 12 always).

            Args:
                tile_line(:obj:`list` of :obj:`Tile`): List of tiles.

            Returns:
                int: Tile line' points.

        """
        if len(tile_line) == 6:
            return 12
        else:
            return len(tile_line)


    def get_qwirkle_chances_caused(self, board, tile_combo):
        """ Counts the qwirkle chances caused by a set of tile moves for the next player.
            A qwirkle chance is caused when a tile line is left with 5 tiles.

            Args:
                board_object(:obj:`Board`): Board object instance with the current game state.
                tile_combo(:obj:`TileCombo`): Tile movements made by a player.

            Returns:
                int: Number of lines killed.

        """
        board_state = board.get_state() # save to restore later

        chances = 0
        for step_index in range(len(tile_combo)): # iterate all turn steps
            tile = tile_combo.tiles[step_index]
            pos = tile_combo.positions[step_index]

            # the length of the linked vertical and horizontal combos are the reference
            horizontal_combo = len(self.get_adjacent_horizontal_line(board.board, tile, pos.row, pos.col))
            vertical_combo = len(self.get_adjacent_vertical_line(board.board, tile, pos.row, pos.col))

            # when a qwirkle is made and chances are more than zero means
            # the player placed the 5th and 6th tile in the line.
            # when the player place the 5th tile a chance was added, but it is not a
            # chance for a rival because the player itself made the qwirkle.
            # hence, that chance need to be subtracted
            if horizontal_combo == 6 and chances > 0:
                chances -= 1
            if vertical_combo == 6 and chances > 0:
                chances -= 1

            if horizontal_combo == 5:
                chances += 1
            if vertical_combo == 5:
                chances += 1

            board.play_tile(tile_combo.tiles[step_index], tile_combo.positions[step_index])

        board.restore_state(board_state)
        return chances


    def get_possible_lines_killed(self, board_object, tile_combo):
        """ Counts the possible lines killed by a given set of tile movements.
            A line is killed when a line could have been linked between the played tile and another
            tile towards a direction (separated by empty cells) but due to the color or shape of
            the played tile it isn't a valid line of tiles.

            Args:
                board_object(:obj:`Board`): Board object instance with the current game state.
                tile_combo(:obj:`TileCombo`): Tile movements made by a player.

            Returns:
                int: Number of lines killed.

        """
        lines_killed = 0 # can be 4 max, because of the 4 directions
        board_state = board_object.get_state()  # save to restore later

        self.play_combo(board_object, tile_combo)
        # recover the updated final positions of the played tiles
        updated_positions = board_object.played_positions[(len(board_object.played_positions) - len(tile_combo)):]

        board = board_object.board # the 2d array of lists
        for step_index in range(len(tile_combo)):
            tile = tile_combo.tiles[step_index]
            pos = updated_positions[step_index]

            # the adjacent cell in that direction has to be empty (0) to evaluate a possible killed line
            # search to the left
            if pos.col > 1 and board[pos.row][pos.col - 1] == 0:
                col = pos.col - 2 # column index moved to search a tile
                cells_traversed = 1 # if 5 cells empty are traversed a line isn't possible in that direction
                while col > 0 and cells_traversed < 5:
                    tile_found = (board[pos.row][col] != 0)
                    if tile_found:
                        # the line linked to the played tile
                        line = self.get_adjacent_horizontal_line(board, tile, pos.row, pos.col)
                        # the line linked to the found found is appended to the line
                        line.extend(self.get_adjacent_horizontal_line(board, board[pos.row][col], pos.row, col))
                        possible_line_len = len(line) + cells_traversed # possible line can be length 6 max to be valid
                        if possible_line_len <= 6 and not self.is_valid_line(line):
                            lines_killed += 1 # line to the left killed
                        break
                    col -= 1
                    cells_traversed += 1

            # search to the right
            if pos.col + 1 < len(board[0]) and board[pos.row][pos.col + 1] == 0:
                col = pos.col + 2 # column index moved to search a tile
                cells_traversed = 1
                while col < len(board[0]) and cells_traversed < 5:
                    tile_found = (board[pos.row][col] != 0)
                    if tile_found:
                        line = self.get_adjacent_horizontal_line(board, tile, pos.row, pos.col)
                        line.extend(self.get_adjacent_horizontal_line(board, board[pos.row][col], pos.row, col))
                        possible_line_len = len(line) + cells_traversed
                        if possible_line_len <= 6 and not self.is_valid_line(line):
                            lines_killed += 1 # line to the right killed
                        break
                    col += 1
                    cells_traversed += 1

            # search up
            if pos.row > 1 and board[pos.row - 1][pos.col] == 0:
                row = pos.row - 2 # row index moved to search a tile
                cells_traversed = 1
                while row > 0 and cells_traversed < 5:
                    tile_found = (board[row][pos.col] != 0)
                    if tile_found:
                        line = self.get_adjacent_vertical_line(board, tile, pos.row, pos.col)
                        line.extend(self.get_adjacent_vertical_line(board, board[row][pos.col], row, pos.col))
                        possible_line_len = len(line) + cells_traversed
                        if possible_line_len <= 6 and not self.is_valid_line(line):
                            lines_killed += 1 # line up killed
                        break
                    row -= 1
                    cells_traversed += 1


            # search down
            if pos.row + 1 < len(board) and board[pos.row + 1][pos.col] == 0:
                row = pos.row + 2 # row index moved to search a tile
                cells_traversed = 1
                while row < len(board) and cells_traversed < 5:
                    tile_found = (board[row][pos.col] != 0)
                    if tile_found:
                        line = self.get_adjacent_vertical_line(board, tile, pos.row, pos.col)
                        line.extend(self.get_adjacent_vertical_line(board, board[row][pos.col], row, pos.col))
                        possible_line_len = len(line) + cells_traversed
                        if possible_line_len <= 6 and not self.is_valid_line(line):
                            lines_killed += 1 # line down killed
                        break
                    row += 1
                    cells_traversed += 1

        board_object.restore_state(board_state)
        return lines_killed


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
