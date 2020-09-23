
class Position:
    """ Representation of a board position.

        Attributes:
            row(int): Board row.
            col(int): Board col.

    """

    def __init__(self, row, col):
        """ The constructor receives the two attributes.

        Args:
            row(int): Board row.
            col(int): Board col.

        """
        self.row = row
        self.col = col

    def __str__(self):
        return '(' + str(self.row) + ',' + str(self.col) + ')'

    def __repr__(self):
        return self.__str__()