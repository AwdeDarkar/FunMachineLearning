import pygame

class Console:
    def __init__(self, rules):
        self.rules = rules
        self.buffer = []

        pygame.font.init()
        self.font = pygame.font.SysFont(rules["font"], rules["font_size"])
        self.buffer.append("Hi")
        

    def cprint(self, text):
        self.buffer.append(text)
        if(len(self.buffer) > self.rules["buffer_length"]):
            self.buffer = self.buffer[1:]

    def cset(self, text, line=0):
        self.buffer[line] = text

    def draw(self, surface):
        pos = self.rules["position"][:]
        
        for line in self.buffer:
            text = self.font.render(line, True, toRGB(self.rules["color"]))
            surface.blit(text, pos)
            pos[1] += self.rules["line_length"]
            
def toRGB(hexstr):
    x = int(hexstr, 16)
    r = x >> (16)
    g = (x - (r << (16))) >> (8)
    b = (x - (r << (16)) - (g << (8)))
    return r, g, b
