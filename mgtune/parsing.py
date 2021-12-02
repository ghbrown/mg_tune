
import os
import re
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
    

def tag_file(file_name,tagged_file_name,fdl):
    """
    finds and inserts all unused options of tunable parameters
    with value set to tag of form "mgtune_tag_*" in file at
    file_name
    ---Inputs---
    file_name : {string or path}
        path to source file possibly containing calls to optimized functions
    tagged_file_name : {string or path}
        path to copy of source file with marks inserted
    fdl : {list}
        function dictionary list, a list of dictionaries, each of which
        defines the free parameters of a function and its possible values
    ---Outputs---
    parameter_options_list : {list}
        list keeping track of all free parameters (those that are inserted with tag)
            and their respective possible values
        len(parameter_options_list) = number of free parameters in function call
            given by string
        len(parameter_options_list[i]) = 2
        parameter_options_list[i] = [ith option name, ith argument options (or keywords)]
    NOTE: also writes to file tagged_file_name
    """
    with open(file_name,'r') as f:
        lines = f.readlines()

    cur_tag_num = 0 #number of parameter tags which have been placed
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
                tagged_call_string,call_parameter_options_list = tag_call(call_string,
                                                                          function_dict,
                                                                          cur_tag_num)
                parameter_options_list += call_parameter_options_list
                lines[i_l] = pre_call + tagged_call_string + post_call #overwrite line with
                #function call with tagged version of the functionc call
                num_tags_added = len(call_parameter_options_list)
                cur_tag_num += num_tags_added

    with open(tagged_file_name,'w') as f:
        f.writelines(lines)
    return parameter_options_list
        

def tag_call(string,fd,first_tag_num):
    """
    given a string 'fun(a,b,c=20)' corresponding to a single function call
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
    tagged_string : {string}
        input string with unused optional argument names and tags inserted
    parameter_options : {lists}
        len(parameter_options) = number of free parameters in function call
            given by string
        len(parameter_options[i]) = 2
        parameter_options[i] = [ith argument name, ith argument options (or keywords)]
    """
    string_no_close_paren = string[:-1] #lop off closing parentheses
    parameter_options = [] #items to be appended
    cur_tag = first_tag_num
    tagged_string = string_no_close_paren #copy to be edited

    #loop over every possible optional argument
    for key, item in fd.items():
        if (isinstance(item,str) and (item == 'untunable')):
                #don't search in function call if argument is untunable
                pass
        else: #search in string for instance of optional argument key
            option_pattern = key + ' *=' #regex that matches: key, any number of spaces, then =
            m = re.search(option_pattern,string) #None if no matches
            if (m is None): 
                #optional_argument_name *= is not inside of function call string
                #means that it should be set
                parameter_options.append([key,item])
                tagged_string += f', {key}=mgtune_tag_{cur_tag}'
                cur_tag += 1

    tagged_string = tagged_string + ')' #add back closing parentheses
    return (tagged_string, parameter_options)
                

             

            
        

