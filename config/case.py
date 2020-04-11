# change densities 
# change maxspeed

import simulation.road, simulation.speedLimits
import random
import sys
from simulation.speedLimits import *
from simulation.trafficGenerators import *

#avpercent = sys.argv[1]

maxFps= 500 #default = 40 , fast = 10, nice = 500
size = width, heigth = 1250, 500
# in miliseconds
updateFrame = 500 #default = 500, fast = 10 , nice 500

seed = 20

lanes = 3
length = 100
numCar = int(sys.argv[2])

trafficGenerator = TrafficGenerator(numCar) #density 0.08= 24, 0.2 = 60, 0.6 = 180 , 0.4 = 120    #if 15 then that means increase system density linearly
#trafficGenerator = GaussianTrafficGenerator(15,25) #Needs A LOT OF WORK!
speedLimits = []

maxSpeed = int(sys.argv[3])
maxLength = 1000
l = 139
ti = 20

t = random.randint(7,13)

slowDownProbability, laneChangeProbability = 0,0

print("\n")
print("The input parameters are: \n")
names = ["Output file name: ","Total Number of cars: ", "Maximum speed on road: ", "Maximum AV-AV speed: ", "Maximum AV-HV speed: ", "Maximum HV speed: ", "Probability of lane change of AV: ", "Probability of lane change of HV: ", "Probability of braking of AV: ", "Probability of braking of HV: ", "Number of AVs: "]

for i in range(1, len(sys.argv)):
    print(str(names[i-1]) + str(sys.argv[i]))
print("\n\n")

#traffic lights
#speedLimits = [SpeedLimit(range=((l , 0), (l ,3)), limit=0, ticks=60, active = True)]


#boundary fixed
#speedLimits = [SpeedLimit(range=((l , 0), (l ,3)), limit=0, ticks=0, active = True)]

#blinking entry and traffic lights
#speedLimits = [SpeedLimit(range=((7, 0), (7,3)), limit=0, ticks=t, active = True)] + [SpeedLimit(range=((l , 0), (l ,3)), limit=0, ticks=100, active = True)] #tick = non_zero_number = traffic light

#blinking entry and closed
#speedLimits = [SpeedLimit(range=((7, 0), (7,3)), limit=0, ticks=t, active = False)] + [SpeedLimit(range=((l , 0), (l ,3)), limit=0, ticks=0, active = True)] #tick = non_zero_number = traffic light

