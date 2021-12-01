

## `mgtune`

a parameter autotuner for multigrid methods using black box optimization

designed specifically to interface with [PyAMG](https://pyamg.readthedocs.io/en/latest/)

## Workflow

User has a linear system (or a collection of linear systems) for which they would like to select optimal multigrid parameters.

The file `driver.py` defines your linear systems, and makes a call of the form

```python
opt_settings = mgtune.tune(path_to_file_with_solver,A_list,b_list)
```

The file `solver.py` has the rough form

```python
import pyamg

def solver(A,b,<set desired optional argument>):
    #function name can be nearly arbitrary
    <construct your own solver using pyamg and arbitrary Python>
    return x
```

with a few critical notes:

- full command names should be used, for example `pyamg.aggregation.smoothed_aggregation_solver`
- all specified optional arguments will be considered fixed, conversely, (nearly) all unspecified optinal arguments will be optimized over
- currently, `mgtune` can only optimize certain functions within PyAMG (since support for functions must be added manually) 
- all of this happens by parsing the solver file at `path_to_file_with_solver`, and rewriting it with different optional parameters during optimization so try to keep things simple for the best results
- the parameters which are not optimized (candidate vectors, for example) are omitted because their parameter space is too large, or the parser/writer implementation would be extremely complex; thankfully these cases are rather rare


### Dependencies

Python + `numpy` + `pyamg`

[NOMAD: a blackbox optimization software](https://nomad-4-user-guide.readthedocs.io/en/latest/)


