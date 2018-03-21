import sys, pygame
from pygame import Color
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
        self.actor_spts = [ ActorSprite(actor, len(world.actors), self.sprite_actor, self.screen) for actor in world.actors ]
        self.projectile_spts = []
        
    def update(self):
        self.screen.fill(self.color)
        
        for actor_sprite in self.actor_spts:
            if(not actor_sprite.actor.aid in self.world.killlist):
                actor_sprite.draw(self.screen)

        for projectile_sprite in self.projectile_spts:
            projectile_sprite.draw(self.screen)

        if(self.console): self.console.draw(self.screen)
        pygame.display.flip()


class ActorSprite:
    def __init__(self, actor, num_actors, sprite, screen):
        self.actor = actor
        self.sprite = sprite.copy()
        screen.blit(self.sprite, self.actor.pos)

    def draw(self, surface):
        sprite = pygame.transform.rotate(self.sprite, toDeg(-self.actor.heading))
        surface.blit(sprite, [ x - 32 for x in self.actor.pos ])

class ProjectileSprite:
    def __init__(self, projectile, screen):
        self.projectile = projectile
        pygame.draw.circle(screen, 0x0, snap(self.projectile.pos), 3)

    def draw(self, surface):
        pygame.draw.circle(surface, 0x0, snap(self.projectile.pos), 3)
