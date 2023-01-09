"""
This module contains the Settings class
which contains the settings for the game.
"""


class Settings:
    """
    This class contains the settings for the game.

    Attributes:
        SCREEN_WIDTH (int): The width of the screen.
        SCREEN_HEIGHT (int): The height of the screen.
        BG_COLOUR (tuple[int,int,int]): The background colour of the screen.
        Not to be confused with the background image.
        FPS (int): The frames per second.
    """

    def __init__(self):
        """
        Initializes the settings.
        """
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 300, 512
        self.BG_COLOUR = (225, 225, 225)
        self.FPS = 30
