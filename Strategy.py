import constants, functions, numpy, copy

class AioStrategy():
    def __init__(self, wlim, softlim, name):
        self.wlim=wlim
        self.softlim=softlim
        self.name=name
    def __str__(self):
        return(self.name)
    def decision(self, prev, hslim=constants.default_sc['wavelimit']):
        out=0
        back=0
        repair=0
        if prev[2]==0:
            loc=prev[0]
            rt=prev[2]
            wt=prev[3]
        elif prev[2]>0:
            if prev[0]=='turbine':
                if prev[3]!=0:
                    loc=prev[0]
                    rt=prev[2]
                    wt=prev[3]
                elif prev[1]>=hslim:
                    loc='port'
                    rt=prev[2]
                    wt=prev[3]
                    back=1
                elif prev[1]<hslim:
                    loc=prev[0]
                    rt=prev[2]-1
                    wt=prev[3]
                    repair=1
            elif prev[0]=='port':
                if prev[1]>=self.softlim:
                    loc=prev[0]
                    rt=prev[2]
                    wt=0
                elif prev[1]<self.softlim:
                    if prev[3]==self.wlim:
                        loc='turbine'
                        rt=prev[2]
                        wt=0
                        out=1
                    elif prev[3]<self.wlim:
                        loc='port'
                        rt=prev[2]
                        wt=prev[3]+1
                    elif prev[3]>self.wlim:
                        loc=prev[0]
                        rt=prev[2]
                        wt=prev[3]
        val=[loc, rt, wt, out, back, repair]
        return(val)
    def define_matrix(self, states, data):
        matrix=[None]*len(states)
        for j in range(len(states)):
            matrix[j]=[0]*len(states)
            desc=self.decision(states[j])
            for i in range(len(states)): # i=0,...(numberstates-1)
                if states[i][0]==desc[0] and states[i][2]==desc[1] and states[i][3]==desc[2]:
                    if i==j:
                        matrix[j][i]=data[functions.binning(states[j])][functions.binning(states[i])]-1
                    elif i!=j:
                        matrix[j][i]=data[functions.binning(states[j])][functions.binning(states[i])]
                elif i==j:
                    matrix[j][i]=-1
        output=numpy.array(matrix)
        return(output)
    def valid_states(self, poss_states):
        states=copy.deepcopy(poss_states)
        invalids=[]
        for state in states:
            if state[3]>self.wlim:
                i=states.index(state)
                invalids.append(i)
            elif state[0]=='turbine' and state[3]!=0:
                i=states.index(state)
                invalids.append(i)
            elif state[2]==0:
                i=states.index(state)
                invalids.append(i)
        invalids.sort(reverse=True)
        for i in invalids:
            del states[i]
        return(states)

