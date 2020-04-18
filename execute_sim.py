import gameEngine, importlib, random, config
import numpy as np
import pygame

#define parameters
num_episodes = 10000
max_steps_per_episode = 100 
learning_rate = 0.1 
discount_rate = 0.99

exploration_rate = 1 
max_exploration_rate = 1 
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

#environment set up from Traffic Analysis Software
config = importlib.import_module('config.case') 
game = gameEngine.caEnv_v0(config)                                                                                                                  
env, simulation, clock = game.environment()

#qlearning specific parameters
action_space_size = env.actionSpaceSize
state_space_size = env.stateSpaceSize
q_table = np.zeros((state_space_size, action_space_size))


#game.newRun()
#game.runBatch()
#game.qrender_interactive()
game.runInteractive()
