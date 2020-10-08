import pygame
from logic.tiles.color import Color
from logic.tiles.shape import Shape


pygame.font.init()  # shapes are drawn as unicode characters
shape_font = pygame.font.Font('gui/segoe.ttf', 30)
text_font = pygame.font.Font('gui/segoe.ttf', 16, bold=True)

board_pos_size = 40
tile_size = 30
tile_padding = 10
tile_background_color = (30, 30, 30)

bot_plays_rects = [(0, 0, 0, 0), (0, 0, 0, 0)]
option_rects = [(0, 0, 0, 0), (0, 0, 0, 0)]

bot_btn_height = 50
bot_btn_width = 135
bot_btn_shadow = 4

def get_tile_rgb(color):
    rgb_values = {
        Color.BLUE.value:   (0, 102, 255),
        Color.RED.value:    (255, 77, 77),
        Color.GREEN.value:  (102, 255, 102),
        Color.ORANGE.value: (255, 153, 51),
        Color.PURPLE.value: (204, 102, 255),
        Color.YELLOW.value: (255, 255, 102)
    }
    return rgb_values.get(color, (0, 0, 0))


def get_shape_x_offset(shape):
    offsets = {
        Shape.CLOVER.value:  15,
        Shape.STAR.value:    12,
        Shape.CROSS.value:   17,
        Shape.CIRCLE.value:  12,
        Shape.SQUARE.value:  12,
        Shape.DIAMOND.value: 12,
    }
    return offsets.get(shape, 2)


def draw_tile(window, tile, x, y):
    pygame.draw.rect(window, tile_background_color, (x + tile_padding, y + tile_padding, tile_size, tile_size))

    shape_color = get_tile_rgb(tile.color)
    shape_text = shape_font.render(tile.shape, True, shape_color)
    shape_y_offset = 2
    shape_x_offset = get_shape_x_offset(tile.shape)
    window.blit(shape_text, (x + shape_x_offset, y + shape_y_offset))


def draw_grid(window, board, scroll_x, scroll_y):
    for row in range(len(board)):
        for col in range(len(board[row])):
            tile = board[row][col]
            tile_x = (col * board_pos_size) + scroll_x
            tile_y = (row * board_pos_size) + scroll_y
            if tile != 0:
                draw_tile(window, tile, tile_x, tile_y )


def highlight_positions(window, positions, scroll_x, scroll_y):
    offset = 6
    square_size = 38
    color = (255, 51, 153)
    for pos in positions:
        x = (pos.col * board_pos_size) + scroll_x
        y = (pos.row * board_pos_size) + scroll_y
        pygame.draw.rect(window, color, (x+offset, y+offset, square_size, square_size))


def draw_tile_hand(window, hand, x, y):
    hand_pos = 0
    for tile in hand:
        tile_x = x + (hand_pos * board_pos_size)
        draw_tile(window, tile, tile_x, y)
        hand_pos += 1


def collides(pos, rect):
    posx, posy = pos
    rectx, recty, rect_width, rect_height = rect
    if rectx <= posx <= (rectx + rect_width) and recty <= posy <= (recty + rect_height):
        return True
    else:
        return False


def draw_bots_hands(window, points_bot, smarter_bot):
    window_height = pygame.display.get_surface().get_size()[1]

    # draw racks backgrounds
    pygame.draw.rect(window, (63, 114, 175), (150, window_height - 160, 250, bot_btn_height))
    pygame.draw.rect(window, (41, 188, 139), (150, window_height - 80, 250, bot_btn_height))

    # draw bots points
    pygame.draw.rect(window, (245, 245, 245), (405, window_height - 147, 65, 30))
    pygame.draw.rect(window, (245, 245, 245), (405, window_height - 67, 65, 30))

    points_text = text_font.render(str(points_bot.points) + " pts", True, (14, 82, 164))
    window.blit(points_text, (410, window_height - 145))
    points_text = text_font.render(str(smarter_bot.points) + " pts", True, (31, 144, 106))
    window.blit(points_text, (410, window_height - 65))

    # draw tile hands
    draw_tile_hand(window, points_bot.hand, 150, window_height - 160)
    draw_tile_hand(window, smarter_bot.hand, 150, window_height - 80)


