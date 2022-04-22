from uuid import UUID

from games.base import ConsumerUpdater, GameConsumer
from games.roulette.web.views import ROULETTE_MANAGER


class RouletteUpdater(ConsumerUpdater):
    # Updater for roulette

    @staticmethod
    def place_bet(request_data: dict):
        game_instance = ROULETTE_MANAGER.get(UUID(request_data['session_id']))
        bet = request_data['data']['bet']
        amount = request_data['data']['amount']

        game_instance.record_bet(request_data['user'], amount, bet)
    FUNCTION_MAP = {'place_bet': place_bet.__func__}


class RouletteConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = NotImplemented
        self.updater = RouletteUpdater

    def connect(self):
        super(RouletteConsumer, self).connect()

        # Called when connecting to web socket


    def disconnect(self, code):
        super(RouletteConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
