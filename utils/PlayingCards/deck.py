from random import shuffle

from utils.PlayingCards.card import Card


class Deck:
    def __init__(self, card_class=Card):
        self.card_class = card_class
        self.deck = []
        self.build()
        self.shuffle()

    def shuffle(self):
        shuffle(self.deck)

    def build(self):
        self.deck = []
        for suit in self.card_class.SUITS:
            for rank in self.card_class.RANKS:
                self.deck.append(self.card_class(suit, rank))

    def __len__(self):
        return len(self.deck)
