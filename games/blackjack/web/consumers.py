from games.base import ConsumerUpdater, GameConsumer


class BlackjackUpdater(ConsumerUpdater):
    FUNCTION_MAP = {}


class BlackjackConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.game_manager = BLACKJACK_MANAGER
        self.updater = BlackjackUpdater

    def connect(self):
        super(BlackjackConsumer, self).connect()

    def disconnect(self, code):
        super(BlackjackConsumer, self).disconnect(code)
