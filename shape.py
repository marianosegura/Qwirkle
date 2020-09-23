from enum import Enum

class Shape(Enum):
    """ Enumeration of Qwirkle shapes. Shapes are: square,
        circle, diamond, clover, cross and star.

    """
    SQUARE = '■'
    CIRCLE = '●'
    DIAMOND = '◆'
    CLOVER = '♧'
    CROSS = "X"
    STAR = '★'