from itertools import cycle
from time import sleep

from wordle_controller import WordleController

controller = WordleController()

# 9 colors used because 5 and 9 are coprime, so repainting will give
# a different color arrangement each time.
COLORS = cycle([
    'darkmagenta',
    'darkseagreen',
    'darkred',
    'darkgreen',
    'darkorange',
    'darkorchid',
    'darksalmon',
    'darkblue',
    'darkkhaki'
])


# ====================
def display_message():

    # ====================
    def repaint_tiles():
        """Paint all the tiles by cycling through the elements of COLORS"""

        for i in range(6):
            for j in range(5):
                controller.change_tbd_color(i, j, next(COLORS))

    # ====================
    def flip_row(row_index: int, sleep_between_tiles: float = 0.25):
        """Simulate flip animation on a row of the board, painting each tile
        a new colour in the process."""

        for i in range(5):
            controller.flip_tile(row_index, i)
            sleep(sleep_between_tiles)
            controller.change_tbd_color(row_index, i, next(COLORS))

    sleep(10)
    # === HAPPY ===
    controller.write_word('happy', 0, 0.5)
    flip_row(0)
    sleep(1.5)
    # === BDAY ===
    controller.write_word('bday ', 1, 0.4)
    flip_row(1)
    sleep(1)
    # === BRO!! ===
    controller.write_word('bro!!', 2, 0.3)
    flip_row(2)
    sleep(0.5)
    # === cakes ===
    controller.write_word('🎂🎂🎂🎂🎂', 3, 0.2)
    flip_row(3)
    # === beer ===
    controller.write_word('🍺🍺🍺🍺🍺', 4, 0.15)
    flip_row(4)
    # === gifts ===
    controller.write_word('🎁🎁🎁🎁🎁', 5, 0.1)
    flip_row(5)

    for _ in range(10):
        repaint_tiles()

    sleep(10)


# ====================
if __name__ == "__main__":

    display_message()
