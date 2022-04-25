from decimal import Decimal
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.slots.web.views import SLOTS_MANAGER


class SlotsUpdater(ConsumerUpdater):
    @staticmethod
    def load_game(request_data):
        game_instance = SLOTS_MANAGER.get(UUID(request_data['session_id']))

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def place_bet(request_data):
        bet = request_data['data']['bet']
        game_instance = SLOTS_MANAGER.get(UUID(request_data['session_id']))

        game_instance.bet = bet
        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready'}
                }

    @staticmethod
    def play_slots(request_data):
        game_instance = SLOTS_MANAGER.get(UUID(request_data['session_id']))
        game_instance.record_bet(request_data['user'])
        return game_instance.play_slots()

    @staticmethod
    def make_move(request_data):
        game_instance = SLOTS_MANAGER.get(UUID(request_data['session_id']))
        move = request_data['data']['move']

        game_instance.round.update_game(request_data['user'], move)

        return {'type': 'load_game',
                'data': game_instance.dict_representation()
                }

    @staticmethod
    def request_user_balance(request_data):
        request_data['user'].refresh_from_db()
        return {'type': 'update',
                'group_send': False,
                'data': {'to_update': 'balance',
                         'balance': str(request_data['user'].current_balance)}
                }

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_bet': place_bet.__func__, 'play_slots': play_slots.__func__,
                    'action': make_move.__func__, 'request_user_balance': request_user_balance.__func__}


class SlotsConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = SLOTS_MANAGER
        self.updater = SlotsUpdater

    def connect(self):
        super(SlotsConsumer, self).connect()

        game_dict = SlotsUpdater.load_game({'session_id': self.session_id})
        game_dict['user'] = self.user.username

        async_to_sync(self.channel_layer.group_send)(
            self.session_id,
            {
                'type': 'send_message',
                'data': game_dict
            }
        )

    def disconnect(self, code):
        super(SlotsConsumer, self).disconnect(code)

        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': SlotsUpdater.load_game({'session_id': self.session_id})
                }
            )
