"""
This module contains the Game class, which represents the game.
It can also be run to play the game manually.
"""

import sys

import gymnasium as gym
import numpy as np
import pygame as pg

from scenes import GameScene, MainMenu
from settings import Settings

sys.modules["gym"] = gym


class Game(gym.Env):
    """
    This class represents the game/environment.

    It's an extension of the `gym.Env` class.
    It contains the main loop of the game, and the methods to
    initialize the game, update the screen and check for events.

    Environment attributes:
        observation_space (gym.spaces.Dict): The observation space of the
        environment.
        action_space (gym.spaces.Discrete): The action space of the
        environment.
        _action_to_move (dict[int, str]): A dictionary that maps the action
        to the move.
        reward_range (tuple[int, int]): The reward range of the environment.

    Game attributes:
        is_ml (bool): Whether the game is being run on machine learning mode
        or not.
        screen (pg.Surface): The surface to draw the game on.
        current_scene (MainMenu | GameScene): The current scene of the game.
        Can be either the main menu or the game scene.
        clock (pg.time.Clock): The clock of the game. Used to limit the
        framerate.
        settings (Settings): The settings of the game.
    """

    def __init__(self, is_ml=False):
        """
        Initializes the game/environment.

        Args:
            is_ml (bool, optional): Whether the game is being run on
            machine learning mode or not. Defaults to False.
        """
        self.is_ml = is_ml
        # Initialize pygame related stuff
        self.initialize()
        # Set the current scene
        if self.is_ml:
            self.current_scene = GameScene(self.screen, self.is_ml)
        else:
            self.current_scene = MainMenu(self.screen)
        # Set the observation space
        self.observation_space = gym.spaces.Dict({
            "player_velocity":
            gym.spaces.Box(low=-8, high=10, shape=(1, ), dtype=np.int32),
            "x_distance":
            gym.spaces.Box(low=-126, high=166, shape=(1, ), dtype=np.int32),
            "y_upper_distance":
            gym.spaces.Box(low=-269, high=354, shape=(1, ), dtype=np.int32),
            "y_lower_distance":
            gym.spaces.Box(low=-268, high=355, shape=(1, ), dtype=np.int32),
        })
        # Set the action space
        self.action_space = gym.spaces.Discrete(2)
        # Create a dictionary that maps the action to the move
        self._action_to_move = {0: "jump", 1: "do nothing"}
        # Set the reward range
        self.reward_range = (-500, float('inf'))

    def initialize(self):
        """
        Initializes pygame, creates the screen and other attributes.
        """
        # Initialize pygame
        pg.init()
        # Set the clock to limit the framerate
        self.FPS_CLOCK = pg.time.Clock()
        # Initialize a Settings object
        self.settings = Settings()
        # Create the screen
        self.screen = pg.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        # Initialize the mixer, for playing audio
        pg.mixer.init()
        # Set the title of the window
        pg.display.set_caption("Flappy Birdo")

    def _get_obs(self) -> dict[str, np.ndarray]:
        """
        Gets the observation of the environment.

        The observation is a dictionary that contains the following keys:
            - player_velocity: The velocity of the player.
            - x_distance: The horizontal distance to the next pipe.
            - y_upper_distance: The vertical distance to the next upper pipe.
            - y_lower_distance: The vertical distance to the next lower pipe.

        The values of the dictionary are numpy arrays.

        Returns:
            dict[str, np.ndarray]: The observation of the environment.
        """
        observation = {
            "player_velocity":
            np.array([self.current_scene.player.velocity]),
            "x_distance":
            np.array(
                [self.current_scene.get_horizontal_distance_to_next_pipe()]),
            "y_upper_distance":
            np.array(
                [self.current_scene.get_vertical_distance_to_upper_pipe()]),
            "y_lower_distance":
            np.array(
                [self.current_scene.get_vertical_distance_to_lower_pipe()]),
        }
        return observation

    def _get_info(self) -> dict[str, int]:
        """
        Gets the info of the environment.

        The info is a dictionary that contains the following keys:
            - score: The score of the player.

        Returns:
            dict[str, int]: The info of the environment.
        """
        return {"score": self.current_scene.score}

    def render(self, mode="human"):
        self._update_screen()
        self._check_events()

    def step(self, action):
        self.render()

        # If the game is being run on machine learning mode
        if self.is_ml:
            # Take the action
            self.current_scene.player.take_action(self._action_to_move[action])
            # If the player has passed a pipe, give a reward of 1
            if self.current_scene.has_passed_a_pipe:
                reward = 1
                self.current_scene.has_passed_a_pipe = False
            else:
                reward = 0

            terminated = False
            # If the player has collided with a pipe, give a reward of -500
            # and terminate the episode
            if self.current_scene.check_collisions():
                reward = -500
                terminated = True
            # Return the needed values
            return self._get_obs(), reward, terminated, False, self._get_info()

    def _set_scene(self, scene):
        """
        Sets the current scene of the game.

        Args:
            scene (MainMenu | GameScene): The scene to be set.
        """
        self.current_scene = scene

    def _check_events(self):
        """
        Checks for events and handles them.
        """
        for event in pg.event.get():
            # If the user closes the window, quit the game
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            else:
                # Check for events in the current scene
                # and set the scene accordingly if needed
                code = self.current_scene.check_events(event)
                if code == "GameScene":
                    self._set_scene(GameScene(self.screen, self.is_ml))
                elif code == "MainMenu":
                    self._set_scene(MainMenu(self.screen))
                    
    def _display_score(self):
        # Display the score on the screen with Pygame
        font = pg.font.Font("resources/fonts/digitaldrip.medium.ttf", 50)

        text = font.render(f"Your score is {self.score}", True,
                           (255, 255, 255))

        self.screen.blit(text, (self.screen.get_width() / 2 - 100,
                                self.screen.get_height() / 2 - 50))

        pg.display.flip()


    def _update_screen(self):
        """
        Updates the screen.
        """
        # Update the current scene
        # and set the scene accordingly if needed
        code = self.current_scene.update_screen()
        if code == "MainMenu":
            self._set_scene(MainMenu(self.screen))
        elif code == "GameScene":
            # Reset the environment
            # Only happens in ml_mode
            self.reset()
        # Use the clock to limit the framerate
        self.FPS_CLOCK.tick(self.settings.FPS)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._set_scene(GameScene(self.screen, self.is_ml))
        return self._get_obs(), self._get_info()


# If executed directly, run the game with ml_mode set to False
if __name__ == "__main__":
    game = Game(is_ml=False)
    while True:
        game.step(1)
