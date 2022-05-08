from random import shuffle
from typing import Union

from utils.PlayingCards.card import Card
from utils.PlayingCards.deck import Deck


class BlackjackCard(Card):
    """
    Playing card class for a blackjack game
    """

    def __init__(self, suit: str, rank: Union[str, int]):
        super().__init__(suit, rank)
        self.value = self.get_value()

    def get_value(self) -> int:
        """
        Returns:
            The value of the card
        """
        if type(self.rank.rank) is int:
            return self.rank.rank
        elif self.rank in ('J', 'Q', 'K'):
            return 10
        else:
            return 11


class BlackjackHand:
    """
    Class for a player's hand of blackjack
    """

    def __init__(self):
        self.hand = []
        self.outcome = None

    def hit(self, new_card: BlackjackCard) -> bool:
        """
        Appends a new card to the players hand

        Args:
            new_card: new card to be added to the hand

        Returns:
            True if the hand's value is over 21. Otherwise False
        """
        self.hand.append(new_card)
        if self.value() >= 21:
            return True

        return False

    def value(self) -> int:
        """
        Returns:
            The integer value of the blackjack hand
        """
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

    def calculate_outcome(self, dealer) -> None:
        """
        Calculates the outcome of the hand

        Args:
            dealer: the dealer's hand to compare this hand to
        """
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

    def to_list(self) -> list:
        """
        Returns:
            a list containing the string representation of all the cords
        """
        return [str(card) for card in self.hand]

    def __repr__(self) -> str:
        """
        Returns:
            the string representation of the hand
        """
        return str(self.hand.__str__()) + " " + str(self.value())


class Pack(Deck):
    """
    Class for a pack of multiple Decks, like is used in blackjack
    """

    def __init__(self, num_decks: int = 2, shuffle_pct: float = .75, card_class=Card):
        self.num_decks = num_decks
        self.card_class = card_class
        super().__init__(card_class)
        self.shuffle_card = int(len(self.deck) * (1 - shuffle_pct))

    def build(self) -> None:
        """
        Builds the pack and fills it with cards
        """
        self.deck = []
        for _ in range(self.num_decks):
            self.deck += Deck(card_class=self.card_class).deck

    def shuffle(self) -> None:
        """
        Builds and shuffles a new pack
        """
        self.build()
        shuffle(self.deck)

    def deal(self) -> Card:
        """
        Deals a card

        Returns:
            The card dealt
        """
        return self.deck.pop(0)

    def check_reshuffle(self) -> None:
        """
        Checks if the deck needs to be reshuffled and reshuffles it if it does.
        """
        if len(self.deck) < self.shuffle_card:
            self.shuffle()


class Dealer(BlackjackHand):
    """
    Hand class for the blackjack dealer
    """

    def __init__(self, pack: Pack):
        super(Dealer, self).__init__()
        self.pack = pack

    def play_hand(self) -> None:
        """
        Plays the dealers hand and adds cards till the value is 17+
        """
        while self.value() <= 16:
            self.hand.append(self.pack.deal())
