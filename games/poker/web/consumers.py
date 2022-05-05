import json
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.poker.web.views import POKER_MANAGER


class PokerUpdater(ConsumerUpdater):
    # Updater for poker
    @staticmethod
    def load_game(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))

        return {'type': 'load_game', 'data': game_instance.dict_representation(request_data['user'])}

    @staticmethod
    def ready_up(request_data: dict) -> dict:
        """
        Changes a player's ready status
        Args:
            request_data: the request dictionary

        Returns:
            the full dictionary representation of the game
        """
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))
        is_ready = bool(int(request_data['data']['ready']))
        game_instance.ready_up(request_data['user'], is_ready)

        return {'group_send': True, 'message_function': 'individual_game_load'}

    @staticmethod
    def place_action(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))

        game_instance.round.player_action(request_data['user'], request_data['data']['action'],
                                          float(request_data['data']['amount']))

        return {'group_send': True, 'message_function': 'individual_game_load'}

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_action': place_action.__func__,
                    'ready_up': ready_up.__func__}


class PokerConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = POKER_MANAGER
        self.updater = PokerUpdater

    def connect(self):
        super(PokerConsumer, self).connect()

        async_to_sync(self.channel_layer.group_send)(
            self.session_id,
            {
                'type': 'individual_game_load',
            }
        )

    def disconnect(self, code):
        super(PokerConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'individual_game_load',
                }
            )

    def individual_game_load(self, event: dict):
        message = PokerUpdater.load_game({'session_id': self.session_id, 'user': self.user})
        message['user'] = self.user.username
        self.send(text_data=json.dumps(message))
