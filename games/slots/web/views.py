from games.base import SessionManager, GameSessionView
from games.slots.game.slots import Slots

SLOTS_MANAGER = SessionManager(Slots, 'slots')


class SlotsSession(GameSessionView):
    template_name = 'slots/slots.html'
    game_manager = SLOTS_MANAGER
    redirect_to = 'slots_sessions'
