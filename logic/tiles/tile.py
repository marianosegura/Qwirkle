from logic.tiles.shape import Shape
from logic.tiles.color import Color

class Tile:
    """ Qwirkle tile piece, with shape and color.

        Attributes:
            color(str): Tile color.
            shape(str): Tile shape.

    """


    def __init__(self, color, shape):
        """ The constructor receives all the attributes.

            Args:
                color(str): Tile color.
                shape(str): Tile shape.

        """
        self.color = color
        self.shape = shape


    def __str__(self):
        return '%s%s' % (self.shape, self.color)


    def __repr__(self):
        return self.__str__()

# Ready to go instances for testing
b_sqr = Tile(Color.BLUE.value, Shape.SQUARE.value)
b_crc = Tile(Color.BLUE.value, Shape.CIRCLE.value)
b_dmd = Tile(Color.BLUE.value, Shape.DIAMOND.value)
b_clv = Tile(Color.BLUE.value, Shape.CLOVER.value)
b_x = Tile(Color.BLUE.value, Shape.CROSS.value)
b_str = Tile(Color.BLUE.value, Shape.STAR.value)

r_sqr = Tile(Color.RED.value, Shape.SQUARE.value)
r_crc = Tile(Color.RED.value, Shape.CIRCLE.value)
r_dmd = Tile(Color.RED.value, Shape.DIAMOND.value)
r_clv = Tile(Color.RED.value, Shape.CLOVER.value)
r_x = Tile(Color.RED.value, Shape.CROSS.value)
r_str = Tile(Color.RED.value, Shape.STAR.value)

y_sqr = Tile(Color.YELLOW.value, Shape.SQUARE.value)
y_crc = Tile(Color.YELLOW.value, Shape.CIRCLE.value)
y_dmd = Tile(Color.YELLOW.value, Shape.DIAMOND.value)
y_clv = Tile(Color.YELLOW.value, Shape.CLOVER.value)
y_x = Tile(Color.YELLOW.value, Shape.CROSS.value)
y_str = Tile(Color.YELLOW.value, Shape.STAR.value)

g_sqr = Tile(Color.GREEN.value, Shape.SQUARE.value)
g_crc = Tile(Color.GREEN.value, Shape.CIRCLE.value)
g_dmd = Tile(Color.GREEN.value, Shape.DIAMOND.value)
g_clv = Tile(Color.GREEN.value, Shape.CLOVER.value)
g_x = Tile(Color.GREEN.value, Shape.CROSS.value)
g_str = Tile(Color.GREEN.value, Shape.STAR.value)

o_sqr = Tile(Color.ORANGE.value, Shape.SQUARE.value)
o_crc = Tile(Color.ORANGE.value, Shape.CIRCLE.value)
o_dmd = Tile(Color.ORANGE.value, Shape.DIAMOND.value)
o_clv = Tile(Color.ORANGE.value, Shape.CLOVER.value)
o_x = Tile(Color.ORANGE.value, Shape.CROSS.value)
o_str = Tile(Color.ORANGE.value, Shape.STAR.value)

p_sqr = Tile(Color.PURPLE.value, Shape.SQUARE.value)
p_crc = Tile(Color.PURPLE.value, Shape.CIRCLE.value)
p_dmd = Tile(Color.PURPLE.value, Shape.DIAMOND.value)
p_clv = Tile(Color.PURPLE.value, Shape.CLOVER.value)
p_x = Tile(Color.PURPLE.value, Shape.CROSS.value)
p_str = Tile(Color.PURPLE.value, Shape.STAR.value)