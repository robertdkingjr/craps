import random


class RollResult:
    crap = 0
    on = 1
    nothing = 2
    payout = 3


class Roll:
    """Roll both dice upon initialization. get() returns result sum"""
    def __init__(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)

    def get(self):
        return self.dice1 + self.dice2


class Wagers:
    """Hold all bets on the table"""
    def __init__(self):
        self.pass_line = 0
        self.no_call = 0
        # todo more bets

    def clear(self):
        self.pass_line = 0
        self.no_call = 0


class CrapMode:
    """(enum) Mode used to originally form FSM model of table... could be easily replaced"""
    # idle = 0
    on = 1
    off = 2


mode_name = {CrapMode.on: "ON",
             CrapMode.off: "OFF"}


class CrapsStats:
    """Hold all stats throughout one game-play"""

    # Check if craps bank makes it up to these levels (percentages of init)
    thresholds = [1 + .02 * x for x in range(20)]

    def __init__(self, init_bank_value):
        self.bank_init = init_bank_value
        # Hold list of bank values every time value is changed
        self.bank_list = [init_bank_value]
        # Hold bool of if bank value reaches thresholds
        self.threshold_result_dict = self.init_threshold_result_dict(init_value=False)

    @staticmethod
    def init_threshold_result_dict(init_value):
        comparison_results = {}
        for level in CrapsStats.thresholds:
            comparison_results[level] = init_value
        return comparison_results

    def process_bank_level(self, bank):
        """Populate stats based on given bank level"""

        self.bank_list.append(bank)

        # Check if balance made it to various levels
        for level in self.threshold_result_dict.keys():
            if bank > (level * self.bank_init):
                self.threshold_result_dict[level] = True


class Craps:
    """Represent all aspects of a Craps table with a single gambler (keeping track of its own stats)
    Only pass-line/no-call bets implemented so far"""

    # "True odds" payout
    true_odds = {4: 6 / 3,
                 5: 6 / 4,
                 6: 6 / 5,
                 8: 6 / 5,
                 9: 6 / 4,
                 10: 6 / 3}

    def __init__(self, init_bank_value, debug=False):
        self.debug = debug

        self.mode = CrapMode.off
        self.on_number = None

        # Assuming 1 gambler for now
        self.bets = Wagers()
        self._bank = init_bank_value
        self.stats = CrapsStats(init_bank_value=init_bank_value)

    @property
    def bank(self):
        return self._bank

    @bank.setter
    def bank(self, value):
        if value < 0:
            value = 0
        self._bank = value
        self.stats.process_bank_level(bank=self._bank)

    def report(self):
        print("MODE: {} (ON {})".format(mode_name[self.mode], self.on_number))
        print("BANK: {}".format(self.bank))

    def bet_pass_line(self, amount=5):
        if self.bank < amount:
            raise Exception("Not enough money!")
        elif self.mode is CrapMode.on:
            raise Exception("Cannot bet, game already started!")
        else:
            self.bank -= amount
            self.bets.pass_line += amount
            if self.debug:
                print("BET pass line: {}".format(amount))

    def bet_no_call(self, amount=10):
        if self.bank < amount:
            raise Exception("Not enough money!")
        elif self.mode != CrapMode.on:
            raise Exception("Cannot bet without on!")
        else:
            self.bank -= amount
            self.bets.no_call += amount
            if self.debug:
                print("BET no call: {}".format(amount))

    def roll(self):
        if self.debug:
            self.report()
        roll = Roll().get()

        if self.debug:
            print("Roll: {}".format(roll))

        if self.mode == CrapMode.off:
            if roll in [7, 11]:
                self.payout()
                return RollResult.nothing
            elif roll in [2, 3, 12]:
                self.crap_out()
                return RollResult.crap
            elif roll in self.true_odds.keys():
                self.on_number = roll
                if self.debug:
                    print("ON: {}".format(self.on_number))
                self.mode = CrapMode.on
                return RollResult.on
            else:
                raise Exception("Unhandled mode")

        elif self.mode == CrapMode.on:
            if roll == self.on_number:
                self.payout()
                self.mode = CrapMode.off
                return RollResult.payout
            elif roll in self.true_odds.keys():
                # Rolled wrong on number
                return RollResult.nothing
            elif roll == 7:
                self.crap_out()
                self.mode = CrapMode.off
                self.on_number = None
                return RollResult.crap
            elif roll in [2, 3, 11, 12]:
                return RollResult.nothing
            else:
                raise Exception("Unhandled mode")

        return RollResult.nothing

    def crap_out(self):
        self.mode = CrapMode.off
        self.bets.clear()
        if self.debug:
            print("CRAP!")
            self.report_bank()

    def payout(self):
        if self.mode == CrapMode.on:
            no_call_payback = self.bets.no_call
            true_odds_payout = self.true_odds[self.on_number] * self.bets.no_call
        else:
            no_call_payback = 0
            true_odds_payout = 0

        pass_line_payout = self.bets.pass_line

        # Keep pass line bet in place
        self.bank += pass_line_payout

        # Give back all no call bet
        self.bank += true_odds_payout
        self.bank += no_call_payback
        self.bets.no_call = 0

        self.mode = CrapMode.off
        self.on_number = None

        if self.debug:
            print("Payout: {} pass + {} true odds (+return {} no call)".format(pass_line_payout,
                                                                               true_odds_payout,
                                                                               no_call_payback))

            self.report_bank()

    def report_bank(self):
        print("Bank: {}".format(self.bank))
