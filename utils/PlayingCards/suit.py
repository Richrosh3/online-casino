SUIT_ORDER = {'D': 1, 'C': 2, 'H': 3, 'S': 4}


class Suit:

    def __init__(self, suit):
        self.suit = suit

    def __lt__(self, other):
        if isinstance(other, str):
            return SUIT_ORDER[self.suit] < SUIT_ORDER[other]
        return SUIT_ORDER[self.suit] < SUIT_ORDER[other.suit]

    def __le__(self, other):
        if isinstance(other, str):
            return SUIT_ORDER[self.suit] <= SUIT_ORDER[other]
        return SUIT_ORDER[self.suit] <= SUIT_ORDER[other.suit]

    def __eq__(self, other):
        if isinstance(other, str):
            return SUIT_ORDER[self.suit] == SUIT_ORDER[other]
        return SUIT_ORDER[self.suit] == SUIT_ORDER[other.suit]

    def __ne__(self, other):
        if isinstance(other, str):
            return SUIT_ORDER[self.suit] != SUIT_ORDER[other]
        return SUIT_ORDER[self.suit] != SUIT_ORDER[other.suit]

    def __gt__(self, other):
        if isinstance(other, str):
            return SUIT_ORDER[self.suit] > SUIT_ORDER[other]
        return SUIT_ORDER[self.suit] > SUIT_ORDER[other.suit]

    def __ge__(self, other):
        if isinstance(other, str):
            return SUIT_ORDER[self.suit] >= SUIT_ORDER[other]
        return SUIT_ORDER[self.suit] >= SUIT_ORDER[other.suit]

    def __repr__(self):
        return str(self.suit)
