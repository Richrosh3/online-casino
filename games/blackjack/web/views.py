from games.base import SessionManager, GameSessionView
from games.blackjack.game.blackjack import Blackjack

BLACKJACK_MANAGER = SessionManager(Blackjack, 'blackjack')


class BlackjackSession(GameSessionView):
    """
    The class view for a blackjack game
    """
    template_name = 'blackjack/blackjack.html'
    game_manager = BLACKJACK_MANAGER
    redirect_to = 'blackjack_sessions'
