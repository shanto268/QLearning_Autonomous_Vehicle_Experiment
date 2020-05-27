# QLearning Program to train an agent efficient lane changing 
Nagel Schreckenberg Cellular Automata Model for training an agent to make efficient lane change decisions using Q Learning Algorithm. 

## Description
This program has three main objects - car, road, and representation. The representation object deals with interactive mode, while the road and car classes make up the environment for the simulation. The road has three lanes with each lane having 100 cells, the road is modeled as a circular road (periodic boundary conditions). The simulation starts with 99 HVs with well defined properties randomly distributed on the road, 1 agent is also distributed randomly in the same road. Each update of the system involves each car object making lane change decisions followed by longitudinal update. The agent uses QLearning algorithms to learn the optimal lane change policy that would reduce the time taken for it to make 10 cycles on the road.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame, matplotlib and any other packages that you may be missing on your system

```bash
pip install pygame
```
## Default Mode
This version has the following simulation conditions
```bash
Total Number of cars: 100
Maximum speed on road: 5
Maximum AV-AV speed: 3
Maximum AV-HV speed: 3
Maximum HV speed: 3
Probability of lane change of AV: 0.6
Probability of lane change of HV: 0.6
Probability of braking of AV: 0.4
Probability of braking of HV: 0.4
Number of AVs: 1
Simulation Terminates at (cycles): 10
Random seed is fixed at  4
Maximum Time Steps: 2000
```
The default parameters used for qlearning are as below:
```python
  #define parameters 
  num_episodes = 100
  max_steps_per_episode = 2000
  learning_rate = 0.1 
  discount_rate = 0.99
  exploration_rate = 1 
  max_exploration_rate = 1 
  min_exploration_rate = 0.01
  exploration_decay_rate = 0.005
```

# Model/Idea (Needs Implementation)
The new model/idea of the qLearning framework involves a realistic assumption that makes the training much faster (theoretically) and the program more accurate and realistic.
The new model depends on the concept of visibility; the agent is now aware of vehicles in its vicinity (front, back and sides) and makes its decision of lane changes based on this visibility radius. This reduces the state space by a factor of 10 and thus training speed increases drastically!

## QState 
Matrix composed of 32 rows (assuming 5 cell visibility front and back and 2 cells on the sides ) and 3 columns.
The rows correspond to the state space (32 grids in the road data structure).
The columns correspond to the action space (change lane up, change lane down, do not change lane)

## Environment
The environment would be as follows:

Walkway
Road (lane 1)
Road (lane 2)
Road (lane 3)
Walkway

Note that the roads are circular (periodic boundary).

## Reward Function Logic
There are three types of rewards and two types of Penalty. 

Best Reward > Better Reward > Good Reward


Highest Penalty > Penalty

The reward function working for version 1.0 is as follows:
```python
action is passed as input to the function guiding the agent's lane change dynamics
    if action results in agent moving to an occupied lane ->  end episode and  high penalty
    if action leads to empty block and safe for moving -> good reward
    if action leads to safety and better v_potential -> highest reward
    if action leads to not changing lane and lane change was not possible -> good reward

for each cycle completed, c, record time taken, t.
        rewards += constant * ( cycle_distance / t)
        -> this would incentivize agent to increase its average speed more
        -> this would also make sure that it completes more cycles
```
Once, the aggregate reward is calculated using the above code block. The final reward for the episode is calculated as follows:
```python
final_reward = aggregate_reward - timesteps_taken_to_complete_10_cycles
```

## Cases and Resolution (Reward Allocation) for version 2.0

These are the following cases that may be result of a lane changing action.

1. Action leading to footpath
    * Highest Penalty
    * End Episode
2. Action leading to occupied cell (sideswapping collision)
    * Highest Penalty
    * End Episode
3. Action leading to collision from speeding vehicle during lane change (runaway collision)
    * Highest Penalty
    * End Episode
4. Action leading to empty cell
    * Good Reward
    * Continue Episode
