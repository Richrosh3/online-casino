import json
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.craps.web.views import CRAPS_MANAGER


class CrapsUpdater(ConsumerUpdater):
    """
    CrapsUpdater is an extension of the ConsumerUpdater class, handling the game Craps.

    Requests come in from listeners.js, are processed in CrapsUpdater, with the results being sent to craps.js (the
    exception is update balance requests, which come from craps.js and are sent back to that file).
    """

    @staticmethod
    def load_game(request_data: dict) -> dict:
        """
        load_game() is responsible for transitioning to and from different phases of the Craps game. This function
        contains the logic necessary to create the proper message for craps.js that will display the desired elements in
        the craps.html page.

        This function is responsible for deciding whether a message needs to be sent to all players or just one. When a
        player readies up on a betting screen, they are sent to a waiting screen for the next phase. When all players
        are ready, then the waiting screen needs to be replaced with the appropriate role -- one player will be the
        shooter, and the rest are not. As such, this function will check if all players are ready and create a message
        such that everyone's waiting screen is updated appropriately.

        :param request_data:    A dictionary containing request data, such as session id's and usernames.

        :return:                A dictionary containing a message to be sent to craps.js, including the message type
                                'load_game' and the necessary data.
        """
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        to_all = False
        if game_instance.all_ready():
            to_all = True
            game_instance.unready_all()

        # The following block of code handles the situation when we're entering a phase of the game where the display
        # differs depending on whether you're the shooter or not.
        # If that information is relevant, then send it along with the game representation.
        if 'user' in request_data and game_instance.round is not None:
            if request_data['user'] == game_instance.shooter:
                return {'type': 'load_game',
                        'group_send': False,
                        'data': game_instance.dict_representation() | {'shooter': True, 'to_all': to_all}
                        }
            else:
                return {'type': 'load_game',
                        'group_send': False,
                        'data': game_instance.dict_representation() | {'shooter': False, 'to_all': to_all}
                        }

        return {'type': 'load_game',
                'data': game_instance.dict_representation()}

    @staticmethod
    def ready1(request_data: dict) -> dict:
        """
        Function that handles the result of hitting the ready button during the first phase of betting. When players
        ready up during the first phase of betting, they are sent to a waiting area until all other players are ready.
        More details are in the docstring for the load_game() function. This function will return the result of the
        load_game() function.

        :param request_data:    A dictionary containing request data such as session id's and usernames.

        :return:                The result of load_game() with the given request, which will result in players being
                                taken to the next phase of the game.
        """
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        is_ready = bool(int(request_data['data']['ready']))
        game_instance.ready_up(request_data['user'], is_ready)

        if game_instance.round is None:
            game_instance.start_round()

        return CrapsUpdater.load_game(request_data)

    @staticmethod
    def ready2(request_data: dict) -> dict:
        """
        Function that handles the result of hitting the ready button during the second phase of betting. When players
        ready up during the second phase of betting, they are sent to a waiting area until all other players are ready.
        More details are in the docstring for the load_game() function. This function will return the result of the
        load_game() function.

        :param request_data:    A dictionary containing request data such as session id's and usernames.

        :return:                The result of load_game() with the given request, which will result in players being
                                taken to the next phase of the game.
        """
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        is_ready = bool(int(request_data['data']['ready']))
        game_instance.ready_up(request_data['user'], is_ready)

        game_instance.round.stage = 'point'
        return CrapsUpdater.load_game(request_data)

    @staticmethod
    def ready_restart(request_data: dict) -> dict:
        """
        Function for processing the ready button on the game over screen. When all players are readied up on this
        screen, the game is restarted. This is done by routing a request to the load_game() function.

        :param request_data:    A dictionary containing request data, such as session id's and usernames.

        :return:                If not all players are ready, a message is sent to craps.js which changes the ready
                                button to green. If all players are ready, then the game is restarted by routing the
                                request to load_game().
        """
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
        """
        place_bet1() processes bets made during the first phase of betting. The values are passed into and processed by
        the game instance.

        :param request_data:    A dictionary containing request data. In this case, it must contain 'pass_bet' and
                                'dont_pass_bet' values.

        :return:                A message to be passed to craps.js which will update the bet values on the player board.
        """
        pass_bet = request_data['data']['pass_bet']
        dont_pass_bet = request_data['data']['dont_pass_bet']
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        # update_bets() will remove the amounts from the user's account and add it to the internal bets dictionary
        game_instance.update_pass_bets(request_data['user'], float(pass_bet), float(dont_pass_bet))

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    @staticmethod
    def place_bet2(request_data: dict) -> dict:
        """
        place_bet2() processes bets made during the second phase of betting. The values are passed into and processed by
        the game instance.

        :param request_data:    A dictionary containing request data. In this case, it must contain 'come_bet' and
                                'dont_come_bet' values.

        :return:                A message to be passed to craps.js which will update the bet values on the player board.
        """
        come_bet = request_data['data']['come_bet']
        dont_come_bet = request_data['data']['dont_come_bet']
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))

        # update_bets() will remove the amounts from the user's account and add it to the internal bets dictionary
        game_instance.update_come_bets(request_data['user'], float(come_bet), float(dont_come_bet))

        return {'type': 'update',
                'data': game_instance.dict_representation() | {'to_update': 'ready_up'}
                }

    @staticmethod
    def come_out_roll(request_data: dict) -> dict:
        """
        Function for processing the requests made during the come out phase, the first phase of rolling dice. The game
        instance's CrapsRound object will handle the actual game logic. This function will check if the game has ended,
        in which case the payments are distributed and the game over screen is loaded. Otherwise, the next phase of
        betting will be entered.

        :param request_data:    A dictionary containing request data like session id's and usernames.

        :return:                If the game has ended as a result of the player's roll, a message is sent to craps.js
                                which will send players to the game over screen. Otherwise, the message will send
                                players to the next phase of betting.
        """
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        roll1, roll2 = game_instance.round.roll_dice("come_out")

        if game_instance.round.round_over:
            game_instance.calculate_payouts()
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'game_over',
                                                                   'value1': str(roll1),
                                                                   'value2': str(roll2)
                                                                   }
                    }
        else:
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'come_out_done',
                                                                   'value1': str(roll1),
                                                                   'value2': str(roll2)
                                                                   }
                    }

    @staticmethod
    def point_roll(request_data: dict) -> dict:
        """
        Function for processing the requests made during the point phase, the second phase of rolling dice. The game
        instance's CrapsRound object will handle the actual game logic. This function will check if the game has ended,
        in which case all players are made unready (since they need to ready up again to restart), payments are
        distributed, and the game over screen is loaded. Otherwise, the point phase will continue until it is over.

        :param request_data:    A dictionary containing request data like session id's and usernames.

        :return:                If the game has ended as a result of the player's roll, a message is sent to craps.js
                                which will send players to the game over screen. Otherwise, the message will update the
                                screen with the last roll and allow rolling to continue until the game is over.
        """
        game_instance = CRAPS_MANAGER.get(UUID(request_data['session_id']))
        roll1, roll2 = game_instance.round.roll_dice("point")

        if game_instance.round.round_over:
            game_instance.unready_all()
            game_instance.calculate_payouts()
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'game_over',
                                                                   'value1': str(roll1),
                                                                   'value2': str(roll2)
                                                                   }
                    }
        else:
            return {'type': 'update',
                    'data': game_instance.dict_representation() | {'to_update': 'point_reroll',
                                                                   'value1': str(roll1),
                                                                   'value2': str(roll2)
                                                                   }
                    }

    @staticmethod
    def user_balance(request_data: dict) -> dict:
        """
        :param request_data:    A dictionary containing request data like session id's and usernames.

        :return:                The given user's current account balance.
        """
        request_data['user'].refresh_from_db()

        return {'type': 'update',
                'group_send': False,
                'data': {'to_update': 'balance',
                         'to_all': False,
                         'balance': str(request_data['user'].current_balance)}
                }

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_bet1': place_bet1.__func__,
                    'ready_up': ready_restart.__func__, 'come_out_roll': come_out_roll.__func__,
                    'place_bet2': place_bet2.__func__, 'ready2': ready2.__func__, 'point_roll': point_roll.__func__,
                    'ready1': ready1.__func__, 'request_user_balance': user_balance.__func__}
    """
    The function map maps message types (as defined in listeners.js) to the actual function that needs to be called
    in order to process the input given from listeners.js
    """


