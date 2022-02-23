from itertools import cycle
from time import sleep

from wordle_controller import WordleController

controller = WordleController()

# 9 colors used because 5 and 9 are coprime so repainting will give
# a different color arrangement each time.
COLORS = cycle([
    'darkmagenta',
    'darkblue',
    'darkred',
    'darkgreen',
    'darkorange',
    'darkorchid',
    'darkseagreen',
    'darksalmon',
    'darkkhaki'
])


# ====================
def display_message():

    # ====================
    def repaint_tiles():
        """Paint all the tiles by cycling through the elements of COLORS"""

        for i in range(6):
            for j in range(5):
                controller.change_tbd_style(i, j, next(COLORS))

    # ====================
    def flip_row(row_index: int, sleep_between_tiles: float = 0.25):
        """Stimulate flip animation on a row of the board, painting each tile
        a new colour in the process."""

        for i in range(5):
            controller.flip_letter(row_index, i)
            sleep(sleep_between_tiles)
            controller.change_tbd_style(row_index, i, next(COLORS))

    sleep(1)
    sleep_between_letters = 0.5
    sleep_between_words = 1.5

    # === HAPPY ===
    controller.write_word('happy', 0, sleep_between_letters)
    flip_row(0)
    sleep(sleep_between_words)
    # === BDAY ===
    sleep_between_letters -= 0.1
    sleep_between_words -= 0.5
    controller.write_word('bday ', 1, sleep_between_letters)
    flip_row(1)
    sleep(sleep_between_words)
    # === BRO!! ===
    sleep_between_letters -= 0.1
    sleep_between_words -= 0.5
    controller.write_word('bro!!', 2, sleep_between_letters)
    flip_row(2)
    sleep(sleep_between_words)
    # === cakes ===
    controller.write_word('🎂🎂🎂🎂🎂', 3, sleep_between_letters)
    flip_row(3)
    # === beer ===
    controller.write_word('🍺🍺🍺🍺🍺', 4, sleep_between_letters)
    flip_row(4)
    # === PRESENT ===
    controller.write_word('🎁🎁🎁🎁🎁', 5, sleep_between_letters)
    flip_row(5)

    for _ in range(10):
        repaint_tiles()

    sleep(10)


# ====================
if __name__ == "__main__":

    display_message()
