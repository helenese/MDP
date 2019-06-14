import numpy, copy, reward, constants, Strategy, functions, solving, sys
sys.stdout=open("applog.txt", "w")


for month in range(1,13):
    path_transition='Weather/Markov/Markov_'+str(month)+'.txt' #insert path to the transition probabilities for waves 
    data=numpy.genfromtxt(path_transition,comments="#", delimiter="\t", unpack=False)
    path_waveheight='Weather/Markov/Waveheight_'+str(month)+'.txt'
    data1 =numpy.genfromtxt(path_waveheight, comments='#', delimiter='\t', unpack=False)
    locations=['port', 'turbine']
    waveheight=list(functions.frange(0.4,(len(data))*0.4,0.4))
    repairtime=list(range(constants.default_sc['repairtime_max_plus1']))
    wait=[0,1,2,3]

    a = [copy.deepcopy(locations), waveheight, repairtime, wait] 

    poss_states=[[]]
    for x in a:
        t = []
        for y in x:
            for i in poss_states:
                t.append(i+[y])
        poss_states = t


    strategies=[
        Strategy.AioStrategy(0, 1.6, "simple"),
        Strategy.AioStrategy(1, 1.6, "wait1"),
        Strategy.AioStrategy(2, 1.6, "wait2"),
        Strategy.AioStrategy(3, 1.6, "wait3"),
        Strategy.AioStrategy(0, 2.0, "2m"),
        Strategy.AioStrategy(0, 2.4, "2.4m"),
        Strategy.AioStrategy(0, 2.8, "2.8m"),
        Strategy.AioStrategy(0, 1.2, "1.2m"),
        Strategy.AioStrategy(0, 0.8, "0.8m"),
        Strategy.AioStrategy(0, 1.6, "1.6m")
        ]


    reward_types=[reward.downtime, reward.production, reward.repair, reward.back, reward.out]


    for strat in strategies:
        states=strat.valid_states(poss_states)
        result=[]
        for rew in reward_types:
            e=solving.evaluation(strat, rew, states, data, data1)
            result.append(e)
        print("Strategy %s has an expected downtime of %s [h], and expected production losses of %s [Wh]. With %s expected vessel accesses, %s expected repair actions and %s expected vessel returns" % (strat, result[0], result[1], result[4], result[2], result[3]))#, result[4], result[2], result[3]))
        rtmax=constants.default_sc['repairtime_max_plus1']
        file = open('results_timing.txt', 'a')
        file.write('\t'.join([str(month),str(rtmax), str(strat), str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4])])+'\r\n')
        file.close()

