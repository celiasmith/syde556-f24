import nengo
import numpy as np
model = nengo.Network()
with model:
    stim_food = nengo.Node([0,0])
    food = nengo.Ensemble(n_neurons=200, dimensions=2)
    food.radius = 1.4
    nengo.Connection(stim_food, food)
    
    stim_home = nengo.Node(0)
    home = nengo.Ensemble(n_neurons=100, dimensions=1)
    nengo.Connection(stim_home, home)
    
    motor = nengo.Ensemble(n_neurons=200, dimensions=2,
                           radius=1.4)
    
    position = nengo.Ensemble(n_neurons=2000, dimensions=2,
                              radius=1)
    nengo.Connection(position, position, synapse=0.1)
    nengo.Connection(motor, position, 
                     transform=0.1, synapse=0.1)
    
    nengo.Connection(food, motor)
    nengo.Connection(position, motor, transform=-1)
    
    do_home = nengo.Ensemble(n_neurons=300, dimensions=3,
                             radius=1)
    nengo.Connection(position, do_home[:2])
    nengo.Connection(home, do_home[2], transform=2)
    
    def home_func(x):
        pos_x, pos_y, home = x
        if home > 0:
            return -pos_x, -pos_y
        else:
            return 0, 0
    do_home_fcn = nengo.Ensemble(300, 2)
    nengo.Connection(do_home, do_home_fcn, function=home_func)
    nengo.Connection(do_home_fcn, motor)
    