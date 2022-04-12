from games.base import ConsumerUpdater, GameConsumer


class PokerUpdater(ConsumerUpdater):
    # Updater for poker

    FUNCTION_MAP = {}


class PokerConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = NotImplemented
        self.updater = PokerUpdater

    def connect(self):
        super(PokerConsumer, self).connect()

        # Called when connecting to web socket

    def disconnect(self, code):
        super(PokerConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
