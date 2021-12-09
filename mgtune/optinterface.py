
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

    options_file = obj_dir + '/options.p'
    types_file = obj_dir + '/param_types.txt'
    tagged_solver_file = obj_dir + '/tagged_solver.py'
    running_solver_file = obj_dir + '/running_solver.py'

    #options_list is a list of two element lists
    #options_list[i][0] is the parameter's name
    #options_list[i][1] is a list of its possible values (or  bounds if the
    #variable is a float, etc.)
    options_list = pickle.load(open(options_file,'rb'))

    with open(types_file,'r') as f:
        line = f.readlines()[0] #only one line file
    type_list = line.split()

    #determine parameters that correspond to x
    parameter_strings = [0]*len(x) #list to hold parameter strings

    for i_p,(x_cur,type_cur) in enumerate(zip(x,type_list)):
        if (type_cur == 'R'):
            print('ERROR: mgtune does not yet support real (non-integer) parameters')
        elif (type_cur == 'B'):
            print('ERROR: mgtune does not yet support binary parameters (though it easily could)')
        elif (type_cur == 'I'):
            parameter_strings[i_p] = str(options_list[i_p][1][x_cur])

    #write parameters that correspond to x into the tagged
    #solver to create running solver
    with open(tagged_solver_file) as f:
        tagged_lines = f.readlines()
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

    with open(obj_dir+'/nomad_obj_debug.txt','w') as f:
        f.writelines(running_lines)
        #f.writelines([' '.join(parameter_strings)])
    

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
