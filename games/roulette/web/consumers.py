from uuid import UUID

from games.base import ConsumerUpdater, GameConsumer
from games.roulette.web.views import ROULETTE_MANAGER


class RouletteUpdater(ConsumerUpdater):
    # Updater for roulette

    @staticmethod
    def place_bet(request_data: dict):
        game_instance = ROULETTE_MANAGER.get(UUID(request_data['session_id']))
        bet = request_data['data']['bet']
        amount = float(request_data['data']['amount'])

        is_valid = game_instance.record_bet(request_data['user'], amount, bet)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'valid_bet': is_valid}
                }

    @staticmethod
    def play(request_data: dict):
        game_instance = ROULETTE_MANAGER.get(UUID(request_data['session_id']))
        game_instance.start_round()

        return {'type': 'load_game',
                'data': game_instance.dict_representation()
                }
    FUNCTION_MAP = {'place_bet': place_bet.__func__, 'play': play.__func__}


class RouletteConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = ROULETTE_MANAGER
        self.updater = RouletteUpdater

    def connect(self):
        super(RouletteConsumer, self).connect()

        # Called when connecting to web socket


    def disconnect(self, code):
        super(RouletteConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
