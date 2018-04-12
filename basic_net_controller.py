from controller import Controller
import random
import math

import numpy as np
import tensorflow as tf

def sig(x):
    return 1/(1+math.exp(-x))

def extractInputs(world):
    inputs = []
    for actor in world.actors:
        inputs += actor.pos
        inputs += actor.vel
        inputs.append(actor.heading)
        inputs.append(int(actor.firing))
        inputs.append(actor.cooldown)
        inputs.append(actor.hp)
    return inputs

def init_weights(shape):
    """ Weight initialization """
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)

def forwardprop(X, w_1, w_2):
    """
    Forward-propagation.
    IMPORTANT: yhat is not softmax since TensorFlow's softmax_cross_entropy_with_logits() does that internally.
    """
    h    = tf.nn.sigmoid(tf.matmul(X, w_1))  # The \sigma function
    yhat = tf.matmul(h, w_2)  # The \varphi function
    return yhat

def fltToPos(pos):
    return int(pos[0]*150+150), int(pos[1]*150+150)

class BasicNetController(Controller):

    def __init__(self, net, actor):
        Controller.__init__(self, actor)
        self.net = net
        self.values = net[:]
        self.weights = [tf.random_normal((24,1), stddev=0.1), tf.random_normal((4,1), stddev=0.1)]
        self.w1 = init_weights((24, 256))
        self.w2 = init_weights((256, 4))
        self.yhat = [0,0,0,0,0]
        self.pred = [0]*5
        self.X = tf.placeholder("float", shape=[None, 24])

    def pull(self):
        self.aimpos = fltToPos(self.pred[:2])
        self.control = fltToPos(self.pred[2:4])
        t = self.pred[4]
        #print(t)
        if(t <= 0):
            self.firing = False
        else:
            self.firing = True
        

    def sync(self, world):
        super().sync(world)
        inputs = extractInputs(world)
        self.values[0] = inputs
        yhat = forwardprop(self.X, self.w1, self.w2)
        self.pred = [ random.random()*2-1 for i in range(5) ]
        
def genRandController(shape, actor):
    net = []
    for s in shape:
        net.append( [ random.random()*2-1 for i in range(s) ] )
    net.append( [ random.random()*2-1 for i in range(5) ] )
    return BasicNetController(net, actor)
