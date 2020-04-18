"""
Functionality:
    must have qlearning capabilites
    must be able to run sim 
    must be able to communicate with sim program
Need to fix:
    reseting after episode ends 
    may be add visuals to check progress
"""
#needed libraries and code files
import sys, pygame, simulation.road, simulation.speedLimits, random, importlib, config
from representation import Representation
from simulationManager import SimulationManager
from simulation.trafficGenerators import *

#print to console
print("Initializing batch simulation....")
print("Starting simulation...\n")

#define parameters
num_episodes = 100 
max_steps_per_episode = 2000 
learning_rate = 0.1 
discount_rate = 0.99
exploration_rate = 1 
max_exploration_rate = 1 
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

#roadironment set up from Traffic Analysis Software
config = importlib.import_module('config.case') 
random.seed(config.seed)
clock = pygame.time.Clock() 
speedLimits = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed) 
road = simulation.road.Road(config.lanes, config.length, speedLimits) 
simulation = SimulationManager(road, config.trafficGenerator, config.updateFrame)

#set up qtable from sim program
action_space_size = road.actionSpaceSize
state_space_size = road.stateSpaceSize
q_table = np.zeros((state_space_size, action_space_size))
rewards_all_episodes = []

#q learnin algorithm
for episode in range(num_episodes):
    state = road.reset()        #need to ensure that sim starts from the same state
    print("============================================= NEW EPISODE ==================================")
    print("default state: ",state)
    done = False
    rewards_current_episode = 0
    while simulation.running:   #may need to change this to for loop with max time steps
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])
        else:
            action = road.sampleAction()
        #update agent needs to be entered here
        new_state, reward, done = road.step(action)
        print("new state ", new_state)
        print("reward ", reward)
        print("done ", done)
        print("action ", action)
        print("max q: ",  np.max(q_table[new_state, :]))
        # Update Q-table for Q(s,a)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) +  learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
        state = new_state
        rewards_current_episode += reward
        print()
        if done == True:
            break
    # Exploration rate decay
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    rewards_all_episodes.append(rewards_current_episode)
