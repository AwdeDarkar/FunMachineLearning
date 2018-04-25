import sys, pygame
from pygame import Color
import colorsys
import rules
from rules import *

class Display:
    def __init__(self, grules, world, console=None):
        self.grules = grules
        self.length = world.length
        self.height = world.height
        self.world = world
        self.console = console
        self.screen = pygame.display.set_mode((self.length, self.height))
        self.color = Color(grules["background_color"])
        
        self.screen.fill(self.color)
        
        
        self.sprite_actor = pygame.image.load(self.grules["actor_sprite_url"])
        self.sprite_actor = self.sprite_actor.convert_alpha()
        colors = calculateColors(len(world.actors))
        self.actor_spts = [ ActorSprite(actor, len(world.actors), self.sprite_actor,
                                        self.screen, colors[actor.aid], 16) for actor in world.actors ]
        self.projectile_spts = []
        
    def update(self):
        self.screen.fill(self.color)
        
        for actor_sprite in self.actor_spts:
            if(not actor_sprite.actor.aid in self.world.killlist):
                actor_sprite.draw(self.screen)

        for projectile_sprite in self.projectile_spts:
            if(projectile_sprite.projectile.pid in self.world.plive):
                projectile_sprite.draw(self.screen)

        if(self.console): self.console.draw(self.screen)
        pygame.display.flip()


def calculateColors(num):
    colors = []
    for i in range(0, num):
        colors.append( toInt(colorsys.hsv_to_rgb(i/num, 0.8, 0.8)) )
    return colors

def toInt(rgb):
    r, g, b = rgb
    v = 0
    v += int(r*255)
    v = v << 8
    v += int(g*255)
    v = v << 8
    v += int(b*255)
    return v

class ActorSprite:
    def __init__(self, actor, num_actors, sprite, screen, color, radius):
        self.actor = actor
        self.sprite = sprite.copy()
        screen.blit(self.sprite, self.actor.pos)
        self.color = color
        self.radius = radius

    def draw(self, surface):
        sprite = pygame.transform.rotate(self.sprite, toDeg(-self.actor.heading))
        pygame.draw.circle(surface, self.color, snap(self.actor.pos), self.radius)
        surface.blit(sprite, [ x - self.radius*2 for x in self.actor.pos ])

class ProjectileSprite:
    def __init__(self, projectile, screen):
        self.projectile = projectile
        pygame.draw.circle(screen, 0x0, snap(self.projectile.pos), 3)

    def draw(self, surface):
        pygame.draw.circle(surface, 0x0, snap(self.projectile.pos), 3)
