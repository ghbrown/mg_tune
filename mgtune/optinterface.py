
import pickle


def write_params_file(params_file,type_file,lower_file,upper_file,obj_file,max_f_eval):
    """
    assembles known problem info and settings for NOMAD
    into a plain text file 
    ---Inputs---
    ---Outputs---
    """

    #get data from pickles
    type_list = pickle.load(open(type_file,'rb'))
    lower_bound_list = pickle.load(open(lower_file,'rb'))
    upper_bound_list = pickle.load(open(upper_file,'rb'))

    #convert to single string
    type_string = ' '.join(type_list)
    lower_bound_string = ' '.join(lower_bound_list)
    upper_bound_string = ' '.join(upper_bound_list)

    dimension = len(type_string.split()) #number of decision variables

    lines = []
    lines.append(f'BB_OUTPUT_TYPE OBJ\n')
    lines.append(f'BB_EXE \"$python {obj_file}\"\n\n')
    lines.append(f'DIMENSION {dimension}\n')
    lines.append(f'BB_INPUT_TYPE ( {type_string} )\n')
    lines.append(f'LOWER_BOUND ( {lower_bound_string} )\n')
    lines.append(f'UPPER_BOUND ( {upper_bound_string} )\n\n')
    lines.append(f'LH_SEARCH 1 0\n\n') #use latin hypercube search to set X0
    lines.append(f'MAX_BB_EVAL {max_f_eval}\n\n')
    lines.append(f'DISPLAY_DEGREE 2')

    with open(params_file,'w') as f:
        f.writelines(lines)


def get_parameter_strings(x,options_list,param_types,obj_dir):
    """
    gives the source code snippets corresponding to the current iterate
    ---Inputs---
    x : {list}
        current NOMAD iterate, made of integers and floats
    param_types : {list}
        list of strings corresponding to NOMAD parameters types
        'I' -> integer
        'R' -> real
        'B' -> binary
    options_list : {list}
        list keeping track of all free parameters (those that are inserted with tag)
            and their respective possible values
        len(parameter_options_list) = number of parameters NOMAD is optimizing
            given by string
        len(parameter_options_list[i]) = 2
        parameter_options_list[i] = [ith option name, list of ith argument options (or keywords)]
    obj_dir : {path or string}
        directory which houses the NOMAD objective function
        likely something like .../user_running_dir/mgtune_working/
    ---Outputs---
    parameter_strings : {list}
       list of strings, each corresponding to a parameter option
    """

    parameter_strings = [0]*len(x) #list to hold parameter strings

    for i_p,(x_cur,type_cur) in enumerate(zip(x,param_types)):
        if (type_cur == 'R'):
            print('ERROR: mgtune does not yet support real (non-integer) parameters')
        elif (type_cur == 'B'):
            print('ERROR: mgtune does not yet support binary parameters (though it easily could)')
        elif (type_cur == 'I'):
            parameter_strings[i_p] = str(options_list[i_p][1][x_cur])
    return parameter_strings


def overwrite_tags_with_parameters(tagged_lines,parameter_strings):
    """
    Takes tagged lines and the respective options and creates a
    valid Python source file.
    ---Inputs---
    tagged_lines : {list}
        list of all lines making up the tagged source code of the
        user's solver (all lines included, some tagged)
    parameter_strings : {list}
        list containing strings of source code to insert at each
        corresponding tag point
    ---Outputs---
    running_lines : {list}
        list of lines corresponding to a version of user's
            solver with arguments specified by parameter_strings 
    """

    running_lines = [0]*len(tagged_lines)
    num_tags_found = 0
    tag_string_cur = f'mgtune_tag_{num_tags_found}'
    for i_line,tagged_line in enumerate(tagged_lines):
        cur_line = tagged_lines[i_line]
        found_all_tags_in_line = False
        while (not found_all_tags_in_line): 
            cur_line_split = cur_line.split(tag_string_cur)
            if (len(cur_line_split) == 2):
                #current tag was in line, update cur_line by inserting parameter at split point
                cur_line = cur_line_split[0] + parameter_strings[num_tags_found] + cur_line_split[1]
                num_tags_found += 1
                tag_string_cur = f'mgtune_tag_{num_tags_found}'
            elif (len(cur_line_split) == 1):
                #can't split on current tag (since it's not in line)
                found_all_tags_in_line = True 
                running_lines[i_line] = cur_line
    return running_lines


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
    NONE, writes a file
    """

    #absolute paths of hardcoded files with relevant information
    #these variables should match those in mgtune.ttune.tune
    #limitations of NOMAD IO make it difficult to get around
    #    such hardcoding
    options_file = obj_dir + '/options.p'
    types_file = obj_dir + '/param_types.txt'
    tagged_solver_file = obj_dir + '/tagged_solver.py'
    running_solver_file = obj_dir + '/running_solver.py'


    #get possible options
    options_list = pickle.load(open(options_file,'rb'))
    #options_list is a list of two element lists
    #options_list[i][0] is the parameter's name
    #options_list[i][1] is a list of its possible values (or  bounds if the
    #variable is a float, etc.)

    #extract data type of each option from file
    type_list = pickle.load(open(types_file,'rb'))

    #get lines of tagged version of user's solver
    with open(tagged_solver_file) as f:
        tagged_lines = f.readlines()

    #get source code snippets corresponding to each entry of iterate
    parameter_strings = get_parameter_strings(x,options_list,type_list,obj_dir) 

    #replace tags in source code with respective parameters
    running_lines = overwrite_tags_with_parameters(tagged_lines,parameter_strings)

    #write running solver
    with open(running_solver_file,'w') as f:
        f.writelines(running_lines)
    

def params_file_to_list(params_file):
    #reads a file setting up NOMAD optimization problem
    #and converts to list, each elements of which sets
    #one option
    with open(params_file,'r') as f:
        lines = f.readlines()
    params = [line.strip() for line in lines if not line.isspace()] 
    return params
    

def get_types_and_bounds(parameter_options_list):
    """
    ---Inputs---
    parameter_options_list : {list}
        list keeping track of all free parameters (those that are inserted with tag)
            and their respective possible values
        len(parameter_options_list) = number of free parameters in function call
            given by string
        len(parameter_options_list[i]) = 2
        parameter_options_list[i] = [ith option name, ith argument options (or keywords)]
    ---Outputs---
    types_list : {list}
        list of "types" for each of the decision variables
        I -> integer
        R -> real (float)
        B -> binary
    lower_bounds_list : {list}
        lower bounds for each of the decision variables, numerics plus -inf, +inf
    upper_bounds_list : {list}
        upper bounds for each of the decision variables, numerics plus -inf, +inf
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

    return types_list, lower_bounds_list, upper_bounds_list
