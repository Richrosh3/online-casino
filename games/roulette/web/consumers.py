from games.base import ConsumerUpdater, GameConsumer, SessionManager


class RouletteUpdater(ConsumerUpdater):
    # Updater for roulette

    @staticmethod
    def place_bet(request_data: dict):
        raise NotImplementedError
    FUNCTION_MAP = {}

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
