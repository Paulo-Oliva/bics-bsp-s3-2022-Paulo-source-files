import pygame as pg


class Sprite():
    """Represents a 2D object in the game.
    """

    def __init__(self, x: int, y: int, sprite, surface):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.surface = surface

    def draw(self):
        """Draws the sprite on the screen.
        """
        self.surface.blit(self.sprite, (self.x, self.y))


class Player(Sprite):
    """
    Represents the player.

    Attributes:
            x: The x coordinate of the player.
            y: The y coordinate of the player.
            sprite: The sprite of the player.
            surface: The surface where to paint the player.
    """

    def __init__(self, x, y, surface):
        super().__init__(
            x, y,
            pg.image.load("resources/sprites/bird.png").convert_alpha(),
            surface)

        self.velocity = -9
        self.max_velocity_y = 10
        self.min_velocity_y = -8
        self.acc_y = 1

        self.jump_velocity = -8  # velocity while flapping
        self.is_flapping = False  # It is true only when the bird is flapping

    def jump(self):
        if self.y > 0:
            self.velocity = self.jump_velocity
            self.is_flapping = True

    def update(self):
        if self.is_flapping:
            self.is_flapping = False
        else:
            if self.velocity < self.max_velocity_y:
                self.velocity += self.acc_y
        self.y += self.velocity

        if self.y < 0:
            self.y = 0
            self.velocity = 0

        if self.y > self.surface.get_height() - self.sprite.get_height():
            self.y = self.surface.get_height() - self.sprite.get_height()
            self.velocity = 0


class Pipe(Sprite):

    def __init__(self, x: int, y: int, upside_down: bool, surface):
        if upside_down:
            sprite = pg.transform.flip(
                pg.image.load("resources/sprites/pipe.png").convert_alpha(),
                False, True)
        else:
            sprite = pg.image.load(
                "resources/sprites/pipe.png").convert_alpha()
        super().__init__(x, y, sprite, surface)
        self.velocity = -4

    def update(self):
        self.x += self.velocity

    def collides(self, player: Player) -> bool:
        """
        Checks if the player is colliding with the pipe.
        """
        # Check if the player is colliding with the pipe
        if self.x < player.x + player.sprite.get_width(
        ) and self.x + self.sprite.get_width() > player.x:
            if self.y < player.y + player.sprite.get_height(
            ) and self.y + self.sprite.get_height() > player.y:
                return True
        return False


class Background(Sprite):
    pass
