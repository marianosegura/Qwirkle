
class TileRestriction:
    """ Representation of a tile restriction. Used restrictions are
        'same row or col', 'same row' and 'same col'.

        Attributes:
            restriction(str): Restriction in string form.
            row(int): Board col.
            col(int): Board col.

    """

    def __init__(self, restriction):
        """ The constructor receives string restriction.

            Args:
                restriction(str): Restriction in string form.

        """
        self.restriction = restriction
        self.row = None
        self.col = None