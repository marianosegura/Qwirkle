
class PlaySteps:
    def __init__(self):
        self.tiles = []
        self.positions = []
        self.points = 0

    def append(self, tile, position):
        self.tiles.append(tile)
        self.positions.append(position)

    def pop(self):
        self.tiles.pop()
        self.positions.pop()

    def __len__(self):
        return len(self.tiles)

    def __str__(self):
        to_string = ''
        for i in range(len(self.tiles)):
            to_string += str(self.tiles[i]) + str(self.positions[i]) + ' -> '
        to_string = to_string[:-3] # remove last arrow pointing to nothing
        return to_string