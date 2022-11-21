import random
from objects import Player, Pipe, Background
import pygame as pg


class MainMenu():
    """
    Represents the main menu of the game.
    """

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        # Player
        self.player = Player(screen.get_width() / 2 - 20,
                             screen.get_height() / 2, screen)

        # Pipes
        self.pipes = generate_pipes(screen)
        for pipe in self.pipes:
            pipe.x -= 100

        # Background
        self.background = Background(
            0, 0,
            pg.image.load("resources/sprites/bg.jpeg").convert(), screen)

    def _update_screen(self):
        """
        Updates the screen.
        """
        self.background.draw()
        self.player.draw()
        for pipe in self.pipes:
            pipe.draw()

        pg.display.flip()

    def _check_events(self, event: pg.event.Event):
        """
        Checks for events.

        Args:
            event (pygame.event.Event): The event to check.

        Returns:
            string: The code of the scene to switch to.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                return "GameScene"


class GameScene():
    """
    Represents the game scene.
    """

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        # Player
        self.player = Player(100, 300, screen)

        # Background
        self.background = Background(
            0, 0,
            pg.image.load("resources/sprites/bg.jpeg").convert(), screen)

        # Score
        self.score = 0

        # Pipes
        self.pipes: list[tuple[Pipe, Pipe]] = []
        self.pipes.append(generate_pipes(screen))

    def _update_screen(self):
        """
        Updates the screen.
        """
        if self._check_collisions():
            return "MainMenu"

        # Check if the player has passed a pipe
        player_mid = self.player.x + self.player.sprite.get_width() / 2
        for pipe in self.pipes:
            pipe_mid = pipe[0].x + pipe[0].sprite.get_width() / 2
            if pipe_mid <= player_mid < pipe_mid + 4:
                self.score += 1
                print(f"Your score is {self.score}")

        # Update the positions of the player and the pipes
        self.player.update()

        for pipe_tuple in self.pipes:
            pipe_tuple[0].update()
            pipe_tuple[1].update()

        # If the pipes are at the end of the screen, generate new pipes
        if 0 < self.pipes[0][0].x < 5:
            self.pipes.append(generate_pipes(self.screen))

        # If the pipes are off the screen, remove them
        if self.pipes[0][0].x < -self.pipes[0][0].sprite.get_width():
            self.pipes.pop(0)

        # Draw everything
        self.background.draw()
        self.player.draw()

        for pipe_tuple in self.pipes:
            pipe_tuple[0].draw()
            pipe_tuple[1].draw()

        # Update the screen
        pg.display.flip()

    def _check_events(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            # If the player presses space, make the player jump
            if event.key == pg.K_SPACE:
                self.player.jump()
            # If the player presses escape, go back to the main menu
            if event.key == pg.K_m:
                return "MainMenu"

    def _check_collisions(self):
        """
        Checks for collisions.
        """
        # Check if the player is colliding with the pipes
        for pipe_tuple in self.pipes:
            if pipe_tuple[0].collides(self.player) or pipe_tuple[1].collides(
                    self.player):
                return True

        # Check if the player is colliding with the ground
        if self.player.y + self.player.sprite.get_height(
        ) >= self.screen.get_height():
            return True

        return False


def generate_pipes(screen) -> tuple[Pipe, Pipe]:
    """
    Generates a pair of pipes.
    """
    # The gap between the pipes
    OFFSET = 110

    # Load the sprite for the pipes
    sprite = pg.image.load("resources/sprites/pipe.png").convert_alpha()

    # Generate the y position of the top pipe
    pipeY = random.randrange(-sprite.get_height() + OFFSET, 0)

    x = screen.get_width()

    # Generate the pipes
    pipe1 = Pipe(x, pipeY, True, screen)
    pipe2 = Pipe(x, pipeY + pipe1.sprite.get_height() + OFFSET, False, screen)

    return (pipe1, pipe2)
