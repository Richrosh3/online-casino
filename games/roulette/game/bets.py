from games.roulette.game.wheel import Wheel


class Bets:

    @staticmethod
    def is_winner(result: str, bet: dict):
        target_numbers = bet['nums']
        if bet['type'] == 'basket':
            target_numbers = ['00', '0', '1', '2', '3']
        elif bet['type'] == 'snake':
            target_numbers = ['1', '5', '9', '12', '14', '16', '19', '23', '27', '30', '32', '34']
        elif bet['type'] == 'column':
            target_numbers = [str(i+int(bet['nums'][0]) - 1) for i in range(1, 35)]
        elif bet['type'] == 'dozen':
            if bet['nums'][0] == '1':
                target_numbers = [str(i) for i in range(1, 13)]
            elif bet['nums'][0] == '2':
                target_numbers = [str(i) for i in range(13, 24)]
            else:
                target_numbers = [str(i) for i in range(24, 37)]
        elif bet['type'] == 'color':
            target_numbers = []
            for number, color in Wheel.color_mapper.items():
                if color == bet['nums'][0]:
                    target_numbers.append(number)
        elif bet['type'] == 'even':
            target_numbers = [str(i) for i in range(2, 37, 2)]
        elif bet['type'] == 'odd':
            target_numbers = [str(i) for i in range(1, 37, 2)]
        elif bet['type'] == 'low':
            target_numbers = [str(i) for i in range(1, 19)]
        elif bet['type'] == 'high':
            target_numbers = [str(i) for i in range(19, 37)]
        return result in target_numbers

    @staticmethod
    def payout_mult(bet: dict) -> int:
        if bet['type'] == 'single':
            return 35
        elif bet['type'] == 'split':
            return 17
        elif bet['type'] == 'trio':
            return 11
        elif bet['type'] == 'street':
            return 11
        elif bet['type'] == 'corner':
            return 8
        elif bet['type'] == 'double':
            return 5
        elif bet['type'] == 'snake':
            return 2
        elif bet['type'] == 'basket':
            return 6
        elif bet['type'] == 'column':
            return 2
        elif bet['type'] == 'dozen':
            return 2
        elif bet['type'] == 'color':
            return 1
        elif bet['type'] == 'even' or bet['type'] == 'odd':
            return 1
        elif bet['type'] == 'low' or bet['type'] == 'high':
            return 1
        raise Exception

    @staticmethod
    def is_single(bet: dict) -> bool:
        return len(bet['nums']) == 1

    @staticmethod
    def is_split(bet: dict) -> bool:
        if len(bet['nums']) != 2:
            return False
        if '00' in bet['nums']:
            return '2' in bet['nums'] or '3' in bet['nums'] or '0' in bet['nums']
        elif '0' in bet['nums']:
            return '2' in bet['nums'] or '1' in bet['nums']
        return abs(int(bet['nums'][0]) - int(bet['nums'][1])) == 1 or \
               abs(int(bet['nums'][0]) - int(bet['nums'][1])) == 3

    @staticmethod
    def is_trio(bet: dict) -> bool:
        if len(bet['nums']) != 3:
            return False
        if '00' in bet['nums']:
            return '2' in bet['nums'] and '3' in bet['nums']
        elif '0' in bet['nums']:
            return '2' in bet['nums'] and '1' in bet['nums']
        return False

    @staticmethod
    def is_street(bet: dict) -> bool:
        if len(bet['nums']) != 3:
            return False
        min_val = min([int(i) for i in bet['nums']])
        return str(min_val) in Wheel.row_heads and str(min_val + 1) in bet['nums'] and str(min_val + 2) in bet['nums']

    @staticmethod
    def is_corner(bet: dict) -> bool:
        if len(bet['nums']) != 4:
            return False
        min_val = min([int(i) for i in bet['nums']])
        return str(min_val + 1) in bet['nums'] and str(min_val + 3) in bet['nums'] and str(min_val + 4) in bet['nums']

    @staticmethod
    def is_double(bet: dict) -> bool:
        if len(bet['nums']) != 6:
            return False
        min_val = min([int(i) for i in bet['nums']])
        return str(min_val) in Wheel.row_heads and not any([(min_val + 1) not in bet['nums'] for i in range(1, 6)])

    BET_CHECKER = {'single': is_single.__func__, 'split': is_split.__func__,
                   'trio': is_trio.__func__, 'street': is_street.__func__,
                   'corner': is_corner.__func__, 'double': is_double.__func__}
