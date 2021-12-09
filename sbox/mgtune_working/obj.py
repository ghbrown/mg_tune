
from pathlib import Path
import sys
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
    mgtune.optinterface.iterate_to_running_solver(x,obj_dir)

    f = np.sum(np.abs(x))
    
    print(f) #printing value is equivalent to returning it

obj()
