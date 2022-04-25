from utils.PlayingCards.card import Card


class PokerCard(Card):
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    def __init__(self, val, suit):
        super(PokerCard, self).__init__(val, suit)
        self.val = self.get_value()

    def get_value(self):
        if type(self.rank.rank) is int:
            return self.rank.rank
        elif self.rank == 'J':
            return 11
        elif self.rank == 'Q':
            return 12
        elif self.rank == 'K':
            return 13
        else:
            return 14

    def __eq__(self, other):
        return self.val == other.val and self.suit == other.suit

    def __ne__(self, other):
        return self.val != other.val or self.suit != other.suit
