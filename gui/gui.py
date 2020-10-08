from gui.display_utilities import *
from gui.tile_translation_utilities import *
from logic.bots.bot import Bot
from logic.bots.smarter_bot import SmarterBot
from logic.game_objects.bag import Bag
from logic.game_objects.board import Board
import ast

def run_gui():
    fps = 60 # pygame frame rate
    window = pygame.display.set_mode((800, 600), pygame.RESIZABLE) # pygame rezisable window
    pygame.display.set_caption('Qwirkle') # window title
    clock = pygame.time.Clock() # clock used to refresh the display

    board_object = Board() # board object that contains the tile grid
    highlighted_positions = [] # last positions played by a bot are highlighted

    bag = Bag() # contains the game tiles initially

    points_bot = Bot() # first bot, decides only based on points
    smarter_bot = SmarterBot() # second bot, decides upon qwirkle chances and lines killed
    last_combo_points = 0 # the last combo points are displayed

    points_bot.draw_tiles(bag) # both bots draw tiles
    smarter_bot.draw_tiles(bag)

    scroll_x = 0 # scroll values are used to move the board on screen
    scroll_y = 0
    scrolling_velocity = 2

    game_finished = False # indicates if the game is finished
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # close game event
                run = False

            if event.type == pygame.VIDEORESIZE:  # screen resize update event
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:  # button events
                button_action = get_button_action(pygame.mouse.get_pos())
                if button_action:

                    if button_action == "points bot plays" or button_action == "smarter bot plays" and not game_finished: # bot plays turn
                        bot = points_bot if button_action == "points bot plays" else smarter_bot
                        combo = bot.get_best_combo(board_object)
                        if combo is not None:
                            last_combo_points = bot.get_combo_points(board_object, combo)
                            bot.points += last_combo_points
                            bot.play_combo(board_object, combo)
                            bot.remove_tiles_from_hand(combo.tiles)
                            bot.draw_tiles(bag)

                            highlighted_positions = board_object.get_current_tiles_positions(combo.tiles)
                        else:
                            bag.swap_all_tiles(bot) # bot can't play any combo with current hand

                        if bot.out_of_tiles():  # game is finished
                            game_finished = True

                    if button_action == "reset" or button_action == "set game state": # common reset code between reset  and set game state
                        game_finished = False
                        bag = Bag()
                        points_bot = Bot()
                        smarter_bot = SmarterBot()
                        last_combo_points = 0
                        highlighted_positions = []

                    if button_action == "reset":  # reset game
                        board_object = Board([[0]])
                        points_bot.draw_tiles(bag)
                        smarter_bot.draw_tiles(bag)

                    if button_action == "set game state": # set board state
                        string_board = []
                        string_hand = []
                        board_preset = input("Input board preset (0, 1), or empty for new one:")
                        if board_preset != "":
                            string_hand, string_board = get_board_preset(int(board_preset))
                        else:
                            string_board = input("Input board state: ")
                            string_hand = input("Bot hand: ")

                        board_object = Board(translate_tile_board(ast.literal_eval(string_board)))

                        points_bot.hand = translate_tile_list(ast.literal_eval(string_hand))
                        if not points_bot.hand:
                            points_bot.draw_tiles(bag)

                        smarter_bot.hand = translate_tile_list(ast.literal_eval(string_hand))
                        if not smarter_bot.hand:
                            smarter_bot.draw_tiles(bag)


        pressed = pygame.key.get_pressed() # board scrolling key events
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            scroll_y -= scrolling_velocity
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            scroll_y += scrolling_velocity
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            scroll_x += scrolling_velocity
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            scroll_x -= scrolling_velocity

        window.fill((245, 245, 245)) # window background

        highlight_positions(window, highlighted_positions, scroll_x, scroll_y)
        draw_grid(window, board_object.board, scroll_x, scroll_y)
        draw_combo_points_and_bag(window, last_combo_points, len(bag))
        draw_bots_hands(window, points_bot, smarter_bot)
        draw_buttons(window, pygame.mouse.get_pos())
        #pygame.mouse.get_pos()
        pygame.display.update()  # update display
        clock.tick(fps)  # keep constant frame rate

    pygame.quit() # close window
