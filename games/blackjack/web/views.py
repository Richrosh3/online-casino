from games.base import SessionManager, GameSessionView
from games.blackjack.game.blackjack import Blackjack

BLACKJACK_MANAGER = SessionManager(Blackjack)


class BlackjackSession(GameSessionView):
    template_name = 'blackjack/blackjack.html'
    game_manager = BLACKJACK_MANAGER
    redirect_to = 'blackjack_sessions'
