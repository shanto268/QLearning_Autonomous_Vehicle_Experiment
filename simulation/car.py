# No selective headway case
from config.case import *
import random

#constants 
max_hv = int(data[5])  #SAS 2020
max_av_av = int(data[3])  #SAS 2020
max_av_hv = int(data[2])  #SAS 2020
limitCycle = int(data[11])*100 #SAS 2020
#paramaters for rewards
HIGH_PENALTY = -1000 
GOOD_REWARD = 500
BEST_REWARD = 1200

class Car:
    #LOOK INTO UPDATE X CODES --> UPDATE LANE --> ROAD.PY
    laneChangeProbability = 0
    slowDownProbability = 0
    lanetotup = []    #saves all the lane changes --> sum returns total number of lane changes
    L0 = []
    laneAv =  []      #saves all av lane changes --> sum returns av total number of lane changes
    
    def __init__(self, road, pos, velocity = 0, vtype = 0, seen = False):   #track function that updates velocity and use that as vtype
        self.velocity = velocity
        self.road = road
        self.pos = pos
        self.prevPos = pos
        self.vtype = vtype #vtype = 1 HV ; VTYPE = 2 AV
        self.time = 0
        self.lanechngup = 0
        self.lanechngdwn = 0
        self.lanechngavup = 0
        self.lanechngavdwn = 0
        self.lanechngL0 = 0
        self.contspeed = 3
        self.contprop = 30
        self.seen = seen 
        self.count = 0   #counting number of cars
        self.clusternum = 0 #number of clusters > 3
        self.clustersize = 0 #size of clusters
        self.freq = 0
        self.freqtot = 0
        self.CAVdist = 0
        self.terminate = False # SAS 2020
        self.numer = 0  #P(lanechange) = numer / denumer 2020
        self.denumer = 0 #SAS 2020
        self.reward = 0 #SAS 2020   
    
    def bare_bones_lane_change(self,act):
        self.prevPos = self.pos
        if self.vtype == 1: #vehicle is HV 
            Car.laneChangeProbability = (1 -float(data[7]))  #SAS 2020
            self.updateLaneLogic()
            return self.pos   
        else:  #vehicle is agent
            return self.bareBonesAgentLaneChange(act)
    
    def bareBonesAgentLaneChange(self,act):
    #if action results in agent moving to an occupied lane ->  end episode and  high penalty
    #if action leads to empty block and safe for moving -> good reward
    #if action leads to safety and better v_potential -> highest reward
    #constraint around boundaries
    #if terminate = true, may not need to return self.pos
        if act == 1:  #lane change up
            self.pos = self.pos[0], max(0,self.pos[1]-1)  
        elif act == 2:  #lane change down
            self.pos = self.pos[0], min(2,self.pos[1]+2)
        else: #no lane change and not safe to change lane
            self.pos = self.pos[0], self.pos[1]
        self.bareBonesAllocateReward(self.pos, act)
      #  print("terminate from car ", self.terminate) 
        return self.pos
    
    #may need to get rid of looping conditions
    def bareBonesAllocateReward(self, posn, act):
        #provision for looping
        if posn[0] < (self.road.getLength() - 5) and posn[0] >= 0:
            self.reward = self.bbReward(posn, act, True) 
        elif posn[0] < self.road.getLength() and posn[0] >= (self.road.getLength() - 5):
            self.reward = self.bbReward(posn, act, False) 

    def SpeedGain(self, sourceLane, destLane):                           
        if self.pos[0] < (self.road.getLength() - 5) and self.pos[0] >= 0:
            srcLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
            destLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], destLane) )#gets max speed at destlane
        elif self.pos[0] < self.road.getLength() and self.pos[0] >= (self.road.getLength() - 5):
            srcLaneSpeed =  self.road.d2n( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
            destLaneSpeed =  self.road.d2n( (self.pos[0], destLane) )#gets max speed at destlane
        if destLaneSpeed <= srcLaneSpeed: 
            return False 
        else:
            return True 
    
    def bbReward(self, posn, act, isInMid):
        reward = 0
        #if new position leads to occupied lane
            #high penalty
            #end episode
        #if new position leads to empty block and safe 
            #if not better v_gain
                #good reward
            #if better v_gain
                #best reward
        #if stay at lane and lane change not possible
            #good reward
        #if stay at lane and lane change possible and best v_gain at same lane
            #highest reward
        if (isInMid):
            if (act==0):
                if ( not self.road.possibleLaneChangeUp(posn) and not self.road.possibleLaneChangeDown(posn) ):
                    return GOOD_REWARD
                elif ( self.road.possibleLaneChangeUp(posn) ):
                    if (not self.SpeedGain( posn[1], posn[1] - 1 )):
                        return BEST_REWARD 
                elif ( self.road.possibleLaneChangeDown(posn) ):
                    if (not self.SpeedGain( posn[1], posn[1] + 1 )):
                        return BEST_REWARD 
            elif (act==1):
                if (not self.road.possibleLaneChangeUp(posn)): #not possible to change lane up
                    self.terminate = True 
                    return HIGH_PENALTY 
                elif ( self.road.possibleLaneChangeUp(posn) and self.safeToChangeLane(posn[1], posn[1] - 1) ):
                    if (not self.SpeedGain( posn[1], posn[1] - 1 )):
                        return GOOD_REWARD
                    elif ( self.SpeedGain( posn[1], posn[1] - 1 ) ):
                        return BEST_REWARD
            elif (act==2):
                 if (not self.road.possibleLaneChangeDown(posn)): #not possible to change lane up
                    self.terminate = True 
                    return HIGH_PENALTY 
                 elif ( self.road.possibleLaneChangeDown(posn) and self.safeToChangeLane(posn[1], posn[1] + 1) ):
                    if (not self.SpeedGain( posn[1], posn[1] + 1 )):
                        return GOOD_REWARD
                    elif ( self.SpeedGain( posn[1], posn[1] + 1 ) ):
                        return BEST_REWARD           
            #min(max_hv,self.road.distanceToNextThing(posn)) #mid
        else:
            # min(max_hv, self.road.d2n(posn)) #loop
             if (act==0):
                if ( not self.road.possibleLaneChangeUp(posn) and not self.road.possibleLaneChangeDown(posn) ):
                    return GOOD_REWARD
                elif ( self.road.possibleLaneChangeUp(posn) ):
                    if (not self.SpeedGain( posn[1], posn[1] - 1 )):
                        return  BEST_REWARD 
                elif ( self.road.possibleLaneChangeDown(posn) ):
                    if (not self.SpeedGain( posn[1], posn[1] + 1 )):
                        return  BEST_REWARD 
             elif (act==1):
                if (not self.road.possibleLaneChangeUp(posn)): #not possible to change lane up
                    self.terminate = True 
                    return  HIGH_PENALTY 
                elif ( self.road.possibleLaneChangeUp(posn) and self.safeToChangeLane(posn[1], posn[1] - 1) ):
                    if (not self.SpeedGain( posn[1], posn[1] - 1 )):
                        return  GOOD_REWARD
                    elif ( self.SpeedGain( posn[1], posn[1] - 1 ) ):
                        return  BEST_REWARD
             elif (act==2):
                 if (not self.road.possibleLaneChangeDown(posn)): #not possible to change lane up
                    self.terminate = True 
                    return  HIGH_PENALTY 
                 elif ( self.road.possibleLaneChangeDown(posn) and self.safeToChangeLane(posn[1], posn[1] + 1) ):
                    if (not self.SpeedGain( posn[1], posn[1] + 1 )):
                        return  GOOD_REWARD
                    elif ( self.SpeedGain( posn[1], posn[1] + 1 ) ):
                        return  BEST_REWARD             
        return 0

    #pos tuple for agent to state
    def pos2state(self):
        if self.vtype == 2:
            x = self.pos[0]
            y = self.pos[1]
            return y+3*x

    def qUpdateLane(self,act):
        self.prevPos = self.pos
        if self.vtype == 1: #vehicle is HV 
            Car.laneChangeProbability = (1 -float(data[7]))  #SAS 2020
            self.updateLaneLogic()
            return self.pos   
        else:  #vehicle is agent
            return self.agentLaneChange(act)
     
    #lane change decision to action convert
    #action to lane change decision
    #reward allocation based on lane changes
    def agentLaneChange(self, act):
        if act == 1 and self.AgentLaneChangePossibleUp(): #lane change up
            self.pos = self.pos[0], max(0,self.pos[1]-1)   
        elif act == 2 and self.AgentLaneChangePossibleDown(): #lane change down
            self.pos = self.pos[0], min(2,self.pos[1]+2)
        else: #no lane change and not safe to change lane
            self.pos = self.pos[0], self.pos[1]
    #    print("pos: " ,self.pos)
        self.allocateReward() 
        return self.pos

    def allocateReward(self):
        if self.pos[0] < (self.road.getLength() - 5) and self.pos[0] >= 0:
            self.reward = min(max_hv,self.road.distanceToNextThing(self.pos))
        elif self.pos[0] < self.road.getLength() and self.pos[0] >= (self.road.getLength() - 5):
            self.reward = min(max_hv, self.road.d2n(self.pos))

    def AgentLaneChangePossibleUp(self):
        return self.road.possibleLaneChangeUp(self.pos) and self.safeToChangeLane(self.pos[1], self.pos[1] - 1)

    def AgentLaneChangePossibleDown(self):
        return self.road.possibleLaneChangeDown(self.pos) and self.safeToChangeLane(self.pos[1], self.pos[1] + 1)

    def safeToChangeLane(self, sourceLane, destLane):                           
        if self.pos[0] < (self.road.getLength() - 5) and self.pos[0] >= 0:
            srcLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
            destLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], destLane) )#gets max speed at destlane
        elif self.pos[0] < self.road.getLength() and self.pos[0] >= (self.road.getLength() - 5):
            srcLaneSpeed =  self.road.d2n( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
            destLaneSpeed =  self.road.d2n( (self.pos[0], destLane) )#gets max speed at destlane
        prevCar = self.road.findPrevCar( (self.pos[0], destLane) )  #NaSch lane change rule safety
        if prevCar == None: return True #safety check 1
        else:
            distanceToPrevCar = self.pos[0] - prevCar.pos[0] #safety check 2
            return distanceToPrevCar > prevCar.velocity #True only if no collision
        
    def cluster(self):
        if self.seen == False:
            if self.vtype == 2 and self.road.ncvtype2(self.pos) == 2 and self.road.distanceToNextThing(self.pos) < 5:
                self.count += 1
            #    print(self.count)
        
            
    def cluster_loop(self):
        if self.seen == False:
            if self.vtype == 2 and self.road.ncvtype1(self.pos) == 2 and self.road.dton(self.pos) < 5 :
                self.count += 1
             #   print(self.count)

    def updateLane(self):
        self.prevPos = self.pos
        if self.vtype == 1: Car.laneChangeProbability = (1 -float(data[7]))  #SAS 2020
        else: Car.laneChangeProbability = (1 - float(data[6]))  #SAS 2020
        self.updateLaneLogic()
        return self.pos
    
    def lanecountup(self):
        self.lanechngup += 1
        Car.lanetotup.append(self.lanechngup)
        if self.vtype == 2:
            self.lanechngavup += 1
            Car.laneAv.append(self.lanechngavup)
            
    def lanecountdwn(self):
        self.lanechngdwn += 1
        Car.lanetotup.append(self.lanechngdwn)
        if self.vtype == 2:
            self.lanechngavdwn += 1
            Car.laneAv.append(self.lanechngavdwn)
       
    def lanecountL0(self):
        self.lanechngL0 += 1
        Car.L0.append(self.lanechngL0)
    
    
    def updateLaneLogic(self):
        if self.willingToChangeUp():
            self.denumer += 1
            x = random.random()
            if x >= Car.laneChangeProbability:
                self.numer +=1
                self.lanecountup()
                self.pos = self.pos[0], self.pos[1]-1
        elif self.willingToChangeDown():
            self.denumer += 1
            y = random.random()
            if y >= Car.laneChangeProbability:
                self.numer +=1
                self.lanecountdwn()
                self.pos = self.pos[0], self.pos[1]+1
                if self.pos[1] == 2:
                    self.lanecountL0()
        if self.denumer != 0 and self.vtype == 2: #SAS 2020
            print("P(lc): " + str(float(self.numer /self.denumer)))
    
    def trigger1(self):
        if ((self.road.avee / self.road.amount) * 100) >= 15:
            return True
        else: return False
    
    def trigger2(self): #avgspeed < 5 static dynamic lane
        if self.road.avg <= 1.5 :
            return True
        else: return False
     
    ''' end code '''
    def feedlaneroadpy(self):
        return sum(Car.lanetotup)
    
    def feedav(self):
        return sum(Car.laneAv)
    
    def feedlaneroadLO(self):
        return sum(Car.L0)
    
    def _updateX(self):
        self.velocity = self.calcNewVelocity()

        if self.velocity > 0 and random.random() <= Car.slowDownProbability:
            self.velocity -= 1

        self.pos = self.pos[0] + self.velocity, self.pos[1]
        if (self.pos[0] + self.velocity) >= self.road.getLength():
                self.pos = (self.pos[0] + self.velocity) % self.road.getLength(), self.pos[1]
        return self.pos
          
    def AVdistance(self):
        return self.CAVdist

    def didAVfinish(self,moved):    
        self.CAVdist += moved
        if (self.CAVdist >= limitCycle):
                self.terminate = True

    def updateX(self): #stochastic slowing down
     #   print(self.vlead(self.pos))      
    #    print(self.road.ncvtype(self.pos))
        if self.vtype == 1: Car.slowDownProbability = float(data[9]) #SAS 2020
        else: Car.slowDownProbability = float(data[8]) #SAS 2020
        if self.pos[0] < (self.road.getLength() - 5) and self.pos[0] >= 0:
            self.velocity = self.calcNewVelocity()
            self.cluster()   # need to use distancetonextthing                                                                  
            if self.velocity > 0 and random.random() <= Car.slowDownProbability:
                self.velocity -= 1
            self.pos = self.pos[0] + self.velocity, self.pos[1] 
            if self.vtype == 2:
                self.didAVfinish(self.velocity) #SAS new Add 2020
        elif self.pos[0] < self.road.getLength() and self.pos[0] >= (self.road.getLength() - 5):
            self.velocity = self.newvelocity()
            self.cluster_loop()    #need to use d2n
            if self.velocity > 0 and random.random() <= Car.slowDownProbability:
                self.velocity -= 1
            if (self.pos[0] + self.velocity) >= self.road.getLength():
                self.pos = (self.pos[0] + self.velocity) % self.road.getLength(), self.pos[1]
            else:
                self.pos = self.pos[0] + self.velocity, self.pos[1]
            if self.vtype == 2:
                self.didAVfinish(self.velocity) #SAS new add 2020
        return self.pos    

    def newvelocity(self): 
        return min(self.velocity + 1, self.road.d2n(self.pos), self.v1leadcopy(self.pos),self.maxSpeedofVehicle()) #regular v (M2)
       # return min(self.velocity + 1, self.road.d2n(self.pos), self.v1lead(self.pos)) # M1

    def calcNewVelocity(self):
        return min(self.velocity + 1, self.road.getMaxSpeedAt(self.pos), self.v2leadcopy(self.pos),self.maxSpeedofVehicle()) #regular v  (M2)
       # return min(self.velocity + 1, self.road.getMaxSpeedAt(self.pos), self.v2lead(self.pos)) # M1
    
    def maxSpeedofVehicle(self): #SAS new update 2020
        if self.vtype == 1:
            return max_hv
        else:
            return max_av_av
        
    def v2lead(self, pos): #regular case
        if self.vtype == 1: #RV
            self.freqtot += 1
            return 3
        elif self.vtype == 2: #AV
            if self.road.ncvtype2(self.pos) == 1: #AV - RV -->
                self.freqtot += 1
                return 4
            elif self.road.ncvtype2(self.pos) == 2: #AV - AV -->
                self.freqtot += 1
                self.freq += 1
                return 5
            else:
                return self.road.ncvtype2(self.pos)
            
    def v1lead(self, pos):  #looping boundary case
        if self.vtype == 1: #RV
            self.freqtot += 1
            return 3
        elif self.vtype == 2: #AV
            if self.road.ncvtype1(self.pos) == 1: #AV - RV -->
                self.freqtot += 1
                return 4
            elif self.road.ncvtype1(self.pos) == 2: #AV - AV -->
                self.freqtot += 1
                self.freq += 1
                return 5
            else:
                return self.road.ncvtype1(self.pos)
            
    
    def v2leadcopy(self, pos): #regular case
        if self.vtype == 1: #RV
            self.freqtot += 1
            return 300
        elif self.vtype == 2: #AV
            if self.road.ncvtype2(self.pos) == 1: #AV - RV -->
                self.freqtot += 1
                return 400
            elif self.road.ncvtype2(self.pos) == 2: #AV - AV -->
                self.freqtot += 1
                self.freq += 1
                return 500
            else:
                return 500
            
    def v1leadcopy(self, pos):  #looping boundary case
        if self.vtype == 1: #RV
            self.freqtot += 1
            return 300
        elif self.vtype == 2: #AV
            if self.road.ncvtype1(self.pos) == 1: #AV - RV -->
                self.freqtot += 1
                return 400
            elif self.road.ncvtype1(self.pos) == 2: #AV - AV -->
                self.freqtot += 1
                self.freq += 1
                return 500
            else:
                return 500        

    def willingToChangeUp(self):
        return self.road.possibleLaneChangeUp(self.pos) and self.__willingToChangeLane(self.pos[1], self.pos[1] - 1)
    
    def willingToChangeDown(self):
        return self.road.possibleLaneChangeDown(self.pos) and self.__willingToChangeLane(self.pos[1], self.pos[1] + 1)

    def __willingToChangeLane(self, sourceLane, destLane):                           
        if self.pos[0] < (self.road.getLength() - 5) and self.pos[0] >= 0:
            srcLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
            destLaneSpeed =  self.road.getMaxSpeedAt( (self.pos[0], destLane) )#gets max speed at destlane
        elif self.pos[0] < self.road.getLength() and self.pos[0] >= (self.road.getLength() - 5):
            srcLaneSpeed =  self.road.d2n( (self.pos[0], sourceLane) )  #gets max speed at sourcelane
            destLaneSpeed =  self.road.d2n( (self.pos[0], destLane) )#gets max speed at destlane        
        if destLaneSpeed <= srcLaneSpeed: return False #no incentive
        prevCar = self.road.findPrevCar( (self.pos[0], destLane) )  #NaSch lane change rule safety
        if prevCar == None: return True #safety check 1
        else:
            distanceToPrevCar = self.pos[0] - prevCar.pos[0] #safety check 2
            return distanceToPrevCar > prevCar.velocity #True only if no collision
           

    
