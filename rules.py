import math

PI = math.pi

RULES = {
    "ACTOR" :
    {
        "radius" : 16,
        "max_hp" : 10,
        "max_energy" : 25,
        "start_energy" : 10,
        "energy_regen" : 0.5,
        "cooldown" : 0.2,
        "fire_power" : 1,
        "move_power" : 2000,
        "fire_cost" : 1,
        "move_cost" : 0.01,
        "projectile_speed" : 0.25
    },
    "WORLD" :
    {
        "length" : 800,
        "height" : 600,
        "position_radius" : 100,
        "friction" : 5,
        "floating_point_tolerance" : 2**-16,
        "starting_actors" : 2,
        "projectile_timetolive" : 8
    },
    "GRAPHICS" :
    {
        "actor_sprite_url" : "./actor.png",
        "background_color" : '0xfefefa'
    },
    "CONSOLE":
    {
        "debugging" : True,
        "position" : [0,0],
        "font" : "Consolas",
        "font_size" : 16,
        "line_length" : 20,
        "buffer_length" : 6,
        "color" : '0x000000'
    },
    "TOURNAMENT":
    {
        "batch_size" : 10,
        "max_duration" : 10
    }
}

def bounds_wrapping(obj, pos):
    obj.pos[0] %= RULES["WORLD"]["length"]
    obj.pos[1] %= RULES["WORLD"]["height"]


RULES["WORLD"]["handle_bounds"] = bounds_wrapping

def norm(v):
    return math.sqrt(sum([ x**2 for x in v ]))

def diff(w,v):
    return [ w[i] - v[i] for i in range(0,len(w)) ]

def dist(x,y):
    return norm(diff(x,y))

def vsum(w,v):
    return [ w[0] + v[0], w[1] + v[1] ]

def arg(v):
    return 0

def normalize(v):
    n = norm(v)
    if(n == 0):
        return [0,0]
    return [ v[0]/norm(v), v[1]/norm(v) ]

def dot(w,v):
    return w[0]*w[1] + v[0]*v[1]

def det(w,v):
    return w[0]*v[1] - w[1]*v[0]

def scale(v, a):
    return [a*v[0], a*v[1]]

def toDeg(rad):
    return (rad/(2*PI))*360

def toRad(deg):
    return (deg/360)*2*PI

def snap(vec):
    return [ int(v) for v in vec ]
