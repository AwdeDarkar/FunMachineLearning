import pygame
import rules
from rules import RULES
import actor
import graphics
import controller
import console
import player_controller #wrap this stuff up probably
import basic_net_controller
import sys
import traceback
import time

running = True
try:
    pygame.init()
    console = console.Console(RULES["CONSOLE"])
    console.cprint("Starting")
    world = actor.World(console.cprint, console.cset, RULES)
    display = graphics.Display(RULES["GRAPHICS"], world, console)

    def graphics_create_projectile(projectile):
        p = graphics.ProjectileSprite(projectile, display.screen)
        display.projectile_spts.append(p)
    
    world.g_proj = graphics_create_projectile
    controllers = [ basic_net_controller.genRandController([8,5,8], a) for a in world.actors[1:] ]
    controllers.append(player_controller.PlayerController(world.actors[0]))
except:
    traceback.print_exc()
    running = False
while running:
    t0 = time.time()
    [ c.pull() for c in controllers ]
    console.cset("{0:.3f}π".format(world.actors[0].heading/rules.PI))
    console.cset("Power: {0:.3f}     Health: {1:.1f}".format(world.actors[0].eng, world.actors[0].hp), 1 )
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        else: controllers[-1].push(event)
    try:
        [ c.sync(world) for c in controllers ]
        display.update()
        world.update(time.time() - t0)
        if(len(world.actors) == 1):
            running = False
            for c in controllers:
                if(c.actor.aid == world.actors[0].aid):
                    c.finish(True)
    except:
        traceback.print_exc()
        running = False

pygame.quit()
sys.exit()
