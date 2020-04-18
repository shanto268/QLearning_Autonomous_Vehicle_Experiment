import sys, pygame, simulation.road, simulation.speedLimits, random, importlib, config
from representation import Representation
from simulationManager import SimulationManager
from simulation.trafficGenerators import *

class caEnv_v0():

    def __init__(self,config):
        self.config = config 
        self.data = config.data

    def displayInitialize(self, isBatch):
        if isBatch:
            print("Initializing batch simulation....")
            print("Starting simulation...\n")
        else:
            pygame.init()
            pygame.display.set_caption('Traffic Analysis Software')

    def render_interactive(self):
        random.seed(config.case.seed) 
        screen = pygame.display.set_mode(config.case.size)
        clock = pygame.time.Clock()
        speedLimits = simulation.speedLimits.SpeedLimits(config.case.speedLimits, config.case.maxSpeed)
        road = simulation.road.Road(config.case.lanes, config.case.length, speedLimits) 
        simulation_ = SimulationManager(road, config.case.trafficGenerator, config.case.updateFrame) 
        representation = Representation(screen, road, simulation_, config.case.data)
        while simulation_.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    simulation_.processKey(event.key)
            clock.tick_busy_loop(config.case.maxFps)#.tick_busy_loop = updates the clock
            dt = clock.get_time()# —	time used in the previous tick
            simulation_.update(dt) #updates logistics
            representation.draw(dt * simulation_.timeFactor) #updates graphics
            pygame.display.flip()

    def render_batch(self):
        random.seed(config.case.seed)
        clock = pygame.time.Clock()
        speedLimits = simulation.speedLimits.SpeedLimits(config.case.speedLimits, config.case.maxSpeed)
        road = simulation.road.Road(config.case.lanes, config.case.length, speedLimits)
        simulation_ = SimulationManager(road, config.case.trafficGenerator, config.case.updateFrame) 
        while simulation_.running:
            clock.tick_busy_loop(config.case.maxFps)#
            dt = clock.get_time()# —	time used in the previous tick
            simulation_.update(dt) #updates logistics
        print("\nSimulation ended...")

    def runInteractive(self):
        self.displayInitialize(False) #interactive
        self.render_interactive()

    def runBatch(self): 
        self.displayInitialize(True) #batch
        self.render_batch()
    
    def environment(self):
        random.seed(config.case.seed)
        clock = pygame.time.Clock()
        speedLimits = simulation.speedLimits.SpeedLimits(config.case.speedLimits, config.case.maxSpeed)
        road = simulation.road.Road(config.case.lanes, config.case.length, speedLimits)
        simulation_ = SimulationManager(road, config.case.trafficGenerator, config.case.updateFrame) 
        return road, simulation_, clock

    def newRun(self):
        self.displayInitialize(True) #batch
        random.seed(config.case.seed)
        clock = pygame.time.Clock()
        speedLimits = simulation.speedLimits.SpeedLimits(config.case.speedLimits, config.case.maxSpeed)
        road = simulation.road.Road(config.case.lanes, config.case.length, speedLimits)
        simulation_ = SimulationManager(road, config.case.trafficGenerator, config.case.updateFrame) 
        while simulation_.running:
            action = random.randint(0,2)
            clock.tick_busy_loop(config.case.maxFps)#
            dt = clock.get_time()# —	time used in the previous tick
            simulation_.update(dt,action) #updates logistics
        print("\nSimulation ended...")

        
    #working version 
    def qrender_interactive(self):
        self.displayInitialize(False) #interactive
        random.seed(config.case.seed) 
        screen = pygame.display.set_mode(config.case.size)
        clock = pygame.time.Clock()
        speedLimits = simulation.speedLimits.SpeedLimits(config.case.speedLimits, config.case.maxSpeed)
        road = simulation.road.Road(config.case.lanes, config.case.length, speedLimits) 
        simulation_ = SimulationManager(road, config.case.trafficGenerator, config.case.updateFrame) 
        representation = Representation(screen, road, simulation_, config.case.data)
        while simulation_.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    simulation_.processKey(event.key)
            action = random.randint(0,2)
            clock.tick_busy_loop(config.case.maxFps)#.tick_busy_loop = updates the clock
            dt = clock.get_time()# —	time used in the previous tick
            simulation_.update(dt,action) #updates logistics
            representation.draw(dt * simulation_.timeFactor) #updates graphics
            pygame.display.flip()  
