
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

    num_functions_found = 0
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
                #lines[i_l] = pre_mark + mark_text + post_mark #insert mark in proper line
                lines[i_l] = pre_call + post_call
                find_free_parameters(call_string,function_dict)
                num_functions_found += 1
    #TODO: may as well take advantage of having index of fuction start plus index of
    #its closing parentheses to insert mark for each function

    with open(marked_file_name,'w') as f:
        f.writelines(lines)
        
def find_free_parameters(string,fdl):
#        record location in file (maybe by inserting a keyword like mgtune_insert_N)
#        determine which parameters are unset
#        for each unset parameter:
#            add a starting value to NOMAD parameter file and record it's number
    pass
