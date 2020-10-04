
class TileCombo:
    """ Tile moves done by a player in its turn. Keeps track
        of a list of tiles, played positions.

        Attributes:
            tiles(:obj:`list` of :obj:`Tile`): List of played tiles.
            positions(:obj:`list` of :obj:`Position`): List of played positions.

    """


    def __init__(self):
        """ The constructor initiates the attributes as empty.
        """
        self.tiles = []
        self.positions = []


    def add_move(self, tile, position):
        """ Appends a tile move to the attribute lists.

            Args:
                tile(:obj:`Tile`): Played tile.
                position(:obj:`Position`): Played position.

        """
        self.tiles.append(tile)
        self.positions.append(position)


    def discard_last_move(self):
        """ Deletes the last tile move from the attribute lists.

        """
        self.tiles.pop()
        self.positions.pop()


    def copy(self):
        """ Creates a shallow copy of the instance.

        """
        copy = TileCombo()
        copy.tiles.extend(self.tiles)
        copy.positions.extend(self.positions)
        return copy


    def __len__(self):
        return len(self.tiles)


    def __str__(self):
        to_string = ''
        for i in range(len(self.tiles)):
            to_string += str(self.tiles[i]) + str(self.positions[i]) + ' -> '
        to_string = to_string[:-3] # remove last arrow pointing to nothing
        return to_string


    def __repr__(self):
        return self.__str__()