def draw_buttons(window, mouse_pos):
    window_height = pygame.display.get_surface().get_size()[1]

    button_hovered = get_button_action(mouse_pos)
    points_btn_color = (86, 135, 194) if button_hovered == "points bot plays" else (63, 114, 175)
    smarter_btn_color = (67, 214, 165) if button_hovered == "smarter bot plays" else (41, 188, 139)
    set_game_state_btn_color = (252, 246, 182) if button_hovered == "set game state" else (250, 240, 133)
    reset_btn_color = (204, 204, 204) if button_hovered == "reset" else (180, 180, 180)

    # draw bots play buttons
    pygame.draw.rect(window, (34, 61, 94), bot_plays_rects[0]) # shadow
    pygame.draw.rect(window, points_btn_color, (10, window_height - 160, bot_btn_width, bot_btn_height - bot_btn_shadow))

    pygame.draw.rect(window, (31, 144, 106), bot_plays_rects[1]) # shadow
    pygame.draw.rect(window, smarter_btn_color, (10, window_height - 80, bot_btn_width, bot_btn_height - bot_btn_shadow))

    # draw bots buttons text
    bot_name = text_font.render("Points Bot Plays", True, (245, 245, 245))
    window.blit(bot_name, (18, window_height - 150))
    bot_name = text_font.render("Smarter Bot Plays", True, (245, 245, 245))
    window.blit(bot_name, (18, window_height - 70))

    # set game state button
    pygame.draw.rect(window, (196, 180, 8), option_rects[0]) # shadow
    pygame.draw.rect(window, set_game_state_btn_color, (option_rects[0][0], option_rects[0][1], option_rects[0][2], option_rects[0][3]-5))
    option_text = text_font.render("Set Game State", True, (122, 113, 5))
    window.blit(option_text, (490, window_height - 150))

    # reset button
    pygame.draw.rect(window, (60, 60, 60), option_rects[1]) # shadow
    pygame.draw.rect(window, reset_btn_color, (option_rects[1][0], option_rects[1][1], option_rects[1][2], option_rects[0][3] - 5))
    option_text = text_font.render("Reset", True, (50, 50, 50))
    window.blit(option_text, (490, window_height - 70))

def update_buttons_positions():
    window_height = pygame.display.get_surface().get_size()[1]
    bot_plays_rects[0] = (10, window_height - 160, bot_btn_width, bot_btn_height)
    bot_plays_rects[1] = (10, window_height - 80, bot_btn_width, bot_btn_height)
    option_rects[0] = (480, window_height - 160, 130, 50)
    option_rects[1] = (480, window_height - 80, 130, 50)

def get_button_action(mouse_pos):
    update_buttons_positions()
    if collides(mouse_pos, bot_plays_rects[0]):
        return "points bot plays"
    elif collides(mouse_pos, bot_plays_rects[1]):
        return "smarter bot plays"
    elif collides(mouse_pos, option_rects[0]):
        return "set game state"
    elif collides(mouse_pos, option_rects[1]):
        return "reset"
    return None


def draw_combo_points_and_bag(window, combo_points, tiles_left):
    window_height = pygame.display.get_surface().get_size()[1]
    pygame.draw.rect(window, (245, 245, 245), (10, window_height - 200, 390, 30))

    # draw bag
    tiles_left_text = text_font.render("Bag: " + str(tiles_left), True, (60, 60, 60))
    window.blit(tiles_left_text, (10, window_height - 200))

    # draw combo points
    points_text = text_font.render("Last Combo: ", True, (60, 60, 60))
    window.blit(points_text, (150, window_height - 200))
    points_text = text_font.render(str(combo_points) + " pts", True, (255, 51, 153))
    window.blit(points_text, (240, window_height - 200))
