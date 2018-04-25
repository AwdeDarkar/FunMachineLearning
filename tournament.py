from rules import RULES
from random import shuffle
import actor
import controller
import time

def cset(text): a=0
def cprint(text): print(text)

class Tournament:
    def __init__(self, contestants):
        self.contestants = contestants
        shuffle(self.contestants)

    def runGame(self):
        world = actor.World(cprint, cset, RULES)
        world.g_proj = lambda x: 0
        
        tmpa = self.contestants[:RULES["WORLD"]["starting_actors"]]
        tmpb = self.contestants[RULES["WORLD"]["starting_actors"]:]
        controllers = [ contestant.controller for contestant in tmpa ]
        self.controllers = tmpb + tmpa
        
        ttotal = 0
        frame = 0
        while(ttotal < RULES["TOURNAMENT"]["max_duration"] and len(world.actors) > 1):
            t0 = time.time()
            [ c.pull() for c in controllers ]
            [ c.sync(world) for c in controllers ]
            world.update(time.time() - t0)
            ttotal += time.time() - t0
            frame += 1
            print(frame)

        for c in controllers:
            if(c.actor.aid == world.actors[0].aid):
                c.finish(True)

        def run_batch(self):
            #The number of contestants should always be a multple of the number of actors
            num = int(len(self.contestants / RULES["WORLD"]["starting_actors"]))
            for i in range(num):
                self.runGame()

        def full_run(self, num):
            for i in range(num):
                self.runBatch()

            self.contestants.sort(key=lambda c: c.score)
            return self.contestants
        
def headless(thread=0, *clss):
    world = actor.World(cprint, cset, RULES)
    world.g_proj = lambda x: 0
    controllers = []
    i = 0
    ttotal = 0
    check = thread
    frame = 0
    
    for c in clss:
        controllers += [ c[0](a) for a in world.actors[i:i+c[1]] ]
        i += c[1]
        
    running = True
    while running:
        t0 = time.time()
        [ c.pull() for c in controllers ]
        [ c.sync(world) for c in controllers ]
        world.update(time.time() - t0)
        ttotal += time.time() - t0
        check += time.time() - t0
        frame += 1
        if(check > 5):
            print("Frame: {}, Total Time: {} seconds, Living: {}, Avg HP: {}".format(frame, int(ttotal), len(world.actors), world.avgHP()))
            check = 0
        
        if(len(world.actors) == 1):
            running = False
            for c in controllers:
                if(c.actor.aid == world.actors[0].aid):
                    c.finish(True)
                    print(type(c))                    

from ai_controllers import *
