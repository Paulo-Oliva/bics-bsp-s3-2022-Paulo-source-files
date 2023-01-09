"""
This script is used to train the model using stable-baselines3.

You can use this script to train the model for a certain number of timesteps
and then save it. You can then use the saved model to play the game.
"""

import os
import sys

import gymnasium as gym
from gymnasium.utils.env_checker import check_env

# This is a hack to make gymnasium work with stable-baselines3
sys.modules["gym"] = gym

from stable_baselines3 import PPO

# Where to save the trained models
MODELS_DIR = "models/PPO"

# Create the models directory if it doesn't exist
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# Register the environment with gymnasium
gym.register(id="FlappyBirdo-v0",
             entry_point="game:Game",
             nondeterministic=True)

# Create the environment
env = gym.make("FlappyBirdo-v0", is_ml=True)

# Check if the environment follows the gymnasium API
check_env(env.unwrapped)

# Create the model
model = PPO("MultiInputPolicy", env, verbose=1)

# After how many timesteps to save the model
TIMESTEPS = 10000

# The number of iterations that have been done
ITERATIONS = 0

while True:
    ITERATIONS += 1
    # Train the model for TIMESTEPS timesteps
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
    # Save the model
    model.save(f"{MODELS_DIR}/{TIMESTEPS*ITERATIONS}")
