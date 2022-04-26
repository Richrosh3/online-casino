from games.base import GameSessionView, SessionManager
from games.roulette.game.roulette import Roulette

ROULETTE_MANAGER = SessionManager(Roulette)

class RouletteSession(GameSessionView):
    template_name = 'roulette/roulette.html'
    game_manager = ROULETTE_MANAGER
    redirect_to = 'roulette_sessions'