5. Action to not change lane and lane change was not possible.
    * Good Reward
    * Continue Episode
6. Action leading to empty cell and not run over (safe lane switch)
    * Better Reward
    * Continue Episode
7. Action leading to safe lane switch which results in better velocity gain (optimal lane switch)
    * Best Reward
    * Continue Episode
8. Action to not change lane which results in better velocity gain (optimal cruise)
    * Best Reward
    * Continue Episode
9. Action to not change lane and lane change was possible and beneficial - velocity gain was possible and not enjoyed (nonaggressive)
    * Penalty
    * Continue Episode

## Training Plan
Training must be done for finite number of episodes and each episode must start with random initial conditions. The training code must allow for models to learn from previous trained models. The training model can include neural networks for efficient training (in the works).

## Customization
In order to change the simulation condition, edit the file "config\case.py". 
```python
  9 #sim data
 10 data = ["trial.txt",100,5,3,3,3,0.6,0.6,0.4,0.4,1,10]

"""
order of data:
 ["Output file name: ","Total Number of cars: ", "Maximum speed on road: ",
 "Maximum AV-AV speed: ", "Maximum AV-HV speed: ",     
"Maximum HV speed: ", "Probability of lane change of AV: ", 
"Probability of lane change of HV: ", "Probability of braking of AV: ", 
"Probability of braking of HV: ", "Number of AVs: ","Simulation Terminates at (cycles): "] 
"""
```
In order to change the qlearning parameters, edit respective variables in the "driver.py" file. To change the environment conditions change the "simulation/road.py" file and to change agent/other car behaviors, reward functions change the "simulation/car.py" file. 

Important methods in road.py: 
```python
self.step(act) , self.setEnvironment(totalCars,agentNum) and the constructor
```
Important methods in car.py:
```python
self.qUpdateLane(act) , self.agentLaneChange(act), self.allocateReward() and 
the constructor
```

## Usage
In your shell, execute the following code
```bash
python3 driver.py
```
## Learning Statistics
The program records the rewards, qvalues, and timesteps associated with each episode and upon termination creates a text file with these key statistics and generates two plots - rewards vs episodes, and timesteps vs episodes


## To Do/Functionality List
- [x] Fix directory (clean up)
- [ ] Implement the new state space
- [ ] Implement version 2.0
- [ ] Exit training with qtable saved may be?
- [ ] Use of Neural Networks in training
- [ ] Multiple Agent provision from NaSch software
- [ ] Provision of buses, lorries and different vehicle types in training 
- [ ] Tracking of P(lc)  [idea in my blue notebook]
(To do list (version 1.0) )
- [x] Update Reward Function
- [ ] Include a parameter to adjust the cooperation vs aggressive nature of the agent
- [ ] Identify Best Learning Parameters with respect to simulation time 
- [ ] Identify Best Learning Parameters with respect to rewards
- [ ] Train Model on HPCC Network
- [ ] Moving average, min, max, over range stats plot for rewards update
- [ ] Infer Probability(lane change) from training data 
- [ ] Incorporation of visual sim in training 
- [ ] Implement any change Dr. Li suggests
- [ ] Reducing the state space to only that of the neighboring cells of the agent
- [ ] Incorporation of random seed

## ISSUES (version 1.0):
- [ ] None type return of reward
- [ ] Factoring in time of lap into rewards

## Study Results/Findings/Questions
* The Probability of Lane Change from a trained agent will shed some light into how single opportunistic agent behaves in heterogenous flow of HVs
* The study will also contribute to Cellular Automata model for traffic simulation as it will show that safetiness and opportune behavior can be derived from the reward functions we introduced
* We can use this framework to train the agent with more than one class of vehicles for example (buses, different AV models from our previous models)
* Training in different traffic densities may also shed light on how Probability of Lane Change varies
* We can use heterogenous classes - opportunisitic and aware AVs with HVs and the agent - to learn more about herding and intelligent herding phenomenon. It would be interesting to see if the agent takes part in those behaviors.
