from logic.tiles.tile import Tile


board_presets = [
    ("['★bl', '◆bl', '♧bl', '●bl']", "[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, '●yl', 0, 0], [0, 0, 0, 0, 0, '●pr', 0, 0], [0, 0, 0, 0, 0, '●or', 0, 0], [0, '■rd', '★rd', '◆rd', '♧rd', '●rd', 0, 0], [0, '■bl', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]"),
    ("['◆gr', '◆rd', '◆yl']", "[[0, 0,     0,     0,     0,     0,     0,     0,   0],[0, '■bl', '★bl', 'Xbl', '◆bl', '♧bl','●bl',  0,   0],[0, 0,     0,     0,     0,     0,     '●rd', 0,    0],[0, 0,     0,     0,     0,     0,     '●gr', 0,    0],[0, 0,     0,     0,     0,    '■yl', '●yl', '★yl', 0],[0, 0,     0,     0,     0,     0,     0,     0,    0]]")
    ]


def translate_tile_list(tile_list):
    for index, tile in enumerate(tile_list):
        if tile != 0:
            shape = tile[0]
            color = tile[1:]
            tile_list[index] = Tile(color, shape)
    return tile_list


def translate_tile_board(tile_board):
    for index, tile_list in enumerate(tile_board):
        tile_board[index] = translate_tile_list(tile_list)
    return tile_board


def get_board_preset(preset_index):
    if 0 <= preset_index < len(board_presets):
        return board_presets[preset_index][0], board_presets[preset_index][1]
    else:
        return board_presets[0][0], board_presets[0][1]
