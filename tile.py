
class Tile:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape

    def __str__(self):
        return '%s%s' % (self.shape, self.color)

    def __repr__(self):
        return self.__str__()