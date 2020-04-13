import sys, pygame, simulation.road, simulation.speedLimits, random, importlib, config
from representation import Representation
from simulationManager import SimulationManager
from simulation.trafficGenerators import *
"""
Format of environment:

class FooEnv():

  def __init__(self):
    ...
  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human', close=False):
    ...
"""

class caEnv_v0():
    def __init__(self,config):
        self.config = config
        self.data = config.data
        print(self.data)

    def displayInitialize(self):
        pygame.init()
        pygame.display.set_caption('Traffic Analysis Software')

    def render(self):
        random.seed(config.seed) 
        screen = pygame.display.set_mode(config.size)
        clock = pygame.time.Clock()

        speedLimits = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed)
        road = simulation.road.Road(config.lanes, config.length, speedLimits) 
        simulation_ = SimulationManager(road, config.trafficGenerator, config.updateFrame) 
        representation = Representation(screen, road, simulation_, config.data)#from above functions

        while simulation_.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    simulation_.processKey(event.key)
            clock.tick_busy_loop(config.maxFps)#.tick_busy_loop = updates the clock
            dt = clock.get_time()# —	time used in the previous tick
            simulation_.update(dt) #updates logistics
            representation.draw(dt * simulation_.timeFactor) #updates graphics
         #  representation.batch(dt * simulation.timeFactor) #batch mode
            pygame.display.flip()


    def run(self):
        self.displayInitialize()
        self.render()

#main
config = importlib.import_module('config.case') #sys.argv[1] = e.g. .case or .trafficlight
game = caEnv_v0(config)
game.run()

