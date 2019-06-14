import functions, numpy

def downtime(state):
    if state[2]==0:
        return(0)
    else:
        return(-1)

def production(state):
    if state[2]==0:
        return(0)
    else:
        loss=functions.prodloss(state)
        return((-1)*loss)

def repair(state, strat):
    if strat.decision(state)[5]==1:
        return(-1)
    else:
        return(0)

def back(state, strat):
    if strat.decision(state)[4]==1:
        return(-1)
    else:
        return(0)

def out(state, strat):
    if strat.decision(state)[3]==1:
        return(-1)
    else:
        return(0)

def define_vector(states,rewardtype, strat):
    val=[]
    for state in states:
        if rewardtype==downtime or rewardtype==production:
            val.append(rewardtype(state))
        else:
            val.append(rewardtype(state, strat))
    vector=numpy.array(val)
    return(vector)
