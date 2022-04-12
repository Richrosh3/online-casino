from games.base import ConsumerUpdater, GameConsumer


class CrapsUpdater(ConsumerUpdater):
    # Updater for craps

    FUNCTION_MAP = {}


class CrapsConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = NotImplemented
        self.updater = CrapsUpdater

    def connect(self):
        super(CrapsConsumer, self).connect()

        # Called when connecting to web socket

    def disconnect(self, code):
        super(CrapsConsumer, self).disconnect(code)

        # Called when disconnecting from web socket