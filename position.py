
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return '(' + str(self.row) + ',' + str(self.col) + ')'

    def __repr__(self):
        return self.__str__()