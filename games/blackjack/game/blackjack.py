from uuid import UUID

from accounts.models import CustomUser
from games.base import Game
from games.blackjack.game.utils import Pack, BlackjackCard, BlackjackHand, Dealer


class Blackjack(Game):
    """
    Game class that handles all the functions for blackjack
    """

    def __init__(self, session_id: UUID):
        super().__init__(session_id)

        self.round = None
        self.waiting_room = set()
        self.pack = Pack(card_class=BlackjackCard)
        self.bets = {player: 0 for player in self.players}
        self.players_ready = {player: False for player in self.players}

    def add_players_from_waiting_room(self) -> None:
        """
        Adds players from the waiting room to the game
        """
        for player in self.waiting_room:
            self.players.add(player)
        self.waiting_room = set()

    def all_ready(self) -> bool:
        """
        Returns:
            True if all players are ready, otherwise false
        """
        return all(self.players_ready.values())

    def record_bet(self, player: CustomUser, amount: float) -> None:
        """
        Records a bet for a player

        Args:
            player: user who is placing the bet
            amount: the bet amount
        """
        self.bets[player] = amount

    def ready_up(self, player: CustomUser, ready_state: bool) -> bool:
        """
        Changes a players ready state
        Args:
            player: player to change
            ready_state: if the player is ready

        Returns:
            True if all players are ready and game has moved to next stage; False otherwise
        """
        self.players_ready[player] = ready_state
        return self.check_update_game_stage()

    def get_stage(self) -> str:
        """
        Returns:
            The current stage of the game
        """
        return 'betting' if self.round is None else self.round.get_stage()

    def reset(self) -> None:
        """
        Resets and re-initializes the game
        """
        self.round = None
        self.add_players_from_waiting_room()

        for player in self.players:
            self.bets[player] = 0
            self.players_ready[player] = False

    def start_round(self) -> None:
        """
        Starts a blackjack round
        """
        for player in self.players:
            self.players_ready[player] = False

        self.round = BlackjackRound(self.pack, self)

    def record_bets(self) -> None:
        """
        Updates all players balances who places a bet
        """
        for player in self.bets.keys():
            player.update_balance(-1 * self.bets[player])

    def remove_player(self, player: CustomUser) -> None:
        """
        Removes a player from the blackjack game
        Args:
            player: player to be removed from the game
        """
        if player in self.players:
            self.players.remove(player)
            self.players_ready.pop(player)
            self.bets.pop(player)
            if self.round is not None:
                self.round.remove_player(player)

            if len(self.players) == 0:
                self.reset()
            else:
                self.check_update_game_stage()

        if player in self.waiting_room:
            self.waiting_room.remove(player)

    def check_update_game_stage(self) -> bool:
        """
        Checks if all players are ready, and moves the game to the next stage if they are
        Returns:
            True if all players were ready and the game was moved to the next stage. False otherwise
        """
        all_players_ready = self.all_ready()
        if all_players_ready:
            if self.get_stage() == 'ending':
                self.reset()
            else:
                self.record_bets()
                self.start_round()
        return all_players_ready

    def add_player(self, player: CustomUser) -> None:
        """
        Adds a player to the blackjack game
        Args:
            player: player to be added to the game
        """
        if self.get_stage() == 'betting':
            if player not in self.players:
                self.players.add(player)
                self.bets[player] = 0
                self.players_ready[player] = False
        else:
            self.waiting_room.add(player)

    def dict_representation(self):
        """
        Returns:
            A dictionary representation of the blackjack game
        """
        round_dict = self.round.dict_representation() if self.round is not None else {}
        return {'stage': self.get_stage(),
                'players': [{'player': player.username,
                             'bet': str(self.bets[player]),
                             'ready': self.players_ready[player]} for player in self.players]
                } | round_dict

    def __len__(self) -> int:
        """
        Returns:
            the number of players in the game and in the waiting room
        """
        return len(self.players) + len(self.waiting_room)


class BlackjackRound:
    """
    Class for a round of a blackjack game
    """

    def __init__(self, pack: Pack, game_instance: Blackjack):
        self.game_instance = game_instance
        self.hands = {player: BlackjackHand() for player in game_instance.players}
        self.round_over = False
        self.pack = pack
        self.dealer = Dealer(pack)
        self.initialize_hand()

    def initialize_hand(self) -> None:
        """
        Deals out two cards for all players and the dealer
        """
        for _ in range(2):
            for hand in list(self.hands.values()) + [self.dealer]:
                hand.hand.append(self.pack.deal())
        self.check_for_blackjack()

    def check_for_blackjack(self) -> None:
        """
        Checks to see if any player has a blackjack and makes any player that has blackjack ready
        """
        for player in self.game_instance.players:
            if self.hands[player].value() == 21:
                self.game_instance.players_ready[player] = True
                self.check_dealers_turn()

    def check_dealers_turn(self) -> None:
        """
        Checks if it is the dealers turn to play
        """
        if self.get_stage() == 'dealing' and all(self.game_instance.players_ready.values()):
            for player in self.game_instance.players_ready:
                self.game_instance.players_ready[player] = False

            self.play_dealer()

    def make_player_ready(self, player: CustomUser) -> None:
        """
        Changes a players ready state to True
        Args:
            player: player to ready up
        """
        self.game_instance.players_ready[player] = True
        self.check_dealers_turn()

    def update_game(self, player: CustomUser, action: str) -> None:
        """
        Updates the game based on a users actions
        Args:
            player: player that is updating the game
            action: action that the player has chosen
        """
        if action == 'hit':
            if self.hands[player].hit(self.pack.deal()):
                self.make_player_ready(player)

        elif action == 'stay':
            self.make_player_ready(player)

    def remove_player(self, player: CustomUser) -> None:
        """
        Removes a player from a round
        Args:
            player: player to be removed
        """
        self.hands.pop(player)
        self.check_dealers_turn()

    def play_dealer(self) -> None:
        """
        Plays the dealers part of blackjack
        """
        self.dealer.play_hand()
        for player, hand in self.hands.items():
            hand.calculate_outcome(self.dealer)
            self.payout_hand(player, hand)
        self.pack.check_reshuffle()
        self.round_over = True

    def payout_hand(self, player: CustomUser, hand: BlackjackHand) -> None:
        """
        Pays a player based on the outcome of their hand and how much they bet
        Args:
            player: player to pay out to
            hand: the players hand
        """
        if hand.outcome == 'Blackjack':
            player.update_balance(2.5 * self.game_instance.bets[player])
        elif hand.outcome == 'Win' or hand.outcome == 'Dealer Bust':
            player.update_balance(2 * self.game_instance.bets[player])
        elif hand.outcome == 'Push':
            player.update_balance(self.game_instance.bets[player])

    def get_stage(self) -> str:
        """
        Returns:
            the stage of the game
        """
        return 'ending' if self.round_over else 'dealing'

    def dict_representation(self):
        """
        Returns:
            a dictionary representation of the game
        """
        return {'hands': [{'player': player.username,
                           'hand': self.hands[player].to_list(),
                           'value': self.hands[player].value(),
                           'outcome': self.hands[player].outcome,
                           'ready': self.game_instance.players_ready[player]}
                          for player in self.game_instance.players],
                'dealer': {'hand': self.dealer.to_list() if self.round_over else [str(self.dealer.hand[0]), '2B'],
                           'value': self.dealer.value() if self.round_over else self.dealer.hand[0].value
                           }
                }
