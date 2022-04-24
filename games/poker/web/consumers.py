from decimal import Decimal
from uuid import UUID

from asgiref.sync import async_to_sync
from games.base import ConsumerUpdater, GameConsumer
from games.poker.web.views import POKER_MANAGER


class PokerUpdater(ConsumerUpdater):
    # Updater for poker
    @staticmethod
    def load_game(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def start_round(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))
        game_instance.reset_board()
        game_instance.deal_cards()

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'deal'}
                }

    @staticmethod
    def place_action(request_data):
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))
        request = {'player': request_data['user'], 'action': request_data['data']['action'],
                   'amount': float(request_data['data']['amount'])}

        game_instance.player_action(request)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'action'}
                }

    FUNCTION_MAP = {'load_game': load_game.__func__, 'start_round': start_round.__func__,
                    'place_action': place_action.__func__}


class PokerConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = POKER_MANAGER
        self.updater = PokerUpdater

    def connect(self):
        super(PokerConsumer, self).connect()
        game_dict = PokerUpdater.load_game({'session_id': self.session_id})
        game_dict['user'] = self.user.username

        # Called when connecting to web socket
        async_to_sync(self.channel_layer.group_send)(
            self.session_id,
            {
                'type': 'send_message',
                'data': game_dict
            }
        )

    def disconnect(self, code):
        super(PokerConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': PokerUpdater.load_game({'session_id': self.session_id})
                }
            )
