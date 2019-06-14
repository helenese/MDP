import numpy

default_sc={
    'waveheight_max':10.4,
    'waveheight_step':0.4,
    'repairtime_max_plus1':232, #22, 6
    'repairtime_step':1,
    'wavelimit':1.6,
    'vessel_charter': 2300
    }

default_tc={
    'cut_in':3,
    'cut_out':25,
    'v_rated':11.4,
    'rated_power':5000 #kW
    }


path_correlation='Weather/Markov/wind_distr.txt'
data_correlation=numpy.genfromtxt(path_correlation,comments="#", delimiter="\t", unpack=False)  #26(zeilen)x33(spalten)
