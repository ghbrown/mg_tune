
import sys
from pathlib import Path
import time
import pickle
import numpy as np
import mgtune
from mgtune import optinterface

def obj():
    #mgtune objective functions
    #returns the time taken to solve all linear systems
    #with the current iterate of the solver

    obj_dir = str(Path(__file__).parent) #directory containing objective function

    x_file_name = sys.argv[1]
    with open(x_file_name,'r') as f:
        line = f.readlines()[0]

    x_strings = line.split()
    x = [int(elem) for elem in x_strings]


    #use current NOMAD iterate to write a new solver to be evaluated
    mgtune.optinterface.iterate_to_running_solver(x,obj_dir)

    #import newly written solver
    import running_solver #need to make sure not cached so changes take effect

    #get linear systems from pickle
    A_list = pickle.load(open(obj_dir+'/A_list.p','rb'))
    b_list = pickle.load(open(obj_dir+'/b_list.p','rb'))

    #get number of trials for each solver from pickle
    n_trials = pickle.load(open(obj_dir+'/n_trials.p','rb'))

    t = 0 #time to solve all systems in users "training set"
    for A,b in zip(A_list,b_list):
        t_cur_system = 0 #accumulator for current system
        for trial in range(n_trials):
            t_0 = time.perf_counter()
            running_solver.solve(A,b)
            t_1 = time.perf_counter()
            t_cur_system += (t_1 - t_0)
        t += t_cur_system/n_trials #accumulate average time

    #delete running solver from cached modules after using
    #so it is loaded fresh on next objective function run
    try:
        del sys.modules['running_solver']
    except (AttributeError):
        pass
    
    f = t #objective function is total time

    print(f) #return value to NOMAD by printing

obj()
