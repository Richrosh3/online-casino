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

    FUNCTION_MAP = {'load_game': load_game.__func__}


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
