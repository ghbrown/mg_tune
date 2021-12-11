
import time
import numpy as np
import pyamg
import pyamg.gallery
import matplotlib.pyplot as plt

"""
This script solves the same 1-D optimization problem to which
NOMAD is applied in driver.py, but instead simply records the
setup and solve times for every point on a grid of weights.
"""

n = 1000 #matrix dimension
A = pyamg.gallery.poisson((n,),format='csr')  #matrix
b = np.ones((A.shape[0]))                     #right hand side

#timing and optimization variables
n_trials = 40
n_omega = 30
omega_vec = np.linspace(0.01,1,n_omega)
t_vec = np.empty(n_omega)

for i_o,omega in enumerate(omega_vec):
    t_cur = 0 #time accumulator for a single weight
    for trial in range(n_trials): #multiple trials to smooth out timing noise
        t_0 = time.perf_counter()
        ml = pyamg.aggregation.smoothed_aggregation_solver(A,symmetry='hermitian',
                                                           strength=('symmetric',{"theta":0.25}),
                                                           aggregate='standard',smooth='jacobi',
                                                           presmoother=('jacobi',{"withrho":False,
                                                                                  "omega":omega}),
                                                           postsmoother=None,
                                                           improve_candidates=None,
                                                           max_levels=10,max_coarse=10,
                                                           diagonal_dominance=False,keep=False)
        ml.solve(b,x0=None,tol=1e-6,maxiter=100,cycle='V',accel=None,
                 callback=None,residuals=None, return_residuals=False)
        t_1 = time.perf_counter()
        t_cur += (t_1 - t_0)
    t_vec[i_o] = t_cur/n_trials #record average time for current weight

#plot solve time versus omega 
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 20
})
plt.plot(omega_vec,t_vec,'ok')
plt.xlabel(r'weighted Jacobi weight, $\omega$')
plt.ylabel(r'setup and solve time, $t$ [s]')
plt.show()
