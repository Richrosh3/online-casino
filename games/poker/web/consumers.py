import json
from uuid import UUID

from asgiref.sync import async_to_sync

from games.base import ConsumerUpdater, GameConsumer
from games.poker.web.views import POKER_MANAGER


class PokerUpdater(ConsumerUpdater):
    """
    Updater class for poker game
    """

    @staticmethod
    def load_game(request_data: dict) -> dict:
        """
        Returns the full dictionary representation of the game to load the game in the front end

        Args:
            request_data: the request dictionary

        Returns:
            the full dictionary representation of the game
        """
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
    def place_action(request_data: dict) -> dict:
        """
        Places an action for a user

        Args:
            request_data: the request dictionary

        Returns:
            the full dictionary representation of the game for each user
        """
        game_instance = POKER_MANAGER.get(UUID(request_data['session_id']))

        game_instance.round.player_action(request_data['user'], request_data['data']['action'],
                                          float(request_data['data']['amount']))

        return {'group_send': True, 'message_function': 'individual_game_load'}

    FUNCTION_MAP = {'load_game': load_game.__func__, 'place_action': place_action.__func__,
                    'ready_up': ready_up.__func__}


class PokerConsumer(GameConsumer):
    """
    Web socket consumer for poker game
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_manager = POKER_MANAGER
        self.updater = PokerUpdater

    def connect(self):
        """
        Handles connecting a user to game channel and registering them for the session when a user connects to the web
        socket
        """
        super(PokerConsumer, self).connect()

        async_to_sync(self.channel_layer.group_send)(
            self.session_id,
            {
                'type': 'individual_game_load',
            }
        )

    def disconnect(self, code):
        """
        Handles removing a user from the game channel and removing them from the session when a player navigates away
        from the game web page

        Args:
           code: exit code
        """
        super(PokerConsumer, self).disconnect(code)

        # Called when disconnecting from web socket
        if not self.session_empty():
            async_to_sync(self.channel_layer.group_send)(
                self.session_id,
                {
                    'type': 'individual_game_load',
                }
            )

    def individual_game_load(self, event: dict) -> None:
        """
        Loads the game for each web socket connection

        Args:
            event: Event to send. Data must be under 'data' key

        """
        message = PokerUpdater.load_game({'session_id': self.session_id, 'user': self.user})
        message['user'] = self.user.username
        self.send(text_data=json.dumps(message))
