

## `mgtune`

a parameter autotuner for multigrid methods using black box optimization

designed specifically to interface with [PyAMG](https://pyamg.readthedocs.io/en/latest/)

## Workflow

Examples are available in the `examples/` directory, but we provide an overview of the intended user workflow here.

User has linear system (or collection of linear systems) for which they would like to select optimal multigrid parameters.
User also chooses general form of solver (smoothed aggregation, etc.) and writes a simple solve kernel which is to be optimized in a file we'll call `user_solver.py`, which has the form

```python
import pyamg
<other imports>

<other helper functions if needed>

def solve(A,b):
    #must have function with this name and input/output
    #INPUTS: A: square matrix, b: vector
    #OUTPUTS: x: vector
    <custom solver using pyamg and arbitrary Python>
    return x
```

A separate driver script is used to actually define these linear systems and call `mgtune` on user's custom solver

```python
import mgtune

A_list = <list of matrices for which solver should be tuned>
b_list = <corresponding right hand sides>

opt_settings = mgtune.tune(path_to_user_solver,A_list,b_list,path_to_tuned_solver)
```

Note that `path_to_user_solver` **may not contain spaces, a limitation of NOMAD**!

The overall directory sturcture is then

```
some_dir/
  |--user_solver.py
  |--driver.py
```

Other **critical notes**:

- currently, `mgtune` can only optimize certain functions within PyAMG (since support for functions must be added manually), to see what these functions are, call `mgtune.tunable()` in the driver.
- all optional arguments to tunable functions in `user_solver.py` will be considered fixed, conversely, (nearly) all unspecified optinal arguments will be optimized over
- the parameters which cannot optimized (candidate vectors, for example) are omitted because their parameter space is too large, or the parser/writer implementation would be extremely complex (thankfully these cases are rather rare)
- all of this happens by parsing the solver file at `path_to_file_with_solver` and injecting different optional parameters during optimization, so try to keep syntax in this file simple for the best results (ultimately, this should be done by acessing the abstract syntax tree of the user's custom solver functions)


**Major inflexibilities of current parser include**:

- full command names should be used, for example `pyamg.aggregation.smoothed_aggregation_solver` or `ml.solve()`; to get a full printout of the "namespace" of which `mgtune` is aware use `mgtune.tunable()`; in regards to naming in the input solver, the following will result in `mgtune` not detecting any tuning points

```python
import pyamg
from pyamg import smoothed_aggregation_solver
ml = smoothed_aggregation_solver(A)
```

- tunable commands may not be broken over multiple lines (including their options); for example the following is not allowed

```python
ml = pyamg.aggregation.smoothed_aggregation_solver(A,strength='symmetric',
                                                    smooth='jacobi')
```

- tunable commands may not reside in post-source comments; for example, the following is not allowed

```python
ml = pyamg.aggregation.smoothed_aggregation_solver(A) #pyamg.aggregation.smoothed_aggregation_solver
```
    

### Dependencies

`python3` + `numpy` + `pyamg`

[NOMAD: a blackbox optimization software](https://nomad-4-user-guide.readthedocs.io/en/latest/) (which requires Cython)

Setup:

- obtain `python`, `numpy`, `pyamg`, and `cython` (via `pip`, Anaconda, etc.)

- clone NOMAD from [GitHub repo](https://github.com/bbopt/nomad)

- build and install NOMAD according the [instructions](https://nomad-4-user-guide.readthedocs.io/en/latest/Installation.html), be sure to build the Python interface; if using Anaconda, be sure you are in the environment to which you want the Python interface installed when you are building and installing NOMAD

- obtain `mgtune` (suggested to enter project directory and `pip install -e .`, since pip package not yet completed)


### Current status and to do

- current code is likely bug-free, but does not offer usable functionality for actual autotuning
- rather than using NOMAD as the optimization/solver backend, one should look into an alternative (specifically (randomized) coordinate gradient descent with A/B testing of current best config and proposed config, or another standard method for autotuning on integer/discrete variables)




