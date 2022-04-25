from decimal import Decimal
from uuid import uuid4

from django.contrib import auth
from django.test import TestCase

from accounts.models import CustomUser
from games.craps.game.craps import CrapsRound
from games.craps.web.views import CRAPS_MANAGER


class TestCrapsManager(TestCase):
    """
    Test cases for the SessionManager managing CrapsGame
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)

    def tearDown(self) -> None:
        CRAPS_MANAGER.sessions = {}

    def test_create_session_creates_new_session(self):
        self.assertEqual(0, len(CRAPS_MANAGER.sessions))
        CRAPS_MANAGER.create()
        self.assertEqual(1, len(CRAPS_MANAGER.sessions))

    def test_register_user_adds_player_to_game(self):
        session_id = CRAPS_MANAGER.create()
        CRAPS_MANAGER.register_user(session_id, self.user)
        self.assertTrue(self.user in CRAPS_MANAGER.sessions[session_id].players)

    def test_remove_user_removes_a_user_from_the_game(self):
        session_id = CRAPS_MANAGER.create()
        CRAPS_MANAGER.register_user(session_id, self.user)
        self.assertTrue(self.user in CRAPS_MANAGER.sessions[session_id].players)
        CRAPS_MANAGER.remove_user(session_id, self.user)
        self.assertFalse(self.user in CRAPS_MANAGER.sessions[session_id].players)

    def test_session_does_not_exist(self):
        self.assertFalse(CRAPS_MANAGER.session_exists(uuid4()))

    def test_session_exists(self):
        session_id = CRAPS_MANAGER.create()
        self.assertTrue(CRAPS_MANAGER.session_exists(session_id))

    def test_list_sessions_with_no_sessions(self):
        self.assertEqual({}, CRAPS_MANAGER.list_sessions())

    def test_list_sessions_with_active_sessions(self):
        CRAPS_MANAGER.create()
        CRAPS_MANAGER.create()
        self.assertEqual(2, len(CRAPS_MANAGER.list_sessions()))

    def test_get_session_that_doesnt_exist(self):
        self.assertIsNone(CRAPS_MANAGER.get(uuid4()))

    def test_get_session_that_exists(self):
        session_id = CRAPS_MANAGER.create()
        self.assertIsNotNone(CRAPS_MANAGER.get(session_id))

    def test_delete_nonexistent_session(self):
        self.assertIsNone(CRAPS_MANAGER.delete(uuid4()))

    def test_delete_existent_session(self):
        session_id = CRAPS_MANAGER.create()
        self.assertEqual(1, len(CRAPS_MANAGER.sessions))
        self.assertIsNotNone(CRAPS_MANAGER.delete(session_id))
        self.assertEqual(0, len(CRAPS_MANAGER.sessions))


class TestCrapsGame(TestCase):
    """
    Test cases for the CrapsGame class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=Decimal(2000))
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = CRAPS_MANAGER.create()
        CRAPS_MANAGER.register_user(self.session_id, self.user)
        self.game = CRAPS_MANAGER.get(self.session_id)

    def tearDown(self) -> None:
        CRAPS_MANAGER.sessions = {}

    def test_not_all_ready(self):
        self.assertFalse(self.game.all_ready())

    def test_all_ready(self):
        for player in self.game.players_ready:
            self.game.players_ready[player] = True

        self.assertTrue(self.game.all_ready())

    def test_unready_all(self):
        self.game.unready_all()

        for player in self.game.players_ready:
            self.assertFalse(self.game.players_ready[player])

    def test_ready_up_makes_player_ready(self):
        self.game.ready_up(self.user, True)
        self.assertTrue(self.game.players_ready[self.user])

    def test_ready_up_makes_player_unready(self):
        self.game.ready_up(self.user, False)
        self.assertFalse(self.game.players_ready[self.user])

    def test_update_pass_bets_works_in_game_instance(self):
        self.game.update_pass_bets(self.user, Decimal(100), Decimal(100))
        self.assertEqual(self.game.bets[self.user]['pass_bet'], Decimal(100))
        self.assertEqual(self.game.bets[self.user]['dont_pass_bet'], Decimal(100))

    def test_update_come_bets_works_in_game_instance(self):
        self.game.update_come_bets(self.user, Decimal(100), Decimal(100))
        self.assertEqual(self.game.bets[self.user]['come_bet'], Decimal(100))
        self.assertEqual(self.game.bets[self.user]['dont_come_bet'], Decimal(100))

    def test_update_pass_bets_changes_db(self):
        self.game.update_pass_bets(self.user, Decimal(100), Decimal(100))
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_balance, Decimal(1800))

    def test_update_come_bets_changes_db(self):
        self.game.update_come_bets(self.user, Decimal(100), Decimal(100))
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_balance, Decimal(1800))

    def test_calculate_payouts_changes_db(self):
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.game.round.pass_win = True
        self.game.round.dont_pass_win = True
        self.game.round.come_win = True
        self.game.round.dont_come_win = True

        self.game.update_pass_bets(self.user, Decimal(100), Decimal(100))
        self.game.update_come_bets(self.user, Decimal(100), Decimal(100))
        self.game.calculate_payouts()
        self.user.refresh_from_db()

        self.assertEqual(self.user.current_balance, Decimal(2400))

    def test_get_stage_betting1_when_round_not_started(self):
        self.game.round = None
        self.assertEqual(self.game.get_stage(), 'betting1')

    def test_get_stage_new_round_stage_is_come_out(self):
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.assertEqual(self.game.get_stage(), 'come-out')

    def test_reset_round(self):
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.game.reset()
        self.assertIsNone(self.game.round)

    def test_start_round(self):
        self.game.start_round()
        self.assertIsNotNone(self.game.round)
        self.assertEqual(self.game.get_stage(), 'come-out')

    def test_remove_player_removes_player(self):
        self.game.remove_player(self.user)
        self.assertEqual(0, len(self.game.players))
        self.assertEqual(0, len(self.game.players_ready))
        self.assertEqual(0, len(self.game.bets))

    def test_add_player_during_betting1(self):
        user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.game.add_player(user2)
        self.assertTrue(user2 in self.game.players)

    def test_add_player_during_come_out(self):
        user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.game.add_player(user2)

        self.assertFalse(user2 in self.game.players)
        self.assertTrue(user2 in self.game.waiting_room)

    def test_add_player_during_betting2(self):
        user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.game.round.stage = 'betting2'
        self.game.add_player(user2)

        self.assertFalse(user2 in self.game.players)
        self.assertTrue(user2 in self.game.waiting_room)

    def test_add_player_during_point(self):
        user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.game.round.stage = 'point'
        self.game.add_player(user2)

        self.assertFalse(user2 in self.game.players)
        self.assertTrue(user2 in self.game.waiting_room)

    def test_add_player_during_game_over(self):
        user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.game.round = CrapsRound(self.game.players, self.game.shooter)
        self.game.round.stage = 'game-over'
        self.game.add_player(user2)

        self.assertFalse(user2 in self.game.players)
        self.assertTrue(user2 in self.game.waiting_room)

    def test_dict_representation_during_betting1(self):
        self.assertEqual(self.game.dict_representation(), {
            'stage': 'betting1',
            'players': [{
                'player': self.user.username,
                'bet': {
                    'pass_bet': '0',
                    'dont_pass_bet': '0',
                    'come_bet': '0',
                    'dont_come_bet': '0'
                },
                'ready': False,
                'shooter': False
            }],
            'shooter': None,
            'round': None
        })

    def test_dict_representation_with_round(self):
        self.game.start_round()

        self.assertEqual(self.game.dict_representation(), {
            'stage': 'come-out',
            'players': [{
                'player': self.user.username,
                'bet': {
                    'pass_bet': '0',
                    'dont_pass_bet': '0',
                    'come_bet': '0',
                    'dont_come_bet': '0'
                },
                'ready': False,
                'shooter': True
            }],
            'shooter': self.user.username,
            'round': self.game.round.dict_representation()
        })


