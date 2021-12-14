
from pathlib import Path
import numpy as np
import pyamg
import pyamg.gallery

import mgtune

#printout of tunable functions
mgtune.tunable()

#Poisson systems
A_p0 = pyamg.gallery.poisson((1000,))       #smallish 1-D problem
A_p1 = pyamg.gallery.poisson((200,200))  #larger 2-D problem

#linear elasticity
A_l0 = pyamg.gallery.linear_elasticity((40,40))[0] #smallish 1-D problem
A_l1 = pyamg.gallery.linear_elasticity((100,100))[0] #larger 2-D problem

#rotated anisotropic diffusion
r0_stencil = pyamg.gallery.diffusion_stencil_2d(epsilon=100,theta=45)
A_r0 = pyamg.gallery.stencil_grid(r0_stencil,(33,33))
r0_stencil = pyamg.gallery.diffusion_stencil_2d(epsilon=1000,theta=70)
A_r1 = pyamg.gallery.stencil_grid(r0_stencil,(100,100))

#put systems in mgtune's expected form
A_list = [A_p0,A_p1,A_l0,A_l1,A_r0,A_r1]
np.random.seed(seed=4) #set fixed seed for repeatability
b_list = [np.random.rand(A.shape[0]) for A in A_list]

#build relative path from full path (only since running make from different directory)
#relative paths work if you run python adjacent to driver script
cur_dir = str(Path(__file__).parent)
solver_path = cur_dir + '/sa_solver.py'
tuned_solver_path = cur_dir + '/tuned_solver.py'

#tune solver
mgtune.tune(solver_path,A_list,b_list,tuned_solver_path,
            n_trials=1,max_f_eval=250,disp_level=3)

#compare input and tuned solvers on training set
solver_list = [solver_path,tuned_solver_path]
mgtune.compare(solver_list,A_list,b_list,n_trials=5)



