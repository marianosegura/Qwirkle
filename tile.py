from shape import Shape
from color import Color

class Tile:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape

    def __str__(self):
        return '%s%s' % (self.shape, self.color)

    def __repr__(self):
        return self.__str__()

b_sqr = Tile(Color.BLUE.value, Shape.SQUARE.value)
b_crc = Tile(Color.BLUE.value, Shape.CIRCLE.value)
b_x = Tile(Color.BLUE.value, Shape.CROSS.value)
b_clo = Tile(Color.BLUE.value, Shape.CLOVER.value)
r_sqr = Tile(Color.RED.value, Shape.SQUARE.value)
r_crc = Tile(Color.RED.value, Shape.CIRCLE.value)
r_x = Tile(Color.RED.value, Shape.CROSS.value)
r_clo = Tile(Color.RED.value, Shape.CLOVER.value)