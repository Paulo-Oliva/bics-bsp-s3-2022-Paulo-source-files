"""
This module contains the classes that represent the objects in the game.

It contains the Sprite class, the Player class, the Pipe class and the
Background class.
"""

import pygame as pg


class Sprite():
    """
    Represents a 2D sprite in the game.

    Attributes:
        x (int): The x coordinate of the sprite.
        y (int): The y coordinate of the sprite.
        sprite (pg.Surface): The sprite.
        surface (pg.Surface): The surface where to paint the sprite.
    """

    def __init__(self, x: int, y: int, sprite, surface):
        """
        Initializes the sprite.

        Args:
            x (int): The x coordinate of the sprite.
            y (int): The y coordinate of the sprite.
            sprite (pg.Surface): The sprite.
            surface (pg.Surface): The surface where to paint the sprite.
        """
        self.x = x
        self.y = y
        self.sprite = sprite
        self.surface = surface

    def draw(self):
        """
        Draws the sprite on the screen.
        """
        self.surface.blit(self.sprite, (self.x, self.y))


class Player(Sprite):
    """
    Represents the player.

    Attributes:
        velocity (int): The velocity of the player.
        MAX_VELOCITY_Y (int): The maximum velocity of the player in the y axis.
        MIN_VELOCITY_Y (int): The minimum velocity of the player in the y axis.
        ACC_Y (int): The acceleration of the player.
        JUMP_VELOCITY (int): The velocity of the player when it jumps.
    """

    def __init__(self, x: int, y: int, surface):
        """
        Initializes the player.

        Args:
            x (int): The x coordinate of the player.
            y (int): The y coordinate of the player.
            surface (pg.Surface): The surface where to paint the player.
        """
        super().__init__(
            x, y,
            pg.image.load("resources/sprites/bird.png").convert_alpha(),
            surface)
        # Initualize the attributes
        self.velocity = -8
        self.MAX_VELOCITY_Y = 10
        self.MIN_VELOCITY_Y = -8
        self.ACC_Y = 1
        self.JUMP_VELOCITY = -8

    def jump(self):
        """
        Makes the player jump.

        When the player jumps, its velocity is set to the jump velocity.
        """
        self.velocity = self.JUMP_VELOCITY

    def update(self):
        """
        Updates the position of the player.

        This method is called every frame. It updates the position of the
        player by adding the velocity to the y coordinate.
        """
        # If the velocity is less than the maximum velocity, increase it
        # by the acceleration to simulate gravity
        if self.velocity < self.MAX_VELOCITY_Y:
            self.velocity += self.ACC_Y
        # Update the position of the player
        self.y += self.velocity
        # Check if the player is out of the top of the screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        # Check if the player is out of the bottom of the screen
        if self.y > self.surface.get_height() - self.sprite.get_height():
            self.y = self.surface.get_height() - self.sprite.get_height()
            self.velocity = 0

    def take_action(self, action: str):
        """
        Makes the player take an action.

        This method is used in the environment to make the player take an
        action.

        Args:
            action (str): The action to take.
        """
        if action == "jump":
            self.jump()


class Pipe(Sprite):
    """
    Represents a pipe.

    Attributes:
        velocity (int): The velocity of the pipe.
    """

    def __init__(self, x: int, y: int, upside_down: bool, surface):
        """
        Initializes the pipe.

        Args:
            x (int): The x coordinate of the pipe.
            y (int): The y coordinate of the pipe.
            upside_down (bool): Whether the pipe is upside down or not.
            surface (pg.Surface): The surface where to paint the pipe.
        """
        if upside_down:
            # If the pipe is upside down, flip the sprite
            sprite = pg.transform.flip(
                pg.image.load("resources/sprites/pipe.png").convert_alpha(),
                False, True)
        else:
            sprite = pg.image.load(
                "resources/sprites/pipe.png").convert_alpha()

        super().__init__(x, y, sprite, surface)
        # Set the velocity of the pipe
        self.velocity = -4

    def update(self):
        """
        Updates the position of the pipe.

        The position of the pipe is updated by adding the velocity to the x
        coordinate.
        """
        self.x += self.velocity

    def collides(self, player: Player) -> bool:
        """
        Checks if the player is colliding with the pipe.

        Args:
            player (Player): The player.

        Returns:
            bool: Whether the player is colliding with the pipe or not.
        """
        if self.x < player.x + player.sprite.get_width(
        ) and self.x + self.sprite.get_width() > player.x:
            if self.y < player.y + player.sprite.get_height(
            ) and self.y + self.sprite.get_height() > player.y:
                return True
        return False


class Background(Sprite):
    """
    Represents the background.

    Note:
        This class is basically just a Sprite with a different name.
        If anytime in the future, the background needs new functionalities,
        this class can be used to add that functionality.
    """
