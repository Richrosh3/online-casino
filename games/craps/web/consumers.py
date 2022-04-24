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
        print("CALLED: load_game() in CrapsUpdater in consumers.py")

        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        # The following block of code handles the situation when we're entering a phase of the game where the display
        # differs depending on whether you're the shooter or not.
        # If that information is relevant, then send it along with the game representation.
        if 'user' in request_data:
            if request_data['user'] == game_instance.shooter:
                return {'type': 'load_game',
                        'group_send': False,
                        'data': game_instance.dict_representation() | {'shooter': True}
                        }
            else:
                return {'type': 'load_game',
                        'group_send': False,
                        'data': game_instance.dict_representation() | {'shooter': False}
                        }

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def ready_up(request_data: dict) -> dict:
        print("CALLED: ready_up() in CrapsUpdater in consumers.py")

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
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    @staticmethod
    def place_bet1(request_data: dict) -> dict:
        print("CALLED: place_bet1() in CrapsUpdater in consumers.py")

        pass_bet = request_data['data']['pass_bet']
        dont_pass_bet = request_data['data']['dont_pass_bet']
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        # update_bets() will remove the amounts from the user's account
        game_instance.update_pass_bets(request_data['user'], pass_bet, dont_pass_bet)

        # this part actually changes the value of the bets in the game instance. the money is removed first, above
        game_instance.bets[request_data['user']]['pass_bet'] = Decimal(pass_bet)
        game_instance.bets[request_data['user']]['dont_pass_bet'] = Decimal(dont_pass_bet)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    @staticmethod
    def place_bet2(request_data: dict) -> dict:
        print("CALLED: place_bet2() in CrapsUpdater in consumers.py")

        come_bet = request_data['data']['come_bet']
        dont_come_bet = request_data['data']['dont_come_bet']
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        # update_bets() will remove the amounts from the user's account
        game_instance.update_come_bets(request_data['user'], come_bet, dont_come_bet)

        # this part actually changes the value of the bets in the game instance. the money is removed first, above
        game_instance.bets[request_data['user']]['come_bet'] = Decimal(come_bet)
        game_instance.bets[request_data['user']]['dont_come_bet'] = Decimal(dont_come_bet)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    @staticmethod
    def come_out_roll(request_data: dict) -> dict:
        print("CALLED: come_out_roll() in CrapsUpdater in consumers.py")
        print(request_data)

        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        rolled_val = game_instance.round.update_game("come_out")

        if game_instance.round.round_over:
            game_instance.calculate_payouts()
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'game_over',
                                                                   'value': str(rolled_val)
                                                                   }
                    }
        else:
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'come_out_done'}}

    @staticmethod
    def ready2(request_data: dict) -> dict:
        print("CALLED: ready2() in CrapsUpdater in consumers.py")

        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        is_ready = bool(int(request_data['data']['ready']))
        game_instance.ready_up(request_data['user'], is_ready)

        if game_instance.all_ready():
            game_instance.round.stage = 'point'
            return CrapsUpdater.load_game(request_data)

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    @staticmethod
    def point_roll(request_data: dict) -> dict:
        print("CALLED: point_roll() in CrapsUpdater in consumers.py")
        print(request_data)

        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        rolled_val = game_instance.round.update_game("point")

        if game_instance.round.round_over:
            game_instance.calculate_payouts()
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'game_over',
                                                                   'value': str(rolled_val)
                                                                   }
                    }
        else:
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'point_reroll',
                                                                   'value': str(rolled_val)
                                                                   }
                    }

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_bet1': place_bet1.__func__, 'ready_up': ready_up.__func__,
                    'come_out_roll': come_out_roll.__func__, 'place_bet2': place_bet2.__func__,
                    'ready2': ready2.__func__, 'point_roll': point_roll.__func__}


class CrapsConsumer(GameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = CRAPS_MANAGER
        self.updater = CrapsUpdater

        print("CREATED: CrapsConsumer object")

    def connect(self):
        print("CALLED: connect() in CrapsConsumer in consumers.py")

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
        print("CALLED: disconnect() in CrapsConsumer in consumers.py")

        super(CrapsConsumer, self).disconnect(code)

        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': CrapsUpdater.load_game({'session_id': self.session_id})
                }
            )
