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
  exploration_decay_rate = 0.001
```

## QState 
Matrix composed of 300 rows and 3 columns.
The rows correspond to the state space (300 grids in the road data structure).
The columns correspond to the action space (change lane up, change lane down, do not change lane)

## Reward Function Logic
The current version of the program has the reward function working as follows:
```python
 52     def qUpdateLane(self,act):
 53         self.prevPos = self.pos
 54         if self.vtype == 1: 
 55             Car.laneChangeProbability = (1 -float(data[7]))  #SAS 2020
 56             self.updateLaneLogic()
 57             return self.pos   
 58         else:
 59             return self.agentLaneChange(act)
 60  
 61     #lane change decision to action convert
 62     #action to lane change decision
 63     #reward allocation based on lane changes
 64     def agentLaneChange(self, act):
 65         if act == 1 and self.AgentLaneChangePossibleUp(): #lane change up
 66             self.pos = self.pos[0], max(0,self.pos[1]-1)
 67         elif act == 2 and self.AgentLaneChangePossibleDown(): #lane change down
 68             self.pos = self.pos[0], min(2,self.pos[1]+2)
 69         else: #no lane change and not safe to change lane
 70             self.pos = self.pos[0], self.pos[1]
 71     #    print("pos: " ,self.pos)
 72         self.allocateReward()
 73         return self.pos
 74 
 75     def allocateReward(self):
 76         if self.pos[0] < (self.road.getLength() - 5) and self.pos[0] >= 0:
 77             self.reward = min(max_hv,self.road.distanceToNextThing(self.pos))
 78         elif self.pos[0] < self.road.getLength() and self.pos[0] >= (self.road.getLength() - 5):
 79             self.reward = min(max_hv, self.road.d2n(self.pos))
 80 
 81     def AgentLaneChangePossibleUp(self):
 82         return self.road.possibleLaneChangeUp(self.pos) and self.safeToChangeLane(self.pos[1], self.pos[1] - 1)
 83 
 84     def AgentLaneChangePossibleDown(self):
 85         return self.road.possibleLaneChangeDown(self.pos) and self.safeToChangeLane(self.pos[1], self.pos[1] + 1)
 86 
 87     def safeToChangeLane(self, sourceLane, destLane):
 88         srcLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
 89         destLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], destLane) )#gets max speed at destlane
 90         prevCar = self.road.findPrevCar( (self.pos[0], destLane) )  #NaSch lane change rule safety
 91         if prevCar == None: return True #safety check 1
 92         else:
 93             distanceToPrevCar = self.pos[0] - prevCar.pos[0] #safety check 2
 94             return distanceToPrevCar > prevCar.velocity #True only if no collision
```

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
## License
[MIT](https://choosealicense.com/licenses/mit/)
