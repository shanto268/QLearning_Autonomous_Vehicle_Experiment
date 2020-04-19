# comment/uncomment for different experiment
import pygame

time_period = 100 
simTime = 1200

class SimulationManager: 
    def __init__(self, road, trafficGenerator, updateFrame):
        self.road = road
        self.trafficGenerator = trafficGenerator
        self.updateFrame = updateFrame
        self.acc = 0
        self.timeFactor = 2000.0
        self.prevTimeFactor = 1.0
        self.running = True
        self.stepsMade = 0
        self.result = [] 

    def render(self, dt):
        pass


    def update(self, dt): 
        self.acc += dt * self.timeFactor
        limit = 0 
        if self.acc >= self.updateFrame:
            self.acc = self.acc % (self.updateFrame + 0)
            self.makeStep_constant_density()  
        self.endSimulation() 
    
    """
    function of update():
        refreshes frame of sim
        executes road.update() and counts the number of steps made
        checks for end of simulation
    """

    def step_update(self, dt,act): #updates the traffic input and the car-road interplay
        self.acc += dt * self.timeFactor
        limit = 0
        if self.acc >= self.updateFrame:
            self.acc = self.acc % (self.updateFrame + 0)
            self.result = self.makeStep_constant_density(act)  #comment this for increasing density
        self.endSimulation() #comment for increasing density
        return self.result
        
    def makeSteps(self, steps): #makes multiple steps
        for x in range(steps): self.makeStep_constant_density()  #comment this for increasing density
      #  for x in range(steps): self.makeStep_increasing_density()  #uncomment this for increasing density
        
    def step_makeStep_constant_density(self,act):  #for constant density
        if self.stepsMade == 0:
            self.trafficGenerator.generate(self.road) #generates traffic
        #self.road.update(); 
        results = self.road.step(act);
        self.stepsMade += 1
        return results
  
    def makeStep_constant_density(self):  #for constant density
        if self.stepsMade == 0:
            self.trafficGenerator.generate(self.road) #generates traffic
        if self.stepsMade > 0:
            self.road.update(); 
            self.stepsMade += 1

    def processKey(self, key):
        {
            pygame.K_ESCAPE: self.__exit,
            pygame.K_SPACE:  self.__pauseSwitch,
            pygame.K_m: self.__speedUp,
            pygame.K_n: self.__speedDown,
            pygame.K_s: self.__oneStepForward,
            pygame.K_d: self.__manyStepsForward(100)
        }.get(key, lambda: print("Unknown key"))()

    def isStopped(self):
        return self.timeFactor == 0

    def __exit(self): 
        self.running = False
        
    def __pauseSwitch(self):
        self.timeFactor, self.prevTimeFactor = self.prevTimeFactor, self.timeFactor
    def __speedUp(self): 
        self.timeFactor = min(8.0, self.timeFactor*2)

    def __speedDown(self): 
        self.timeFactor = max(1/8, self.timeFactor/2)

    def __oneStepForward(self):
        if self.isStopped(): 
            self.makeStep_constant_density()  #comment this for increasing density
         #  self.makeStep_increasing_density()  #uncomment this for increasing density
        else: print("Can't make step: simulation is running")
    def __manyStepsForward(self, steps):
        def manySteps():
            self.makeSteps(steps)
        return manySteps
    
    def endSimulation(self):
        if self.road.TerminateSimulation() or self.road.updates == 2000:
            self.running = False
        
    def endSim_fd(self):
        if self.road.carCount() == 300:
            self.running = False
