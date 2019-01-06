from matplotlib import pyplot as plt
from craps_table import RollResult, Craps, CrapsStats


def play_one_round(craps):
    # Double odds table
    pass_line_bet = 5
    no_call_bet = 2 * pass_line_bet

    # Make bets
    if craps.bank >= pass_line_bet:
        craps.bet_pass_line(pass_line_bet)

    # Roll
    result = RollResult.nothing
    while result != RollResult.crap:
        result = craps.roll()
        if result == RollResult.on:
            if craps.bank >= no_call_bet:
                craps.bet_no_call(no_call_bet)

    return craps


def play_one_game(bank_init=1000,
                  num_rounds=100,
                  debug=False,
                  do_plot=False):

    bank_values = [0] * num_rounds
    iterations = num_rounds

    craps = Craps(init_bank_value=bank_init, debug=debug)

    for round_index in range(iterations):
        craps = play_one_round(craps)

        # if bank_delta > 0:
        #     win_count += 1
        # bank_deltas[round_index] = bank_delta
        if do_plot:
            bank_values[round_index] = craps.bank

        # Print out bank level at 10 points
        if debug:
            if round_index % round(iterations/10) == 0:
                print(round_index, craps.bank)

    # Show bank values over iterations
    if do_plot:
        plt.figure()
        plt.ylabel("Bank value ($)")
        plt.plot(bank_values)
        plt.show()

    return craps.stats


def calculate_threshold_percents(crap_stats_list,
                                 iterations):
    result_counts = CrapsStats.init_threshold_result_dict(init_value=0)

    for crap_stats in crap_stats_list:
        for level in crap_stats.threshold_result_dict.keys():
            if crap_stats.threshold_result_dict[level]:
                result_counts[level] += 1

    result_percents = CrapsStats.init_threshold_result_dict(init_value=0.0)
    for level, result_count in result_counts.items():
        result_percents[level] = result_count / (iterations / 100)
    # print(result_counts)
    return result_percents


def plot_game_banks(crap_stats_list,
                    num_games=10):

    plt.figure(1)
    plt.ylabel("Bank ($)")

    for index, crap_stats in enumerate(crap_stats_list):
        if index == num_games:
            break
        print(crap_stats.bank_list)
        plt.plot(crap_stats.bank_list)

    plt.show()


def run_simulation(debug=False):
    game_iterations = 10
    game_stats_list = [CrapsStats(init_bank_value=0)]*game_iterations

    for game_index in range(game_iterations):
        game_stats = play_one_game(bank_init=1000, num_rounds=100, debug=debug)
        game_stats_list[game_index] = game_stats

    # result_percents = calculate_threshold_percents(crap_stats_list=game_stats_list,
    #                                                iterations=game_iterations)

    plot_game_banks(game_stats_list, num_games=10)

    return None


def plot_dict(results_dict,
              xlabel="Value reached proportional to starting bank",
              ylabel="Probability (%)"):

    plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(results_dict.keys(), results_dict.values(), 'o')
    plt.show()


if __name__ == "__main__":
    DEBUG = False

    # play_one_game(bank_init=100,
    #               num_rounds=100,
    #               debug=True,
    #               do_plot=True)

    # for _ in range(10):
    run_simulation(debug=DEBUG)
    # plot_dict(results)

    # Test rolling
    # r = None
    # for _ in range(10):
    #     print(Roll().get())



    # # print(bank_deltas)
    # print("WIN PERCENT: {}%".format(win_percent))
    # print("START BANK: {}".format(bank_init))
    # print("NET:", sum(bank_deltas))
    # print("FINAL BANK: {}".format(craps.bank))
    #
    # print(comparison_levels, comparison_results)
