from color import Color
from shape import Shape
from bag import Bag
from tile import Tile
from board import Board

b_sq = Tile(Color.BLUE.value, Shape.SQUARE.value)
b_sq2 = Tile(Color.BLUE.value, Shape.SQUARE.value)
b_cr = Tile(Color.BLUE.value, Shape.CIRCLE.value)
b_cl = Tile(Color.BLUE.value, Shape.CLOVER.value)
r_cl = Tile(Color.RED.value, Shape.CLOVER.value)
b_x = Tile(Color.BLUE.value, Shape.CROSS.value)
r_x = Tile(Color.RED.value, Shape.CROSS.value)

board = Board([[0, 0, 0, 0],
               [0, b_sq, b_cr, 0],
               [0, b_cr, 0, 0]])

print(board)
#line = [r_x, b_sq, b_cl, b_cr]
print(board.is_valid_move(r_x, 0, 1))

