import actor
from rules import *
import math

class Controller:

    def __init__(self, actor):
        self.actor = actor
        self.aimpos = [0,0]
        self.firing = False
        self.alive = True
        self.control = [0,0]

    def heading(self):
        dvect = diff(self.aimpos, self.actor.pos)
        #dvect[0] /= norm(dvect)
        #dvect[1] /= norm(dvect)
        h = math.atan2(dvect[1],dvect[0])
        self.actor.heading = h
        return h

    def pull(self):
        a = 0 #No-op

    def sync(self, world):
        if(self.alive):
            self.actor.set_move(self.control)
            self.actor.firing = self.firing
            self.actor.heading = self.heading()
            if(not self.actor in world.actors):
                self.finish(False)
                self.alive = False

    def score(self, world):
        mean = sum([ a.hp for a in world.actors])/world.rules["starting_actors"]
        return self.actor.hp - mean 

    def finish(self, win):
        print("{} victory condition: {}".format(self.actor.aid, win))
        
