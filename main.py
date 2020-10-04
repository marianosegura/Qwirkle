from logic.game_objects.board import Board
from logic.bots.bot import Bot
from logic.bots.smarter_bot import SmarterBot
from logic.game_objects.bag import Bag
#from time import perf_counter

total_games = 1

points_bot_advantage = 0
smart_bot_advantage = 0

points_bot_wins = 0
smart_bot_wins = 0

for i in range(total_games):
    bag = Bag()
    board = Board()

    points_bot = Bot()
    smart_bot = SmarterBot()

    bots = [smart_bot, points_bot]

    for bot in bots:
        bot.draw_tiles(bag)

    game_finished = False
    turns = 0
    while not game_finished:
        for bot in bots:

            if game_finished:
                break

            combo = bot.get_best_combo(board)

            if combo is not None:
                combo_points = bot.get_combo_points(board, combo)
                bot.points += combo_points
                #print('')
                #print(combo_points, bot)
                bot.play_combo(board, combo)
                #  print(bot)
                #  print(combo)
                #  print(len(bag), " tiles left")
                print(board)
                bot.remove_tiles_from_hand(combo.tiles)
                bot.draw_tiles(bag)
            else:
                bag.swap_all_tiles(bot)

            # check for game finished
            if bot.out_of_tiles():
                bot.points += 6  # bonus points for finishing game
                game_finished = True
                print("Game finished", i)
                #print("turns ", turns)
                print(points_bot)
                print(smart_bot)
                print('')

                if smart_bot.points > points_bot.points:
                    smart_bot_wins += 1
                elif points_bot.points > smart_bot.points:
                    points_bot_wins += 1

                points_bot_advantage = (points_bot.points - smart_bot.points)
                smart_bot_advantage += (smart_bot.points - points_bot.points)
            turns += 1
    """
    for bot in bots:
        bot.draw_tiles(bag)
    print(board)

    smart_bot.hand = points_bot.hand
    n = 10
    print("Points bot execution times")
    for i in range(n):
        start_time = perf_counter()
        points_bot.get_best_combo(board)
        execution_time = perf_counter() - start_time
        print(execution_time)

    print('')
    print("Smart bot execution times")
    for i in range(n):
        start_time = perf_counter()
        smart_bot.get_best_combo(board)
        execution_time = perf_counter() - start_time
        print(execution_time)"""

points_advantage_average = points_bot_advantage / float(total_games)
smart_advantage_average = smart_bot_advantage / float(total_games)
print("Points bot advantage average = ", points_advantage_average)
print("Smart bot advantage average = ", smart_advantage_average)

print("Points bot wins = ", points_bot_wins)
print("Smart bot wins = ", smart_bot_wins)