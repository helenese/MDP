import constants, numpy

def frange(x, y, jump):
    while x < y+0.0001:
        yield x
        x = round(x+jump,3)

def binning(state):
    bin_i=round(state[1]/constants.default_sc['waveheight_step'],3)  #binzise wave: 0.4 m, 3 digits after comma
    if bin_i%1==0:         #modulo operator, with this we "catch" the upper bound of the bin, i.e if it is 0.4 this modulo will give 0, then we take the bin_no (1) minus 1, so it lands in the lowest bin, same for other multiples of 0.4
        if bin_i > 0:
            bin_i=int(bin_i)-1
    bin_i=int(bin_i)
    return(bin_i)

def powerprod(windspeed, tc=constants.default_tc): #linearised power curve for the NREL 5MW turbine
    if windspeed >= tc['cut_in'] and windspeed <= tc['v_rated']:
        return(windspeed*(tc['rated_power']/tc['v_rated']))
    elif windspeed > tc['v_rated'] and windspeed < tc['cut_out']:
        return(tc['rated_power'])
    else:
        return(0)

def prodloss(s):  #Calculating the production loss based on the wave bin and weather data
    wavebin=binning(s)
    probabilities=numpy.array(constants.data_correlation[wavebin])
    windspeeds=numpy.array(list(range(len(probabilities))))+1
    power=[]
    for wind in windspeeds:
        power.append(powerprod(wind))
    productionloss=numpy.dot(probabilities,power)
    return(productionloss)

def column_sum(m,c):
    val=0
    for i in m:
        val=val+i[c]
    return(val)

