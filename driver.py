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
import datetime
import matplotlib.pyplot as plt
import time
#Initializing Training
start = datetime.datetime.now()
start_time = time.time()
print("Initializing Training...")
print("Starting simulation...\n")

#define parameters
SHOW_EVERY = 10
num_episodes = 800
max_steps_per_episode = 1500
learning_rate = 0.1 
discount_rate = 0.99
exploration_rate = 1 
max_exploration_rate = 1 
min_exploration_rate = 0.01
exploration_decay_rate = 0.005

#environment set up from Traffic Analysis Software
config = importlib.import_module('config.case') 
random.seed(config.seed)
clock = pygame.time.Clock() 
speedLimits = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed) 
road = simulation.road.Road(config.lanes, config.length, speedLimits) 
totalCars = 100
numAgent = 1

def reset():
    config = importlib.import_module('config.case') 
    random.seed(config.seed)
    clock = pygame.time.Clock() 
    speedLimits = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed) 
    road = simulation.road.Road(config.lanes, config.length, speedLimits) 
    road.setEnvironment(totalCars,numAgent)
    return road

def processInfo(info):
    pass
def comments(new_state, reward, done, action, q_table):
    print("new state ", new_state)
    print("reward ", reward)
    print("done ", done)
    print("action ", action)
    print("max q: ",  np.max(q_table[new_state, :]))

def paramWrite(name, param, fyl):
    fyl.write(name+str(": ")+str(param)+"\n")

def importQtable(npyfile, new):
    if new==False:
        return  np.zeros((state_space_size, action_space_size))
    else:
        return  np.load(npyfile)

file1 =  open("outputs.txt","a") 
#set up qtable from sim program
action_space_size = road.actionSpaceSize
state_space_size = road.stateSpaceSize
q_table = importQtable("qtable_2020-04-20_11:24:30.npy",False)
rewards_all_episodes = []
timesteps = []
lapTimes = []
#q learnin algorithm

file1.write("*"*50)
file1.write("\nNew simulation started at: " + str(start.strftime("%Y-%m-%d %H:%M:%S\n"))) 
paramWrite("number of episodes",num_episodes,file1)
paramWrite("max steps per episodes",max_steps_per_episode,file1)
paramWrite("learning rate" ,learning_rate,file1)
paramWrite("discount rate" ,discount_rate,file1)
paramWrite("exploration rate", exploration_rate,file1)
paramWrite("max exploration rate", min_exploration_rate, file1)
paramWrite("min exploration rate", max_exploration_rate, file1)
paramWrite("exploration decay rate", exploration_decay_rate, file1)
for episode in range(num_episodes):
    road = reset() 
    state = road.ogstate()       
    #print("\ndefault state: ",state)
    print("Episode: " +str(episode))
    done = False
    file1.write("\nepisode " + str(episode))
    rewards_current_episode = 0
    for step in range(max_steps_per_episode):
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])
        else:
            action = road.sampleAction()
        #new_state, reward, done = road.step(action)
        new_state, reward, done = road.stepBB(action)
        #comments(new_state, reward, done, action, q_table)
        #print("step: ",step)
        #print("")
     #   rwds = processInfo(info)
        # Update Q-table for Q(s,a)
      #  print("reward ", reward)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) +  learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
        state = new_state
        rewards_current_episode += reward
        if done == True:
            break
    file1.write("\nstep : " +str(step))
    file1.write("\nrewards: "+str(rewards_current_episode-step))
#    print("step : ",step)
#    print()
    timesteps.append(step)
    # Exploration rate decay
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    rewards_all_episodes.append(rewards_current_episode-step)

#need to save records to text files
file1.write("\n\nThe Qtable for this simulation is given below:\n")
file1.write(str(q_table))
end = datetime.datetime.now()
file1.write("\n\nEnd of simulation " + str(end.strftime("%Y-%m-%d %H:%M:%S\n")))
file1.write("\nSimulation took "+ str((time.time() - start_time)/60.0) + " minutes\n") 
file1.write("*"*50+str("\n"))
file1.close() 
np.save('qtable_'+str(end.strftime("%Y-%m-%d_%H:%M:%S")),q_table)
print("Simulation is over!")


plt.plot([i for i in range(num_episodes)],rewards_all_episodes, label="rewards")
plt.plot([i for i in range(num_episodes)],timesteps, label="timesteps") 
plt.ylabel("Units")
plt.xlabel("Number of episode")
plt.legend()
plt.grid()
plt.show()

plt.plot([i for i in range(num_episodes)],rewards_all_episodes, label="rewards")
plt.ylabel("Rewards(Units)")
plt.xlabel("Number of episode")
plt.legend()
plt.grid()
plt.show()

plt.plot([i for i in range(num_episodes)],timesteps, label="timesteps")
plt.ylabel("Timesteps (Units)")
plt.xlabel("Number of episode")
plt.legend()
plt.grid()
plt.show()

"""
# Calculate and print the average reward per thousand episodes
rewards_stats = np.split(np.array(rewards_all_episodes),num_episodes/10)
count = 10
print("********Average reward per " + str(count) + " episodes********\n")
for r in rewards_stats:
    print(count, ": ", str(sum(r/2)))
    count += 2
print("\n\n********Q-table********\n")
print(q_table)   
"""