class TestCrapsRound(TestCase):
    """
    Test cases for the CrapsRound class
    """

    def setUp(self) -> None:
        CustomUser.objects.create_user(username='user', password='pass', current_balance=Decimal(2000))
        self.client.login(username='user', password='pass')
        self.user = auth.get_user(self.client)
        self.session_id = CRAPS_MANAGER.create()
        CRAPS_MANAGER.register_user(self.session_id, self.user)

        self.user2 = CustomUser.objects.create_user(username='user2', password='pass')
        CRAPS_MANAGER.register_user(self.session_id, self.user2)

        self.game = CRAPS_MANAGER.get(self.session_id)
        self.game.start_round()
        self.shooter = self.game.shooter
        self.round = self.game.round

    def tearDown(self) -> None:
        CRAPS_MANAGER.sessions = {}

    def test_init_values(self):
        self.assertEqual(self.round.players, self.game.players)
        self.assertEqual(self.round.shooter, self.shooter)
        self.assertFalse(self.round.round_over)
        self.assertEqual(self.round.stage, 'come-out')
        self.assertIsNone(self.round.point)
        self.assertFalse(self.round.pass_win)
        self.assertFalse(self.round.dont_pass_win)
        self.assertFalse(self.round.come_win)
        self.assertFalse(self.round.dont_come_win)

    def test_get_stage_when_round_created(self):
        self.assertEqual(self.round.stage, 'come-out')

    def test_roll_dice(self):
        for roll_num in range(0, 50):
            self.assertTrue(self.round.roll_dice('come_out') in range(2, 13))

    def test_come_out_2_crap_out(self):
        self.round.come_out(2)

        self.assertTrue(self.round.round_over)
        self.assertEqual(self.round.stage, 'game-over')
        self.assertFalse(self.round.pass_win)
        self.assertTrue(self.round.dont_pass_win)
        self.assertFalse(self.round.come_win)
        self.assertFalse(self.round.dont_come_win)
        self.assertIsNone(self.round.point)

    def test_come_out_3_crap_out(self):
        self.round.come_out(3)

        self.assertTrue(self.round.round_over)
        self.assertEqual(self.round.stage, 'game-over')
        self.assertFalse(self.round.pass_win)
        self.assertTrue(self.round.dont_pass_win)
        self.assertFalse(self.round.come_win)
        self.assertFalse(self.round.dont_come_win)
        self.assertIsNone(self.round.point)

    def test_come_out_12_ties(self):
        self.round.come_out(12)

        self.assertTrue(self.round.round_over)
        self.assertEqual(self.round.stage, 'game-over')
        self.assertFalse(self.round.pass_win)
        self.assertFalse(self.round.dont_pass_win)
        self.assertFalse(self.round.come_win)
        self.assertFalse(self.round.dont_come_win)
        self.assertIsNone(self.round.point)

    def test_come_out_7_natural(self):
        self.round.come_out(7)

        self.assertTrue(self.round.round_over)
        self.assertEqual(self.round.stage, 'game-over')
        self.assertTrue(self.round.pass_win)
        self.assertFalse(self.round.dont_pass_win)
        self.assertFalse(self.round.come_win)
        self.assertFalse(self.round.dont_come_win)
        self.assertIsNone(self.round.point)

    def test_come_out_11_natural(self):
        self.round.come_out(11)

        self.assertTrue(self.round.round_over)
        self.assertEqual(self.round.stage, 'game-over')
        self.assertTrue(self.round.pass_win)
        self.assertFalse(self.round.dont_pass_win)
        self.assertFalse(self.round.come_win)
        self.assertFalse(self.round.dont_come_win)
        self.assertIsNone(self.round.point)

    def test_come_out_other_rolls_continue_game(self):
        for roll_num in range(4, 11):
            # 7 would end the game
            if roll_num != 7:
                self.round.come_out(roll_num)

                self.assertFalse(self.round.round_over)
                self.assertEqual(self.round.stage, 'betting2')
                self.assertFalse(self.round.pass_win)
                self.assertFalse(self.round.dont_pass_win)
                self.assertFalse(self.round.come_win)
                self.assertFalse(self.round.dont_come_win)
                self.assertEqual(self.round.point, roll_num)

    def test_point_roll_equal_point(self):
        for roll_num in range(4, 11):
            # point can't be 7
            if roll_num != 7:
                self.round.point = roll_num
                self.round.point_roll(roll_num)

                self.assertTrue(self.round.round_over)
                self.assertEqual(self.round.stage, 'game-over')
                self.assertTrue(self.round.pass_win)
                self.assertFalse(self.round.dont_pass_win)
                self.assertTrue(self.round.come_win)
                self.assertFalse(self.round.dont_come_win)
                self.assertEqual(self.round.point, roll_num)

    def test_point_roll_is_7(self):
        for roll_num in range(4, 11):
            # point can't be 7
            if roll_num != 7:
                self.round.point = roll_num
                self.round.point_roll(7)

                self.assertTrue(self.round.round_over)
                self.assertEqual(self.round.stage, 'game-over')
                self.assertFalse(self.round.pass_win)
                self.assertTrue(self.round.dont_pass_win)
                self.assertFalse(self.round.come_win)
                self.assertTrue(self.round.dont_come_win)
                self.assertEqual(self.round.point, roll_num)

    def test_point_roll_neither(self):
        for roll_num in range(2, 12):
            for point_num in range(4, 11):
                # point cannot be 7
                # rolling 7 would end the game
                # rolling the same as the point would end the game
                if point_num != 7 and roll_num != 7 and point_num != roll_num:
                    self.round.point = point_num
                    self.round.point_roll(roll_num)

                    self.assertFalse(self.round.round_over)
                    self.assertEqual(self.round.stage, 'point')
                    self.assertFalse(self.round.pass_win)
                    self.assertFalse(self.round.dont_pass_win)
                    self.assertFalse(self.round.come_win)
                    self.assertFalse(self.round.dont_come_win)
                    self.assertEqual(self.round.point, point_num)

    def test_remove_player(self):
        self.round.remove_player(self.user2)
        self.assertTrue(self.user2 not in self.round.players)

    def test_dict_representation(self):
        self.assertEqual(self.round.dict_representation(), {
            'round_over': False,
            'point': None,
            'pass_won': False,
            'dont_pass_won': False,
            'come_won': False,
            'dont_come_won': False
        })
