import pygame
from controller import Controller

class PlayerController(Controller):

    def pull(self):
        self.aimpos = pygame.mouse.get_pos()
        self.control = [0,0]
        if(keyPressed(pygame.K_LEFT)):
            self.control[0] = -1
        if(keyPressed(pygame.K_RIGHT)):
            self.control[0] = 1
        if(keyPressed(pygame.K_DOWN)):
            self.control[1] = 1
        if(keyPressed(pygame.K_UP)):
             self.control[1] = -1
        
    def push(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            self.firing = True
        if(event.type == pygame.MOUSEBUTTONUP):
            self.firing = False
            

def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False
