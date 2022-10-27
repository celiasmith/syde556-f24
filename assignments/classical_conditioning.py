#Setup the environment
import numpy as np
import nengo
from nengo.processes import WhiteSignal

model = nengo.Network(label='Learning', seed=8)
with model:
    #Ensembles to represent populations
    US = nengo.Ensemble(50, dimensions=1)
    CS = nengo.Ensemble(50, dimensions=1)
    error = nengo.Ensemble(100, dimensions=1)
    UR = nengo.Ensemble(100, dimensions=1)
    CR = nengo.Ensemble(50, dimensions=1)
    response = nengo.Ensemble(50, dimensions=1)
    
    #Error = pre - post
    #Communication Channel
    nengo.Connection(UR, error, transform=-1, synapse=0.02)
    nengo.Connection(CR, error, transform=1, synapse=0.02)
    
    #Connecting pre population to post population (communication channel)
    conn = nengo.Connection(CS, CR, function=lambda x: 0,
                            solver=nengo.solvers.LstsqL2(weights=True))
    
    #Adding the learning rule to the connection 
    #Adjust learning rate to change extinction and learning speed
    conn.learning_rule_type = nengo.PES(learning_rate=5e-5)
    #Error connections don't impart current
    error_conn = nengo.Connection(error, conn.learning_rule)
    
    nengo.Connection (US, UR, synapse=0.02)
    nengo.Connection (UR, response, synapse=0.02)
    nengo.Connection (CR, response, synapse=0.02)
    
    def CS_fcn(t):
        if t%1 < .5: x = 1
        else: x = 0
        return x
    
    def US_fcn(t):
        x = 0
        if t>1.5 and t <5:
            if t%1 < .5: x = 1
            else: x = 0
        return x
        
    #Providing input to the model
    US_input = nengo.Node(US_fcn)
    CS_input = nengo.Node(CS_fcn)

    # Connecting input to the pre ensemble
    
    nengo.Connection(CS_input, CS, synapse=0.02)  
    nengo.Connection(US_input, US, synapse=0.02)  
    
                                                
                                                