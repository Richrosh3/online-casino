from random import shuffle

from utils.PlayingCards.card import Card
from utils.PlayingCards.deck import Deck


class BlackjackCard(Card):
    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        self.value = self.get_value()

    def get_value(self):
        if type(self.rank.rank) is int:
            return self.rank.rank
        elif self.rank in ('J', 'Q', 'K'):
            return 10
        else:
            return 11


class BlackjackHand:
    def __init__(self):
        self.hand = []
        self.outcome = None

    def hit(self, new_card):
        self.hand.append(new_card)
        if self.value() > 21:
            return True

        if self.value() == 21:
            return True

        return False

    def value(self) -> int:
        total, aces = 0, 0
        for card in self.hand:
            if card.rank != 'A':
                total += card.value
            else:
                total += 11
                aces += 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def calculate_outcome(self, dealer):
        if self.value() > 21:
            self.outcome = 'Player Bust'
        elif self.value() == 21 and len(self.hand) == 2:
            self.outcome = 'Blackjack'
        elif dealer.value() > 21:
            self.outcome = 'Dealer Bust'
        elif self.value() > dealer.value():
            self.outcome = 'Win'
        elif self.value() == dealer.value():
            self.outcome = 'Push'
        else:
            self.outcome = 'Loss'

    def to_list(self):
        return [str(card) for card in self.hand]

    def __repr__(self) -> str:
        return str(self.hand.__str__()) + " " + str(self.value())


class Dealer(BlackjackHand):
    def __init__(self, pack):
        super(Dealer, self).__init__()
        self.pack = pack

    def play_hand(self):
        while self.value() <= 16:
            self.hand.append(self.pack.deal())


class Pack(Deck):
    def __init__(self, num_decks=2, shuffle_pct=.75, card_class=Card):
        self.num_decks = num_decks
        super().__init__(card_class)
        self.shuffle_card = int(len(self.deck) * (1 - shuffle_pct))

    def build(self):
        self.deck = []
        for _ in range(self.num_decks):
            self.deck += Deck(card_class=BlackjackCard).deck

    def shuffle(self):
        self.build()
        shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

    def check_reshuffle(self):
        if len(self.deck) < self.shuffle_card:
            self.shuffle()
