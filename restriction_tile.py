
class TileRestriction:
    """ Representation of a tile restriction. Used restrictions are
        'same row or col', 'same row' and 'same col'.

        Attributes:
            restriction(str): Restriction in string form.
            position(:obj:`Position`): Board position.

    """

    def __init__(self, restriction, position):
        """ The constructor receives string restriction.

            Args:
                restriction(str): Restriction in string form.
                position(:obj:`Position`): Board position.

        """
        self.restriction = restriction
        self.position = position