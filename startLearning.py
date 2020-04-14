import gameEngine, importlib, random, config
import numpy as np
import pygame

#define parameters
num_episodes = 100
max_steps_per_episode = 2000 
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
print(env.reset())

#qlearning specific parameters
action_space_size = env.actionSpaceSize
state_space_size = env.stateSpaceSize
q_table = np.zeros((state_space_size, action_space_size))

rewards_all_episodes = []

for episode in range(num_episodes):  #clock mechanics or for loop
    state = env.reset() #resets sim and returns starting state of agent
    print("state ",state)
    done = False
    rewards_current_episode = 0
    while simulation.running:
        clock.tick_busy_loop(config.maxFps)#
        dt = clock.get_time()# —    time used in the previous tick
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])    
        else:
            action = env.sampleAction()   
        new_state, reward, done = simulation.update(dt,action) #updates logistics  
        print("state ", new_state)
        print("reward ", reward)
        print("done ", done)
        print("action ", action)
        print("max q: ",  np.max(q_table[new_state, :]))
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) +  learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
        state = new_state 
        rewards_current_episode += reward  
        if done == True:
            break
    # Exploration rate decay
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    rewards_all_episodes.append(rewards_current_episode)

# Calculate and print the average reward per thousand episodes
rewards_per_thosand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/10)
count = 10
print("********Average reward per ten episodes********\n")
for r in rewards_per_thosand_episodes:
    print(count, ": ", str(sum(r/10)))
    count += 10
print("\n\n********Q-table********\n")
print(q_table)    

""" To run simulation in batch or interactive mode -> uncomment the following """
#game.runBatch()
#game.runInteractive()
