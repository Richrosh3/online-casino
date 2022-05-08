from games.base import GameSessionView, SessionManager
from games.craps.game.craps import CrapsGame

CRAPS_MANAGER = SessionManager(CrapsGame, 'craps')


class CrapsSession(GameSessionView):
    template_name = 'craps/craps.html'
    game_manager = CRAPS_MANAGER
    redirect_to = 'craps_sessions'
