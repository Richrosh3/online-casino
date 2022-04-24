import json
from uuid import UUID, uuid4

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from accounts.models import CustomUser


class Game:
    """
    Interface for all OnlineCasino games

    - in_limbo is a set for players trying to join a game. This takes care of the issue that players would be removed
      from the session when reloading the page
    """

    def __init__(self, session_id: UUID) -> None:
        self.id = session_id
        self.players = set()
        self.in_limbo = set()

    def add_to_limbo(self, user: CustomUser) -> None:
        """
        Adds a player to the limbo set
        Args:
            user: the player to be added
        """
        self.in_limbo.add(user)

    def remove_from_limbo(self, user: CustomUser) -> None:
        """
        Removes a player from the limbo set if they are in it
        Args:
            user: the player to be removed
        """
        if user in self.in_limbo:
            self.in_limbo.remove(user)

    def add_player(self, player: CustomUser) -> None:
        """
        Adds a player to the game
        Args:
            player: player to be added
        """
        self.players.add(player)

    def remove_player(self, player: CustomUser):
        """
        Removes a player from the game of they are in it
        Args:
            player: player to be removed
        """
        if player in self.players:
            self.players.remove(player)

    def __len__(self) -> int:
        """
        Returns:
            How many players are in the game
        """
        return len(self.players)


class GameConsumer(WebsocketConsumer):
    """
    Base Consumer class for all game's web socket connections
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game_manager = None
        self.session_id = None
        self.user = None
        self.updater = ConsumerUpdater

    def session_empty(self) -> bool:
        """
        Returns:
            whether there are players connected to the websocket
        """
        return len(self.channel_layer.groups.get(self.session_id, {}).items()) == 0

    def connect(self) -> None:
        """
        Handles connecting a user to game channel and registering them for the session when a user connects to the web
        socket
        """
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            self.session_id,
            self.channel_name
        )
        if self.user in self.game_manager.get(UUID(self.session_id)).in_limbo:
            self.game_manager.get(UUID(self.session_id)).remove_from_limbo(self.user)
        self.game_manager.register_user(UUID(self.session_id), self.user)
        self.accept()

    def disconnect(self, code: int) -> None:
        """
        Handles removing a user from the game channel and removing them from the session when a player navigates away
        from the game web page

        Args:
            code: exit code
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.session_id,
            self.channel_name
        )

        if self.user not in self.game_manager.get(UUID(self.session_id)).in_limbo:
            if self.session_empty():
                self.game_manager.delete(UUID(self.session_id))
            else:
                self.game_manager.remove_user(UUID(self.session_id), self.user)

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

        print(update_json)

        if update_json is not None:
            if update_json.get('group_send', True) is False:
                print("Individual send")
                self.send(text_data=json.dumps(update_json))
            else:
                print("Group send")
                async_to_sync(self.channel_layer.group_send)(
                    self.session_id,
                    {
                        'type': 'send_message',
                        'data': update_json
                    }
                )

    def send_message(self, event: dict) -> None:
        """
        Sends a message to this web socket connection

        Args:
            event: Event to send. Data must be under 'data' key

        """
        message = event['data']
        message['user'] = self.user.username
        self.send(text_data=json.dumps(message))


class ConsumerUpdater:
    """
    Base class for a Game Updater
    """

    FUNCTION_MAP = None

    @classmethod
    def function_router(cls, text_json: dict) -> dict:
        """
        Routes the request to the correct function

        Args:
            text_json: Request dictionary. Key 'type' of request must exist in FUNCTION_MAP

        Returns:
            dictionary returned by called function
        """
        return cls.FUNCTION_MAP[text_json['type']](text_json)


class SessionManager:
    """
    Manager for all sessions of a game type
    """

    def __init__(self, game_class: type) -> None:
        self.sessions = dict()
        self.game_class = game_class

    def create(self) -> UUID:
        """
        Creates a new session

        Returns:
            UUID of the newly created session
        """
        session_id = uuid4()
        self.sessions[session_id] = self.game_class(session_id)
        return session_id

    def register_user(self, uuid: UUID, user: CustomUser) -> None:
        """
        Registers a user to a specified session

        Args:
            uuid: UUID of the session to register the user for
            user: User to add to the session
        """
        self.sessions[uuid].add_player(user)

    def remove_user(self, uuid: UUID, user: CustomUser) -> None:
        """
        Removes a user from a specified session

        Args:
            uuid: UUID of the session to remove the user from
            user: User to remove from the session
        """
        self.sessions[uuid].remove_player(user)

    def session_exists(self, uuid: UUID) -> bool:
        """
        Checks to see if the passed session exists
        Args:
            uuid: UUID of the session to check

        Returns:
            true if the session exists
        """
        return uuid in self.sessions.keys()

    def list_sessions(self) -> dict:
        """
        Returns a dictionary of each session and the number of players in that session
        Returns:
            dict of all sessions
        """
        return {str(key): len(self.sessions[key]) for key in self.sessions.keys()}

    def get(self, uuid: UUID) -> Game:
        """
        Returns the requested game
        Args:
            uuid: UUID of the requested game

        Returns:
            the requested game
        """
        return self.sessions.get(uuid)

    def delete(self, uuid: UUID) -> Game:
        """
        Deletes a game session
        Args:
            uuid: UUID of the game to delete

        Returns:
            the deleted game
        """
        if uuid in self.sessions.keys():
            return self.sessions.pop(uuid)


class GameSessionView(LoginRequiredMixin, TemplateView):
    """
    Base class view for the available session page of each game
    """
    game_manager = None
    redirect_to = 'index'

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the GET request
        Args:
            request:  WSGIRequest object containing the request information

        Returns:
            An HttpResponse object rendering the page
        """
        if self.game_manager.session_exists(self.kwargs['session']):
            self.game_manager.get(self.kwargs['session']).add_to_limbo(request.user)
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return redirect(self.redirect_to)
