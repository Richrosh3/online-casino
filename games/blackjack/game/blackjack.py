from games.base import Game
from games.blackjack.game.round import Round
from games.blackjack.game.utils import Pack, BlackjackCard


class Blackjack(Game):
    def __init__(self, session_id):
        super().__init__(session_id)

        self.round = None
        self.waiting_room = set()
        self.pack = Pack(card_class=BlackjackCard)
        self.bets = {player: 0 for player in self.players}
        self.players_ready = {player: False for player in self.players}

    def add_players_from_waiting_room(self):
        for player in self.waiting_room:
            self.players.add(player)
        self.waiting_room = set()

    def all_ready(self):
        return all(self.players_ready.values())

    def record_bet(self, player, amount):
        self.bets[player] = amount

    def ready_up(self, player, ready_state):
        self.players_ready[player] = ready_state
        return self.check_update_game_stage()

    def get_stage(self):
        return 'betting' if self.round is None else self.round.get_stage()

    def reset(self):
        self.round = None
        self.add_players_from_waiting_room()

        for player in self.players:
            self.bets[player] = 0
            self.players_ready[player] = False

    def start_round(self):
        for player in self.players:
            self.players_ready[player] = False

        self.round = Round(self.pack, self)

    def record_bets(self):
        for player in self.bets.keys():
            player.update_balance(-1 * self.bets[player])

    def remove_player(self, player):
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

    def check_update_game_stage(self):
        all_players_ready = self.all_ready()
        if all_players_ready:
            if self.get_stage() == 'ending':
                self.reset()
            else:
                self.record_bets()
                self.start_round()
        return all_players_ready

    def add_player(self, player):
        if self.get_stage() == 'betting':
            if player not in self.players:
                self.players.add(player)
                self.bets[player] = 0
                self.players_ready[player] = False
        else:
            self.waiting_room.add(player)

    def dict_representation(self):
        round_dict = self.round.dict_representation(self.players) if self.round is not None else {}
        return {'stage': self.get_stage(),
                'players': [{'player': player.username,
                             'bet': str(self.bets[player]),
                             'ready': self.players_ready[player]} for player in self.players]
                } | round_dict

    def __len__(self):
        return len(self.players) + len(self.waiting_room)
