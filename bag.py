from color import Color
from shape import Shape
from tile import Tile
import random

class Bag:
    """ Qwirkle bag of tiles.

        Attributes:
                tiles(:obj:`list` of :obj:`Tile`): List of playable tiles.

    """


    def __init__(self):
        """ The constructor initializes the default bag.

        """
        self.tiles = []
        self.set_default_bag()


    def set_default_bag(self):
        """ Returns the default list of tiles. Consist of 3 sets of
            all shapes and color combinations, 108 total.

            Returns:
                :obj:`list` of :obj:`Tile`: Default list of tiles.

        """
        self.tiles = []
        for tile_copy in range(3):
            for shape in Shape:
                for color in Color:
                    tile = Tile(color.value, shape.value)
                    self.tiles.append(tile)
        random.shuffle(self.tiles)


    def draw(self):
        """ Draws a tile from the bag.

            Returns:
                :obj:`Tile`: Drawn tile.

        """
        return self.tiles.pop()


    def discard(self, number):
        """ Discards a number of tiles from the bag.

            Args:
                number(int): Number of tiles to discard.

        """
        for discarded_tile in range(number):
            self.tiles.pop()


    def swap_all_tiles(self, bot):
        """ Swaps all the tiles of a bot hand.

            Args:
                bot(:obj:'Bot'): Bot with a hand of tiles.

        """
        tiles_to_swapp = len(bot.hand)
        for tile in bot.hand:
            self.tiles.append(tile)
        random.shuffle(self.tiles)
        bot.hand = []
        bot.draw_tiles(self)


    def is_empty(self):
        """ Indicates if the tile bag is empty.

            Returns:
                bool: True if the tile bag is empty, false otherwise.

        """
        return len(self.tiles) == 0


    def __len__(self):
        return len(self.tiles)


    def __str__(self):
        return str(self.tiles)


    def __repr__(self):
        return self.__str__()
