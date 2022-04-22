from decimal import Decimal
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.blackjack.web.views import BLACKJACK_MANAGER


class BlackjackUpdater(ConsumerUpdater):
    @staticmethod
    def load_game(request_data):
        game_instance = BLACKJACK_MANAGER.get(UUID(request_data['session_id']))

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def place_bet(request_data):
        bet = request_data['data']['bet']
        game_instance = BLACKJACK_MANAGER.get(UUID(request_data['session_id']))

        game_instance.bets[request_data['user']] = Decimal(bet)
        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready'}
                }

    @staticmethod
    def ready_up(request_data):
        game_instance = BLACKJACK_MANAGER.get(UUID(request_data['session_id']))
        is_ready = bool(int(request_data['data']['ready']))
        all_players_ready = game_instance.ready_up(request_data['user'], is_ready)
        if all_players_ready:
            return BlackjackUpdater.load_game(request_data)
        else:
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'ready'}
                    }

    @staticmethod
    def make_move(request_data):
        game_instance = BLACKJACK_MANAGER.get(UUID(request_data['session_id']))
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

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_bet': place_bet.__func__, 'ready_up': ready_up.__func__,
                    'action': make_move.__func__, 'request_user_balance': request_user_balance.__func__}


class BlackjackConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = BLACKJACK_MANAGER
        self.updater = BlackjackUpdater

    def connect(self):
        super(BlackjackConsumer, self).connect()

        game_dict = BlackjackUpdater.load_game({'session_id': self.session_id})
        game_dict['user'] = self.user.username

        async_to_sync(self.channel_layer.group_send)(
            self.session_id,
            {
                'type': 'send_message',
                'data': game_dict
            }
        )

    def disconnect(self, code):
        super(BlackjackConsumer, self).disconnect(code)
        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': BlackjackUpdater.load_game({'session_id': self.session_id})
                }
            )
