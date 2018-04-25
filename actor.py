import math
import random
from rules import *

class Actor:
    def __init__(self, aid, pos, heading, arules):
        self.aid = aid
        self.pos = pos
        self.heading = heading
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.firing = False
        self.cooldown = 0
        self.quitting = False
        self.alive = True

        self.fire_power = arules["fire_power"]
        self.move_power = arules["move_power"]
        self.fire_cost = arules["fire_cost"]
        self.move_cost = arules["move_cost"]
        self.hit_radius = arules["radius"]
        self.projectile_speed = arules["projectile_speed"]
        self.eng = arules["start_energy"]
        self.engmx = arules["max_energy"]
        self.engrt = arules["energy_regen"]
        self.cooldown_time = arules["cooldown"]
        self.hp = arules["max_hp"]

        self.aimpos = [0,0]

    def handle_cost(self, cost):
        if(cost > self.eng):
            return False
        self.eng -= cost
        return True
    
    def set_move(self, control): #control can be -1, 0, or 1
        wt = norm(control)
        if(wt != 0 and self.handle_cost(self.move_cost*wt)):
            self.acc[0] = control[0]*self.move_power/wt
            self.acc[1] = control[1]*self.move_power/wt
        else:
            self.acc = [0,0]

    def update(self, dt, prj_handler, wrules):
        if(self.firing and self.cooldown <= 0 and self.handle_cost(self.fire_cost)):
            prj_handler.create_projectile(self.aid, self.pos[:], self.vel[:],
                                            self.heading, self.fire_power,
                                            self.projectile_speed)
            self.cooldown = self.cooldown_time
            
        not_moving = 1
        if(norm(self.acc) != 0):
            not_moving = 0

        hvec = diff(self.pos, self.aimpos)
        
        self.cooldown -= dt
        self.pos[0] += self.vel[0]*dt
        self.pos[1] += self.vel[1]*dt
        self.vel[0] += self.acc[0]*dt - not_moving*wrules["friction"]*self.vel[0]*dt
        self.vel[1] += self.acc[1]*dt - not_moving*wrules["friction"]*self.vel[1]*dt
        self.eng = min(self.eng+self.engrt*dt, self.engmx)
        wrules["handle_bounds"](self, self.pos)
        
class Projectile:
    def __init__(self, aid, pos, vel, power, heading, ttl=10):
        self.aid = aid
        self.pid = aid*1000+random.randint(0,999)
        self.pos = pos
        self.ttl = ttl
        self.heading = heading
        self.vel = vel
        self.power = power

    def update(self, dt, wrules):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.ttl -= dt
        wrules["handle_bounds"](self, self.pos)

def calculatePositions(num, rad, center):
    dtheta = 2*math.pi/num
    positions = []
    for i in range(0, num):
        positions.append([rad*math.cos(dtheta*i)+center[0],
                          rad*math.sin(dtheta*i)+center[1]])
    return positions

class World:
    def __init__(self, cprint, cset, rules):
        self.wrules = rules["WORLD"]
        self.length = self.wrules["length"]
        self.height = self.wrules["height"]
        self.actors = []
        self.projectiles = []
        self.cprint = cprint
        self.cset = cset
        self.killlist = []
        self.plive = []
        self.display = None

        actor_pos = calculatePositions(self.wrules["starting_actors"],
                                       self.wrules["position_radius"],
                                       (self.length/2, self.height/2))
        for i in range(0,len(actor_pos)):
            pos = actor_pos[i]
            self.actors.append(Actor(i, pos, math.atan(pos[1]/pos[0]), rules["ACTOR"]))

    def create_projectile(self, aid, pos, vel, heading, fire_power, projectile_speed):
        vel[0] = projectile_speed*math.cos(heading)
        vel[1] = projectile_speed*math.sin(heading)
        proj = Projectile(aid, pos, vel, fire_power, heading, self.wrules["projectile_timetolive"])
        self.projectiles.append(proj)
        self.plive.append(proj.pid)
        self.g_proj(proj)
        
    def avgHP(self):
        return sum([ actor.hp for actor in self.actors ])/len(self.actors)
    
    def update(self, dt):
        for actor in self.actors:
            actor.update(dt, self, self.wrules)

        delete_list_prj = []
        delete_list_act = []
        for projectile in self.projectiles:
            projectile.update(dt, self.wrules)
            if(projectile.ttl < 0):
                self.plive.remove(projectile.pid)
                delete_list_prj.append(projectile)
            for actor in self.actors:
                if(actor.aid != projectile.aid and norm(diff(projectile.pos, actor.pos)) < actor.hit_radius):
                    delete_list_prj.append(projectile)
                    self.plive.remove(projectile.pid)
                    actor.hp -= projectile.power
                    if(actor.hp <= 0):
                        delete_list_act.append(actor)
                        self.killlist.append(actor.aid)
                        self.cprint("Kill!")

        for actor in delete_list_act:
            self.actors.remove(actor)
        for projectile in delete_list_prj:
            self.projectiles.remove(projectile)
                    
