import sys  # To Exit the game
import pygame as pg
from settings import Settings
from scenes import MainMenu, GameScene


class Game():
    """Represents the game"""

    def __init__(self):
        """Initialize the game, and create resources."""
        pg.init()

        self.FPSCLOCK = pg.time.Clock()  # To control the FPS

        self.settings = Settings()

        self.screen = pg.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))

        self.current_scene = MainMenu(self.screen)

        pg.display.set_caption("Flappy Birdo")  # Title

    def set_scene(self, scene):
        self.current_scene = scene

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            else:
                code = self.current_scene._check_events(event)
                if code == "GameScene":
                    self.set_scene(GameScene(self.screen))
                elif code == "MainMenu":
                    self.set_scene(MainMenu(self.screen))

    def _update_screen(self):
        code = self.current_scene._update_screen()
        if code == "MainMenu":
            self.set_scene(MainMenu(self.screen))
        self.FPSCLOCK.tick(self.settings.FPS)


def main():
    game = Game()
    game.run_game()


main()
