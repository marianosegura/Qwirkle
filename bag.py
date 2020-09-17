from color import Color
from shape import Shape
from tile import Tile
import random

class Bag:
    def __init__(self):
        self.tiles = []
        self.set_default_bag()

    def set_default_bag(self):
        self.tiles = []
        for tile_copy in range(3):
            for shape in Shape:
                for color in Color:
                    tile = Tile(color.value, shape.value)
                    self.tiles.append(tile)
        random.shuffle(self.tiles)

    def discard(self, number):
        for discarded_tile in range(number):
            self.tiles.pop()

    def is_empty(self):
        return len(self.tiles) == 0

    # TODO: allow multiple draw? requested > available scenario
    def draw(self, number = 1):
        drawn_tiles = []
        for tile in range(number):
            if not self.is_empty():
                drawn_tile = self.tiles.pop()
                drawn_tiles.append(drawn_tile)
        return drawn_tiles

    def trade(self, player_tiles):
        self.tiles.extend(player_tiles)
        random.shuffle(self.tiles)
        drawn_tiles = self.draw(len(player_tiles))
        return drawn_tiles

    def __len__(self):
        return len(self.tiles)

    def __str__(self):
        return str(self.tiles)

    def __repr__(self):
        return self.__str__()
