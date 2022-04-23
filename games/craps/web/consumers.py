from decimal import Decimal
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.craps.game.craps import CrapsGame
from games.craps.web.views import CRAPS_MANAGER

import logging


class CrapsUpdater(ConsumerUpdater):
    # Updater for craps
    @staticmethod
    def load_game(request_data: dict) -> dict:
        logging.debug("CALLED: load_game() in CrapsUpdater in consumers.py")
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def ready_up(request_data: dict) -> dict:
        logging.debug("CALLED: ready_up() in CrapsUpdater in consumers.py")
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
    def place_bet1(request_data: dict) -> dict:
        print("CALLED: place_bet1() in CrapsUpdater in consumers.py")
        print(request_data)
        pass_bet = request_data['data']['pass_bet']
        dont_pass_bet = request_data['data']['dont_pass_bet']
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        game_instance.bets[request_data['user']]['pass_bet'] = Decimal(pass_bet)
        game_instance.bets[request_data['user']]['dont_pass_bet'] = Decimal(dont_pass_bet)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_bet1': place_bet1.__func__, 'ready_up': ready_up.__func__,}


class CrapsConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = CRAPS_MANAGER
        self.updater = CrapsUpdater

        logging.debug("CREATED: CrapsConsumer object")

    def connect(self):
        logging.debug("CALLED: connect() in CrapsConsumer in consumers.py")
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
        logging.debug("CALLED: disconnect() in CrapsConsumer in consumers.py")
        super(CrapsConsumer, self).disconnect(code)

        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': CrapsUpdater.load_game({'session_id': self.session_id})
                }
            )
