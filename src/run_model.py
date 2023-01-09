"""
This script runs the game using a trained model.
"""

import sys

import gymnasium as gym

# This is a hack to make gymnasium work with stable-baselines3
sys.modules["gym"] = gym
from stable_baselines3 import PPO

if __name__ == "__main__":
    # Register the environment with gymnasium
    gym.register(id="FlappyBirdo-v0",
                 entry_point="game:Game",
                 nondeterministic=True)

    # Create the environment
    env = gym.make("FlappyBirdo-v0", is_ml=True)

    # Load the model
    MODELS_DIR = "models/PPO"
    model_path = f"{MODELS_DIR}/7100000.zip"
    model = PPO.load(model_path)

    # The number of episodes to run
    EPISODES = 5

    for ep in range(EPISODES):
        # Reset the environment
        obs, info = env.reset()
        done = False
        while not done:
            # Get a prediction
            action, _ = model.predict(obs)
            # Use the action
            obs, rewards, terminated, truncated, info = env.step(action.item())
            # Render the game
            env.render()
            # If the episode is over, set done to True
            done = terminated or truncated