class CrapsConsumer(GameConsumer):
    """
    CrapsConsumer is an extension of the GameConsumer class, handling the game Craps.

    Messages come from the CrapsUpdater and are sent to craps.js
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game_manager = CRAPS_MANAGER
        self.updater = CrapsUpdater

    def connect(self) -> None:
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

    def disconnect(self, code: int) -> None:
        super(CrapsConsumer, self).disconnect(code)

        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': CrapsUpdater.load_game({'session_id': self.session_id})
                }
            )

    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        """
        receive() is actually responsible for directing messages from the CrapsUpdater to the craps.js JavaScript file.
        There is a bet of special logic that made it necessary to override this function from the parent class.

        Essentially, the extra logic here is responsible for handling the rolling screen. When a player readies up on a
        betting screen, they're taken to the rolling screen, where a message is shown that they must wait for the other
        players. As such, the messages that send players to that screen are processed individually. This is what the
        'to_all' key that might be present in the message is for. However, when all players have readied, the last
        player to ready needs the individual message to take them to the waiting screen, but then a message for everyone
        must reveal the actual rolling interface. For the shooter, they will be able to roll. Non-shooters will be
        instructed to wait for the shooter. This complicated system necessitates some additional logic.

        :param text_data:   Received string message
        :param bytes_data:  Received bytes message
        """
        request_json = json.loads(text_data)
        request_json['user'] = self.user
        request_json['session_id'] = self.session_id

        if request_json.get('type', None) == 'chat_msg':
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'send_message',
                    'data': {
                        'type': 'chat_msg',
                        'data': {
                            'user': request_json['user'].username,
                            'msg': request_json['data']['msg']
                        }
                    }
                })
        else:
            update_json = self.updater.function_router(request_json)
            
            if update_json is not None:
                if update_json.get('group_send', True) is False:
                    old = update_json['data']['to_all']
                    update_json['data']['to_all'] = False
                    self.send(text_data=json.dumps(update_json))

                    update_json['data']['to_all'] = old

                    if 'to_all' in update_json['data'] and update_json['data']['to_all']:
                        async_to_sync(self.channel_layer.group_send)(
                            self.session_id,
                            {
                                'type': 'send_message',
                                'data': update_json
                            }
                        )
                else:
                    async_to_sync(self.channel_layer.group_send)(
                        self.session_id,
                        {
                            'type': 'send_message',
                            'data': update_json
                        }
                    )
