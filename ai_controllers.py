from controller import Controller
import math
import random
from rules import *

class AimBot(Controller):
    def __init__(self, actor):
        Controller.__init__(self, actor)
        self.actor = actor
        self.target = (0,0)

    def selectTarget(self, world):
        self.target = (0,0)
        bestHP = 0
        for actor in world.actors:
            if actor.hp > bestHP and actor != self.actor:
                bestHP = actor.hp
                self.target = actor.pos

    def pull(self):
        self.aimpos = self.target
        self.control = [0,0]
        self.firing = True

    def sync(self, world):
        super().sync(world)
        self.selectTarget(world)

class DodgeBot(Controller):

    def __init__(self, actor):
        Controller.__init__(self, actor)
        self.actor = actor

    def dodgeProj(self, proj):
        vec = scale(diff(diff(self.actor.pos,proj.pos),proj.vel), 
                    1/(dist(self.actor.pos,proj.pos)+1))
        self.control = vsum(self.control, vec)

    def pull(self):
        self.control = normalize(self.control)
        
    def sync(self, world):
        super().sync(world)
        self.control = [0,0]
        for proj in world.projectiles:
            if(dist(self.actor.pos, proj.pos) < 50):
                self.dodgeProj(proj)
        self.control = normalize(self.control)

class DodgeAimBot(Controller):
    def __init__(self, actor):
        Controller.__init__(self, actor)
        self.actor = actor
        self.target = (0,0)

    def dodgeProj(self, proj):
        vec = scale(diff(diff(self.actor.pos,proj.pos),proj.vel), 
                    1/(dist(self.actor.pos,proj.pos)+1))
        self.control = vsum(self.control, vec)

    def selectTarget(self, world):
        self.target = (0,0)
        bestHP = 0
        for actor in world.actors:
            if actor.hp > bestHP and actor != self.actor:
                bestHP = actor.hp
                self.target = actor.pos

    def pull(self):
        self.control = normalize(self.control)
        self.aimpos = self.target
        self.firing = True
        
    def sync(self, world):
        super().sync(world)
        self.control = [0,0]
        self.selectTarget(world)
        for proj in world.projectiles:
            if(proj.aid != self.actor.aid and
               dist(self.actor.pos, proj.pos) < 50):
                self.dodgeProj(proj)

class ConserveBot(DodgeAimBot):
    def pull(self):
        self.control = normalize(self.control)
        self.aimpos = self.target
        self.firing = (self.actor.eng > self.actor.fire_power*2)

class VolleyBot(DodgeBot):
    def __init__(self, actor):
        DodgeBot.__init__(self, actor)
        self.volley = False

    def pull(self):
        if(self.volley):
            if(self.actor.eng < 1):
                self.volley = False
                self.firing = False
            else:
                self.control = normalize(self.control)
                self.firing = True
                self.aimpos = [random.randint(0, 1000), random.randint(0, 1000)]
        else:
            self.control = normalize(self.control)
            if(self.actor.eng > 20 and random.random() < 0.05):
                self.volley = True
