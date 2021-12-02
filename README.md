

## `mgtune`

a parameter autotuner for multigrid methods using black box optimization

designed specifically to interface with [PyAMG](https://pyamg.readthedocs.io/en/latest/)

## Workflow

User has a linear system (or a collection of linear systems) for which they would like to select optimal multigrid parameters.

The file at location given by `driver.py` defines your linear systems, and makes a call of the form

```python
opt_settings = mgtune.tune(path_to_file_with_solver,A_list,b_list)
```

The file at location specified by `path_to_file_with_solver` has the rough form

```python
import pyamg
<other imports>

<other helper functions>

def solver(A,b):
    #must have function with this name and input/output
    #INPUTS: A: matrix, b: vector
    #OUTPUTS: x: vector
    <custom solver using pyamg and arbitrary Python>
    return x
```

with a few **critical notes**:

- currently, `mgtune` can only optimize certain functions within PyAMG (since support for functions must be added manually) 
- all specified optional arguments to such functions will be considered fixed, conversely, (nearly) all unspecified optinal arguments will be optimized over
- the parameters which are not optimized (candidate vectors, for example) are omitted because their parameter space is too large, or the parser/writer implementation would be extremely complex (thankfully these cases are rather rare)
- all of this happens by parsing the solver file at `path_to_file_with_solver` and injecting different optional parameters during optimization, so try to keep syntax in this file simple for the best results (ultimately, this should be done by acessing the abstract syntax tree of the user's custom solver functions)


**Major inflexibilities of current parser include**:

    - full command names should be used, for example `pyamg.aggregation.smoothed_aggregation_solver`; for example, the following is not allowed

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

    - tunable commands may be not resided in post-source comments; for example, the following is not allowed

    ```python
    ml = pyamg.aggregation.smoothed_aggregation_solver(A) #pyamg.aggregation.smoothed_aggregation_solver
    ```
    

### Dependencies

`python3` + `numpy` + `pyamg`

[NOMAD: a blackbox optimization software](https://nomad-4-user-guide.readthedocs.io/en/latest/)


