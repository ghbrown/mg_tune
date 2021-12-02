
import os
import copy

    
#THE RIGHT WAY TO DO THIS IS BY ACCESSING ABSTRACT SYNTAX TREES,
#BUT NOT COMFORTABLE WITH THAT RIGHT NOW

def locate_function_parentheses(string,start=0):
    #TODO: full doc string
    #given a string like
    # z = my_fun(a,b,c,d=(1,2,3))
    #     *     ^               ^
    #we seek the indices of the parentheses indicated by ^,
    #the first matching () set after index of start (*)

    open_paren_loc = string[start:].find('(') + start #index of first parentheses IN STRING
    num_open_parens = 1
    for i in range(open_paren_loc+1,len(string)):
        if (string[i] ==  '('):
            num_open_parens += 1
        elif (string[i] == ')'):
            num_open_parens -= 1
        if (num_open_parens == 0):
            close_paren_loc = i #found matching parentheses
            break

    return (open_paren_loc, close_paren_loc)


def is_viable_line(string):
    #TODO: full doc string
    #False if string is empty line or comment, True otherwise
    string_no_newline_spaces = ''.join(string.strip().split())
    if (len(string_no_newline_spaces) == 0): 
        return False #is an empty line
    elif (string_no_newline_spaces[0] == '#'):
        return False #is an inline comment
    else:
        return True
    

def mark_functions(file_name,marked_file_name,fdl):
    """
    finds and marks location of functions which may be edited
    ---Inputs---
    file_name : {string or path}
        path to source file possibly containing calls to optimized functions
    marked_file_name : {string or path}
        path to copy of source file with marks inserted
    fdl : {list}
        function dictionary list, a list of dictionaries, each of which
        defines the free parameters of a function and its possible values
    ---Outputs---
    NONE, writes to a file specified by input
    """
    with open(file_name,'r') as f:
        lines = f.readlines()

    num_parameter_tags = 0 #number of parameter tags which have been placed
    parameter_options_list = [] #one parameter option for each tag placed
    #loop over all lines to see if they contain known functions
    for i_l,line in enumerate(lines): 
        for function_dict in fdl:
            fun_name = function_dict["function_name"]
            #if line is not a comment and it contains the function name
            if (is_viable_line(line) and (fun_name in line)):
                start_call = line.find(fun_name) #index of first character of function name
                __, end_call = locate_function_parentheses(line,start=start_call) #index of
                #close parentheses ) that ends function call
                pre_call = line[:start_call]
                post_call = line[end_call+1:]
                call_string = line[start_call:end_call+1] #of form fun(.....)
                mark_text = 'mg_tune_function_mark' + str(num_functions_found)
                lines[i_l] = pre_call + post_call
                find_free_parameters(call_string,function_dict)
    #TODO: may as well take advantage of having index of fuction start plus index of
    #its closing parentheses to insert mark for each function

    with open(marked_file_name,'w') as f:
        f.writelines(lines)
        

def insert_parameter_tags(string,fd,first_tag_num):
    """
    given a string 'fun(a,b,c=20)'
    return all (name, optional arguments) pairs of fun which have not been
    set using knowledge of all optional present in the function
    dictionary fd
    and return a tagged version of call string like
    'fun(a,b,c=20,d=mgtune_option_0,e=mg_tune_tag_1}'
    ---Inputs---
    string : {string}
        the string representing the function call, for example
            string = 'fun(a,b,c=20)'
    fdl : {list}
        function dictionary list, a list of dictionaries, each of which
        defines the free parameters of a function and its possible values
    first_tag_num : {integer}
        number to assign to first tag placed in string
    ---Outputs---
    parameter_options : {lists}
        len(parameter_options) = number of free parameters in function call
            given by string
        len(parameter_options[i]) = 2
        parameter_options[i] = [ith argument name, ith argument options (or keywords)]
    """
    string_no_newline_spaces = ''.join(string.strip().split())

    parameter_options = [] #items to be appended
    cur_tag = first_tag_num
    #loop over every possible optional argument
    for key, item in fdl.items():
        if (isinstance(item,string)):
            if (item == 'untunable'):
                #don't search if argument is untunable
                pass
        else: #search in string for instance of optional argument key
            if ((key+'=') not in string_no_newline_spaces):
                #optional_argument_name= is not inside of function call string
                parameter_options.append([key,item])
    return parameter_options
                

             

            
        

