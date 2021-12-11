
from pathlib import Path
import numpy as np
import pyamg
import pyamg.gallery

import mgtune
from mgtune import parsing
from mgtune import function_info


#construct custom dictionary that will limit optimization to a single parameter
n_omega = 30
reduced_dict = {
    "function_name" : 'pyamg.aggregation.smoothed_aggregation_solver',
    "presmoother" : ['(\'jacobi\',{\"withrho\":False,\"omega\":'+str(w)+'})'
                     for w in np.linspace(0.01,1,n_omega)]
    }

print(reduced_dict["presmoother"][0])

#put dictionary in list like mgtune expects
reduced_function_dictionary_list = [reduced_dict]

n = 1000 #matrix dimension
A = pyamg.gallery.poisson((n,),format='csr')  #matrix
b = np.ones((A.shape[0]))                     #right hand side

#put systems in mgtune's expected form
A_list = [A]
b_list = [b]

#build relative path from full path (only since running make from different directory)
#relative paths work if you run python adjacent to driver script
cur_dir = str(Path(__file__).parent)
solver_path = cur_dir + '/sa_solver.py'
tuned_solver_path = cur_dir + '/tuned_solver.py'

#tune solver at location solver_path
mgtune.tune(solver_path,A_list,b_list,tuned_solver_path,
            wfdl=reduced_function_dictionary_list,
            n_trials=40,max_f_eval=100,disp_level=3)

#run timing on original solver versus tuned solver
#mgtune.compare(solver_path,tuned_solver_path,A_list,b_list)



