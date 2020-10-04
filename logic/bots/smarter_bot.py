from logic.bots.bot import Bot


class SmarterBot(Bot):
    """ Smart bot that take into account combo points, qwirkle chances caused and
        possible lines killed to play combo.

        Attributes:
            hand(:obj:`list` of :obj:`Tile`): List of playable tiles.
            points(int): Bot current points.
    """


    def get_best_combo(self, board):
        """ Returns the smartest tile combo it founds for a turn.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.

            Returns:
                :obj:`TileCombo`: Smartest combo found.

        """
        combos = []  # list of TileCombo objects

        self.find_valid_combos(board, combos)  # list is passed as reference to fill it

        if not combos:  # rare condition where nothing can be played with the current hand
            return None

        # Smartest combo properties are hold for efficiency
        smartest_combo = combos[0]
        smart_points = self.get_combo_points(board, smartest_combo)
        smart_chances = self.get_qwirkle_chances_caused(board, smartest_combo)
        smart_kills = self.get_possible_lines_killed(board, smartest_combo)

        for combo_option in combos:
            smartest_combo = self.pick_smarter_combo(board, smartest_combo, smart_points, smart_chances, smart_kills, combo_option)

            # update smartest combo properties if combo changed
            if smartest_combo == combo_option:
                smart_points = self.get_combo_points(board, smartest_combo)
                smart_chances = self.get_qwirkle_chances_caused(board, smartest_combo)
                smart_kills = self.get_possible_lines_killed(board, smartest_combo)

        #print(smartest_combo)
        return smartest_combo


    def pick_smarter_combo(self, board, combo1, points1, chances1, kills1, combo2):
        """ Picks the smarter combo between two options. In descending order of smartness are
            considered: less qwirkle chances caused, more combo points and less possible lines killed.

            Args:
                board(:obj:`Board`): Board object instance with the current game state.
                combo1(:obj:`TileCombo`): First combo option.
                points1(int): First combo points.
                chances1(int): First combo qwirkle chances caused.
                kills1(int): First combo possible lines killed.
                combo2(:obj:`TileCombo`): Second combo option.

            Returns:
                :obj:`TileCombo`: Smarter combo option.

        """
        points2 = self.get_combo_points(board, combo2)
        chances2 = self.get_qwirkle_chances_caused(board, combo2)
        kills2 = self.get_possible_lines_killed(board, combo2)

        smarter = combo1

        if chances2 < chances1:
            smarter = combo2
        elif points2 > points1 and chances2 == chances1:
            smarter = combo2
        elif points2 == points1 and kills2 <= kills1 and chances2 == chances1:
            smarter = combo2

        return smarter


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
                        if possible_line_len <= 6 and not self.is_valid_line(line) and cells_traversed != 1:
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
                        if possible_line_len <= 6 and not self.is_valid_line(line) and cells_traversed != 1:
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
                        if possible_line_len <= 6 and not self.is_valid_line(line) and cells_traversed != 1:
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
                        if possible_line_len <= 6 and not self.is_valid_line(line) and cells_traversed != 1:
                            lines_killed += 1 # line down killed
                        break
                    row += 1
                    cells_traversed += 1

        board_object.restore_state(board_state)
        return lines_killed


    def __str__(self):
        return "Smart bot: " + str(self.points) + "pts " + str(self.hand)

