"""
# Initiliaze
declare environment
give parameter value

# Q-learning algorithm
for episode in range(num_episodes):
    # initialize new episode params
    
    for step in range(max_steps_per_episode): 
        # Exploration-exploitation trade-off
        # Take new action
        # Update Q-table
        # Set new state
        # Add new reward        

    # Exploration rate decay   
    # Add current episode reward to total rewards list
"""
import gameEngine, importlib, random, config

config = importlib.import_module('config.case') 
game = gameEngine.caEnv_v0(config)                                                                                                                  
env, simulation = game.environment()




#game.runBatch()
#game.runInteractive()
