from games.base import ConsumerUpdater, GameConsumer


class SlotsUpdater(ConsumerUpdater):
    # Updater for craps

    FUNCTION_MAP = {}


class SlotsConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = NotImplemented
        self.updater = SlotsUpdater

    def connect(self):
        super(SlotsConsumer, self).connect()

        # Called when connecting to web socket

    def disconnect(self, code):
        super(SlotsConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
