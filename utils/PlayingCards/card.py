from .rank import Rank
from .suit import Suit


class Card:
    SUITS = ('S', 'H', 'D', 'C')
    RANKS = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')

    def __init__(self, suit, rank):
        self.suit = Suit(suit)
        self.rank = Rank(rank)

    def __lt__(self, other):
        return self.suit < other.suit if self.rank == other.rank else self.rank < other.rank

    def __le__(self, other):
        return self.suit <= other.suit if self.rank == other.rank else self.rank <= other.rank

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit

    def __gt__(self, other):
        return self.suit > other.suit if self.rank == other.rank else self.rank > other.rank

    def __ge__(self, other):
        return self.suit >= other.suit if self.rank == other.rank else self.rank >= other.rank

    def __repr__(self):
        return '{}{}'.format(self.rank, self.suit)

    def __str__(self):
        return '{}{}'.format(self.rank, self.suit)
