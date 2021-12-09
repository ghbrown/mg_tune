
import pickle


def write_params_file(params_file,obj_file,type_file,lower_file,upper_file,max_f_eval):
    """
    assembles known problem info and settings for NOMAD
    into a plain text file 
    """

    with open(type_file,'r') as f:
        type_string = f.readlines()[0] #file only has one line

    with open(lower_file,'r') as f:
        lower_bound_string = f.readlines()[0] #file only has one line

    with open(upper_file,'r') as f:
        upper_bound_string = f.readlines()[0] #file only has one line

    dimension = len(type_string.split()) #number of decision variables

    lines = []
    lines.append(f'BB_OUTPUT_TYPE OBJ\n')
    lines.append(f'BB_EXE \"$python {obj_file}\"\n\n')
    lines.append(f'DIMENSION {dimension}\n')
    lines.append(f'BB_INPUT_TYPE ( {type_string} )\n')
    lines.append(f'LOWER_BOUND ( {lower_bound_string} )\n')
    lines.append(f'UPPER_BOUND ( {upper_bound_string} )\n\n')
    lines.append(f'LH_SEARCH 1 1\n\n') #use latin hypercube search to set X0
    lines.append(f'MAX_BB_EVAL {max_f_eval}\n\n')
    lines.append(f'DISPLAY_DEGREE 2')

    with open(params_file,'w') as f:
        f.writelines(lines)


def iterate_to_running_solver(x,obj_dir):
    """
    takes the current NOMAD iterate (a vector of numbers largely
    corresponding to option value indices) and uses them to
    ---Inputs---
    x : {list}
        current NOMAD iterate, made of integers and floats
    obj_dir : {path or string}
        directory which houses the NOMAD objective function
        likely something like .../user_running_dir/mgtune_working/
    ---Outputs---
    """
    options_list = pickle.load(open(obj_dir+'/options.p','rb'))
    print('unpickled successfully')
    #unpickle
    #read option type parameters
    #look at lines in tagged solver file
    #replace tag with option value
    

def params_file_to_list(params_file):
    #reads a file setting up NOMAD optimization problem
    #and converts to list
    with open(params_file,'r') as f:
        lines = f.readlines()
    params = [line.strip() for line in lines if not line.isspace()] 
    return params
    

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
    types_list = [0]*n_params
    lower_bounds_list = [0]*n_params
    upper_bounds_list = [0]*n_params
    for i_o, option_cur in enumerate(parameter_options_list):
        #option_cur looks like [option_name, [option_1, option_2,...]]
        options = option_cur[1]
        if isinstance(options,list):
                if ((isinstance(options[0],str)) and ('unbounded' in options[0])):
                    print('ERROR: parameters which belong to set of unbounded size not yet implemented')
                else:
                    types_list[i_o] = 'I' #if variable from set of bounded size, must be integer
                    lower_bounds_list[i_o] = 0
                    upper_bounds_list[i_o] = int(len(options) - 1)

    #numerics -> strings
    types_list = [str(elem) for elem in types_list]
    lower_bounds_list = [str(elem) for elem in lower_bounds_list]
    upper_bounds_list = [str(elem) for elem in upper_bounds_list]

    types_line = ' '.join(types_list)
    with open(type_file,'w') as f:
        f.writelines([types_line])

    lower_bounds_line = ' '.join(lower_bounds_list)
    with open(lower_file,'w') as f:
        f.writelines([lower_bounds_line])

    upper_bounds_line = ' '.join(upper_bounds_list)
    with open(upper_file,'w') as f:
        f.writelines([upper_bounds_line])
