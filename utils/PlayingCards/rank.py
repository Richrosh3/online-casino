RANK_ORDER = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


class Rank:
    """
    Class for a card rank
    """

    def __init__(self, rank):
        self.rank = rank

    def __lt__(self, other):
        if type(other) is Rank:
            return RANK_ORDER[self.rank] < RANK_ORDER[other.rank]
        elif type(other) is str:
            return RANK_ORDER[self.rank] < RANK_ORDER[other]
        else:
            raise ValueError('"{}" type not supported for comparison'.format(type(other)))

    def __le__(self, other):
        if type(other) is Rank:
            return RANK_ORDER[self.rank] <= RANK_ORDER[other.rank]
        elif type(other) is str:
            return RANK_ORDER[self.rank] <= RANK_ORDER[other]
        else:
            raise ValueError('"{}" type not supported for comparison'.format(type(other)))

    def __eq__(self, other):
        if type(other) is Rank:
            return RANK_ORDER[self.rank] == RANK_ORDER[other.rank]
        elif type(other) is str:
            return RANK_ORDER[self.rank] == RANK_ORDER[other]
        else:
            raise ValueError('"{}" type not supported for comparison'.format(type(other)))

    def __ne__(self, other):
        if type(other) is Rank:
            return RANK_ORDER[self.rank] != RANK_ORDER[other.rank]
        elif type(other) is str:
            return RANK_ORDER[self.rank] != RANK_ORDER[other]
        else:
            raise ValueError('"{}" type not supported for comparison'.format(type(other)))

    def __gt__(self, other):
        if type(other) is Rank:
            return RANK_ORDER[self.rank] > RANK_ORDER[other.rank]
        elif type(other) is str:
            return RANK_ORDER[self.rank] > RANK_ORDER[other]
        else:
            raise ValueError('"{}" type not supported for comparison'.format(type(other)))

    def __ge__(self, other):
        if type(other) is Rank:
            return RANK_ORDER[self.rank] >= RANK_ORDER[other.rank]
        elif type(other) is str:
            return RANK_ORDER[self.rank] >= RANK_ORDER[other]
        else:
            raise ValueError('"{}" type not supported for comparison'.format(type(other)))

    def __repr__(self):
        return str(self.rank)
