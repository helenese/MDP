import reward, constants, numpy, functions
from scipy.sparse.linalg import spsolve

def equationsystem(matrix, vector):
    val=numpy.linalg.solve(matrix, vector)
    return(val)

def position_starting(states):
    pos=[]
    for i in range(len(states)):
        if states[i][0]=='port' and states[i][2]==constants.default_sc['repairtime_max_plus1']-1 and states[i][3]==0:
            pos.append(i)
    return(pos)


def probability_wave(state, data):
    val=data[functions.binning(state)]
    return(val)
    
    
def evaluation(strat, rewardtype, states, data, data1):
    m=strat.define_matrix(states,data)
    v=reward.define_vector(states,rewardtype, strat)
    les=equationsystem(m, v)
    pos=position_starting(states)
    val=0
    for i in pos:
        val=val+les[i]*probability_wave(states[i],data1)
    return(val)
