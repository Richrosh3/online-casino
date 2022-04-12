from games.base import SessionManager, GameSessionView

# BLACKJACK_MANAGER = SessionManager(Blackjack)


class BlackjackSession(GameSessionView):
    # template_name = 'blackjack/blackjack.html'
    # game_manager = BLACKJACK_MANAGER
    redirect_to = 'blackjack_sessions'
