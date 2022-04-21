from decimal import Decimal
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.craps.game.craps import CrapsGame
from games.craps.web.views import CRAPS_MANAGER


class CrapsUpdater(ConsumerUpdater):
    # Updater for craps
    @staticmethod
    def load_game(request_data: dict) -> dict:
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def ready_up(request_data: dict) -> dict:
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        is_ready = bool(int(request_data['data']['ready']))
        game_instance.ready_up(request_data['user'], is_ready)

        if game_instance.all_ready():
            if request_data['data']['reset']:
                game_instance.reset()
            else:
                game_instance.start_round()
            return CrapsUpdater.load_game(request_data)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready'}
                }

    @staticmethod
    def place_bet(request_data: dict) -> dict:
        bet_amount = request_data['data']['bet_amount']
        bet_type = request_data['data']['bet_type']
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        if CrapsGame.bet_type_valid(bet_type):
            game_instance.bets[request_data['user']][bet_type] = Decimal(bet_amount)

            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'ready'}
                    }

    @staticmethod
    def roll_dice(request_data: dict) -> dict:
        pass

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_bet': place_bet.__func__, 'ready_up': ready_up.__func__,
                    'roll': roll_dice.__func__}


class CrapsConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = CRAPS_MANAGER
        self.updater = CrapsUpdater

    def connect(self):
        super(CrapsConsumer, self).connect()

        game_dict = CrapsUpdater.load_game({'session_id': self.session_id})
        game_dict['user'] = self.user.username

        async_to_sync(self.channel_layer.group_send)(
            self.session_id,
            {
                'type': 'send_message',
                'data': game_dict
            }
        )

    def disconnect(self, code):
        super(CrapsConsumer, self).disconnect(code)

        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': CrapsUpdater.load_game({'session_id': self.session_id})
                }
            )
