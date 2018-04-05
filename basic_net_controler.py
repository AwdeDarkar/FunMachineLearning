from controller import Controller
import random
#import numpy as np

def extractInputs(world):
    inputs = []
    for actor in world.actors:
        inputs += actor.pos
        inputs += actor.vel
        inputs += actor.heading
        inputs += int(actor.firing)
        inputs += actor.cooldown
        inputs += actor.hp
    return inputs

class BasicNetController(Controller):

    def __init__(self, net):
        self.net = net
        self.values = net[:]

    def pull(self):
        self.aimpos = self.values[-1][:2]
        self.control = self.valies[-1][2:4]
        self.firing = self.values[-1][5]

     def sync(self, world):
         super().sync(world)
         inputs = extractInputs(world)
         self.values[0] = inputs
         for i in range(1, len(self.net)):
            for j in range(len(self.net[i]) - 1):
                tmp = sum([ self.values[i-1][k]*self.net[i-1][k]
                            for k in range(len(self.values[i])) ]) + \
                            self.values[i][-1]
                self.values[i][j] = sig(tmp)
        
def genRandController(shape):
    net = []
    for s in shape:
        net.append( [ random.random()*2-1 for i in range(s) ] )
    net.append( [ random.random()*2-1 for i in range(5) ] )
    return BasicNetController(net)
