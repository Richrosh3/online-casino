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
    def start_round(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))
        game_instance.reset_board()
        game_instance.deal_cards()

        return {'group_send': True}

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

        return {'group_send': True}

    @staticmethod
    def place_action(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))

        game_instance.round.player_action(request_data['user'], request_data['data']['action'],
                                          float(request_data['data']['amount']))

        return {'group_send': True}

    FUNCTION_MAP = {'load_game': load_game.__func__, 'start_round': start_round.__func__,
                    'place_action': place_action.__func__, 'ready_up': ready_up.__func__}


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

    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        """
        Called when the web socket receives a message from the user

        Args:
            text_data: received string message
            bytes_data: received bytes message
        """
        request_json = json.loads(text_data)
        request_json['user'] = self.user
        request_json['session_id'] = self.session_id

        update_json = self.updater.function_router(request_json)

        if update_json is not None and isinstance(update_json, dict):
            if update_json.get('group_send', True) is False:
                self.send(text_data=json.dumps(update_json))
            else:
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
