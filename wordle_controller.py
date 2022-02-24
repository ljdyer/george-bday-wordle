"""
wordle_controller.py

Defines a class WordleController for making various changes to the Wordle
website with selenium.
"""

import atexit
import re
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WORDLE_HOME = 'https://www.nytimes.com/games/wordle/index.html'
ACCEPT_COOKIES_XPATH = '//*[@id="pz-gdpr-btn-accept"]'


class WordleController:
    """
    A class to represent a browser window that is displaying the Wordle
    website.

    Method called directly by play_wordle.py:
    """

    # ====================
    def __init__(self):

        # Initialize web driver
        self.init_driver()

        # Always quit driver when app finishes
        @atexit.register
        def kill_me():
            self.kill()

        # Get the Wordle page ready
        self.driver.get(WORDLE_HOME)
        self.accept_cookies()
        self.close_instructions()

        # Get access to parts of DOM inside shadow trees
        self.init_game_app()
        self.init_game_theme_manager()
        self.init_keyboard()
        self.init_rows()

    # ====================
    def init_driver(self):
        """Initialise the main web driver"""

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome('./chromedriver', options=options)

    # ====================
    def accept_cookies(self):
        """Click the button to accept cookies"""

        try:
            (WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  ACCEPT_COOKIES_XPATH)))
                .click())
        except TimeoutException:
            # It's possible the cookies dialogue wasn't displayed, so move on
            # for now
            pass

    # ====================
    def close_instructions(self):
        """Close the instructions modal"""

        # Instructions are displayed in a modal that disappears when we click
        # anywhere in the document body
        try:
            (WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                .click())
        except TimeoutException:
            # This is an problem. Raise an exception.
            raise RuntimeError('Unable to locate document body.')

    # ====================
    def init_game_app(self):
        """Get access to the part of the DOM inside the tag <game-app>, which
        is a shadow host"""

        self.game_app = (self.driver.find_element(By.CSS_SELECTOR, "game-app")
                         .shadow_root)

    # ====================
    def init_game_theme_manager(self):
        """Get access to the part of DOM inside the tag <game-theme-manager>,
        which appears to be a shadow host from inspection of the HTML but for
        some reason can be accessed as-is"""

        self.game_theme_manager = (self.game_app
                                   .find_element(By.CSS_SELECTOR,
                                                 "game-theme-manager"))

    # ====================
    def init_keyboard(self):
        """Get access to the part of the DOM inside the tag <keyboard>, which
        is a shadow host"""

        self.keyboard = (self.game_theme_manager
                         .find_element(By.CSS_SELECTOR, "game-keyboard")
                         .shadow_root)

    # ====================
    def init_rows(self):
        """Get access to the rows of the game board"""

        self.rows = []
        for row_index in range(6):
            self.rows.append(self.game_theme_manager.find_elements(
                By.CSS_SELECTOR, "game-row")[row_index].shadow_root)

    # ====================
    def write_word(self, word: str, row_index: int, interval_time: float):
        """Display the word in the row with row_index, waiting interval_time
        seconds between displaying each letter"""

        row = self.rows[row_index]
        tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
        for tile, letter in zip(tiles, list(word)):
            self.driver.execute_script(
                "arguments[0].setAttribute('letter', arguments[1])",
                tile, letter
            )
            sleep(interval_time)

    # ====================
    def set_letter(self, row_index: int, col_index: int, letter: str):
        """Set the tile in the row and column specified to the letter
        specified"""

        row = self.rows[row_index]
        tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
        tile = tiles[col_index]
        self.driver.execute_script(
            "arguments[0].setAttribute('letter', arguments[1])",
            tile, letter)

    # ====================
    def flip_letter(self, row_index: int, col_index: int):
        """Trigger the 'flip in' animation for the tile in the row and column
        specified"""

        row = self.rows[row_index]
        tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
        tile = tiles[col_index].shadow_root
        tile_div = tile.find_element(By.CSS_SELECTOR, "div.tile")
        self.driver.execute_script(
            "arguments[0].setAttribute('data-animation', 'flip-in')",
            tile_div
        )

    # ====================
    def change_tbd_color(self, row_index: int, col_index: int, color: str):
        """Change the background-color attribute for .tile[data-state='tbd']
        in the style tag associated with the tile in the row and column
        specified"""

        row = self.rows[row_index]
        tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
        tile = tiles[col_index].shadow_root
        style_tag = tile.find_element(By.CSS_SELECTOR, "style")

        old_style = style_tag.get_attribute('innerText')
        # If this is the first time we are changing the style
        if 'var(--color-tone-7)' in old_style:
            new_style = old_style.replace('var(--color-tone-7)',
                                          f'{color} /*here*/')
        # Otherwise, we left the comment '/*here*/ to mark the spot
        elif re.search(r'background-color: \w* \/\*here\*\/', old_style):
            new_style = re.sub(
                r'background-color: \w* \/\*here\*\/',
                f'background-color: {color} /*here*/',
                old_style
            )
        else:
            raise RuntimeError('Could not locate tbd background color!')

        self.driver.execute_script(
            "arguments[0].innerHTML = arguments[1]",
            style_tag, new_style
        )

    # ====================
    def kill(self):
        """Quit the driver"""

        self.driver.quit()
        print('Driver terminated.')
        print()
