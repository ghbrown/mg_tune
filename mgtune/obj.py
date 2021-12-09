
from pathlib import Path
import sys
import time
import pickle
import numpy as np
import mgtune
from mgtune import optinterface

def obj():
    x_file_name = sys.argv[1]
    with open(x_file_name,'r') as f:
        line = f.readlines()[0]

    x_strings = line.split()

    x = [int(elem) for elem in x_strings]
    obj_dir = str(Path(__file__).parent) #directory containing objective function
    A_list = pickle.load(open(obj_dir+'/A_list.p','rb'))
    b_list = pickle.load(open(obj_dir+'/b_list.p','rb'))
    #import running_solver

    """
    t = 0
    for A,b in zip(A_list,b_list):
        t_0 = time.perf_counter()
        running_solver.solve(A,b)
        t_1 = time.perf_counter()
        t += (t_1 - t_0)
    """
    
    mgtune.optinterface.iterate_to_running_solver(x,obj_dir)

    f = np.sum(np.abs(x))
    
    print(f) #printing value is equivalent to returning it

obj()
