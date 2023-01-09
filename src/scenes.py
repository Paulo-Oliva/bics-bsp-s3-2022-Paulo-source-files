"""
This module contains the classes that represent the different scenes of the
game.

It contains the MainMenu class, which represents the main menu of the game,
and the GameScene class, which represents the game scene.
It also contains the _generate_pipes function, which generates a pair of pipes
and is used by the 2 previous classes.
"""

import random

import pygame as pg

from objects import Background, Pipe, Player


class MainMenu():
    """
    Represents the main menu of the game.
    """

    def __init__(self, screen: pg.Surface):
        """
        Initializes the main menu.

        Args:
            screen (pg.Surface): The surface to draw the MainMenu on.
        """
        # Screen
        self.screen = screen

        # Player
        self.player = Player(screen.get_width() / 2 - 20,
                             screen.get_height() / 2, screen)

        # Pipes
        self.pipes = _generate_pipes(screen)
        self.pipes[0].y = -120
        self.pipes[1].y = 320
        for pipe in self.pipes:
            pipe.x -= 100

        # Background
        self.background = Background(
            0, 0,
            pg.image.load("resources/sprites/bg.png").convert(), screen)

    def update_screen(self):
        """
        Updates the screen.

        This method is called every frame. It updates the screen by
        drawing the background, the player and the pipes.
        """

        self.background.draw()

        self.player.draw()
        for pipe in self.pipes:
            pipe.update()
            pipe.draw()

        if self.pipes[0].x < -100:
            self.pipes[0].x = 400
            self.pipes[1].x = 400

        menu = pg.image.load("resources/sprites/menu.png")
        self.screen.blit(menu, (0, 0))

        pg.display.flip()

    def check_events(self, event: pg.event.Event) -> str | None:
        """
        Checks if the user has pressed space to start the game.

        If the user has pressed space, this method returns the string
        "GameScene", which causes the game to switch to the game scene
        and consequently start.

        Args:
            event (pg.event.Event): The event to check.

        Returns:
            str | None: The string "GameScene" if the user has pressed
            space, None otherwise.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                return "GameScene"


class GameScene():
    """
    This class represents the game scene.

    The game scene is the scene where the player plays the game.
    It contains the logic for the game.
    """

    def __init__(self, screen: pg.Surface, is_ml: bool = False):
        """
        Initializes the game scene.

        Args:
            screen (pg.Surface): The surface to draw the GameScene on.
            is_ml (bool, optional): Whether the game is being played by a
            machine learning agent or not. Defaults to False.
        """
        self.screen = screen
        self.is_ml = is_ml
        self.has_passed_a_pipe = False

        # Player
        self.player = Player(100, 300, screen)

        # Sounds
        self.flap_sound = pg.mixer.Sound("resources/audio/flap.wav")
        self.score_sound = pg.mixer.Sound("resources/audio/score.wav")
        self.collision_sound = pg.mixer.Sound("resources/audio/collision.wav")

        # Background
        self.background = Background(
            0, 0,
            pg.image.load("resources/sprites/bg.png").convert(), screen)

        # Score
        self.score = 0

        # Pipes
        self.pipes: list[tuple[Pipe, Pipe]] = []
        self.pipes.append(_generate_pipes(screen))

    def update_screen(self) -> str | None:
        """
        Updates the screen.

        Returns:
            str | None: The string "MainMenu" if the player has collided
            with a pipe or the ground and the game is not being played by
            a machine learning agent, "GameScene" if it is being played by
            a machine learning agent, None otherwise.
        """
        if self.check_collisions():
            self.collision_sound.play()
            if self.is_ml:
                return "GameScene"
            else:
                return "MainMenu"

        # Check if the player has passed a pipe
        self._check_player()
        # Update the positions of the player and the pipes
        self._update_positions()
        # Check the position of the pipes and generate/remove if needed
        self._check_pipes()
        # Draw everything
        self._draw()
        # Update the screen
        pg.display.flip()

    def _draw(self):
        """
        Draws everything on the screen.
        """
        self.background.draw()
        self.player.draw()

        for pipe_tuple in self.pipes:
            pipe_tuple[0].draw()
            pipe_tuple[1].draw()

        # Set the font and font size
        font = pg.font.Font("resources/fonts/FFFFORWA.ttf", 50)
        # Set the text to render
        text = str(self.score)
        # Render the text
        text_surface = font.render(text, True, (30, 30, 30))
        # Draw the text to the screen
        self.screen.blit(text_surface, (self.screen.get_width() / 2 -
                                        text_surface.get_rect().width / 2, 50))

    def _check_player(self):
        """
        Checks if the player has passed a pipe.

        If they did, increases the game score by 1.
        """
        player_mid = self.player.x + self.player.sprite.get_width() / 2
        for pipe in self.pipes:
            pipe_mid = pipe[0].x + pipe[0].sprite.get_width() / 2
            if pipe_mid <= player_mid < pipe_mid + 4:
                self.score_sound.play()
                self.score += 1
                self.has_passed_a_pipe = True
                print(f"Your score is {self.score}")

    def _check_pipes(self):
        """
        Checks if any pipe needs to be removed or generated and proceeds
        accordingly.

        A pipe needs to be removed if it goes off screen. Moreover, a new
        pair of pipes needs to be generated if the first pipe of the list
        is at the end of the screen.
        """
        # If the pipes are at the end of the screen, generate new pipes
        if 0 < self.pipes[0][0].x < 5:
            self.pipes.append(_generate_pipes(self.screen))

        # If the pipes are off the screen, remove them
        if self.pipes[0][0].x < -self.pipes[0][0].sprite.get_width():
            self.pipes.pop(0)

    def _update_positions(self):
        """
        Updates the positions of the player and the pipes.
        """
        self.player.update()

        for pipe_tuple in self.pipes:
            pipe_tuple[0].update()
            pipe_tuple[1].update()

    def check_events(self, event: pg.event.Event) -> str | None:
        """
        Checks if the user has pressed a key and proceeds accordingly.

        If the user has pressed space, the player jumps. If the user has
        pressed 'M', the game goes back to the main menu.

        Args:
            event (pg.event.Event): The event to check.

        Returns:
            str | None: The string "MainMenu" if the user has pressed
            'M', None otherwise.
        """
        if event.type == pg.KEYDOWN:
            # If the player presses space, make the player jump
            if event.key == pg.K_SPACE:
                self.flap_sound.play()
                self.player.jump()

            # If the player presses escape, go back to the main menu
            if event.key == pg.K_m:
                return "MainMenu"

    def check_collisions(self) -> bool:
        """
        Checks if the player has collided with a pipe or the ground.

        Returns:
            bool: True if the player has collided with a pipe or the
            ground, False otherwise.
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
        # If the player is not colliding with anything
        return False

    def get_horizontal_distance_to_next_pipe(self) -> int:
        """
        Gets the horizontal distance to the next pipe.

        If the player has passed the beginning of the pipe, the distance
        is negative.

        Returns:
            int: The horizontal distance to the next pipe.
        """
        return self.pipes[-1][0].x - (self.player.x +
                                      self.player.sprite.get_width())

    def get_vertical_distance_to_upper_pipe(self) -> int:
        """
        Gets the vertical distance to the next upper pipe.

        If the player is above the pipe, the distance is negative.

        Returns:
            int: The vertical distance to the next upper pipe.
        """
        return self.player.y - (self.pipes[-1][0].y +
                                self.pipes[-1][0].sprite.get_height())

    def get_vertical_distance_to_lower_pipe(self) -> int:
        """
        Gets the vertical distance to the next lower pipe.

        If the player is below the pipe, the distance is negative.

        Returns:
            int: The vertical distance to the next lower pipe.
        """
        return self.pipes[-1][1].y - (self.player.y +
                                      self.player.sprite.get_height())


def _generate_pipes(screen: pg.surface) -> tuple[Pipe, Pipe]:
    """
    Generates a pair of pipes.

    A pair of pipes is generated by generating the y position of the top
    pipe and then generating the two pipes.

    Args:
        screen (pg.surface): The screen to draw the pipes on.

    Returns:
        tuple[Pipe, Pipe]: A tuple containing the two pipes.
    """
    # The gap between the pipes
    OFFSET = 110

    # Load the sprite for the pipes
    sprite = pg.image.load("resources/sprites/pipe.png").convert_alpha()

    # Generate the y position of the top pipe
    pipe_y = random.randrange(-sprite.get_height() + OFFSET, 0)

    x = screen.get_width()

    # Generate the pipes
    pipe1 = Pipe(x, pipe_y, True, screen)
    pipe2 = Pipe(x, pipe_y + pipe1.sprite.get_height() + OFFSET, False, screen)

    return (pipe1, pipe2)
