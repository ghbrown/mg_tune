
def write_types_and_bounds(parameter_options_list,type_file,lower_file,upper_file):
    """
    ---Inputs---
    parameter_options_list : {list}
        list keeping track of all free parameters (those that are inserted with tag)
            and their respective possible values
        len(parameter_options_list) = number of free parameters in function call
            given by string
        len(parameter_options_list[i]) = 2
        parameter_options_list[i] = [ith option name, ith argument options (or keywords)]
    type_file : {path or string}
        file where parameter types (int, real, etc.) will be written
    lower_file : {path or string}
        file where lower bounds will be written
    upper_file : {path or string}
        file where upper bounds will be written
    ---Outputs---
    NONE, writes to three files
    """
    n_params = len(parameter_options_list) #get number of free parameters
    type_list = [0]*n_params
    lower_bound_list = [0]*n_params
    upper_bound_list = [0]*n_params
    for i_o, options_cur in enumerate(parameter_options_list):
        if isinstance(options_cur,list):
            if ('unbounded' in options_cur[0]):
                print('ERROR: parameters which belong to set of unbounded size not yet implemented')
            else:
                type_list[i_o] = 'I' #if variable from set of bounded size, must be integer
                lower_bound_list[i_o] = 0
                upper_bound_list[i_o] = int(len(options_cur) - 1)

    #numerics -> strings
    type_list = [str[elem] for elem in type_list]
    lower_bounds_list = [str[elem] for elem in lower_bounds_list]
    upper_bounds_list = [str[elem] for elem in upper_bounds_list]

    type_line = ' '.join(type_list)
    with open(type_file,'w') as f:
        f.write_line(type_line)

    lower_bounds_line = ' '.join(lower_bounds_list)
    with open(type_file,'w') as f:
        f.write_line(lower_bounds_line)

    upper_bounds_line = ' '.join(upper_bounds_list)
    with open(type_file,'w') as f:
        f.write_line(upper_bounds_line)
