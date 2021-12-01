
import os
import copy

    
#THE RIGHT WAY TO DO THIS IS BY ACCESSING ABSTRACT SYNTAX TREES,
#BUT NOT COMFORTABLE WITH THAT RIGHT NOW

#loop over input file lines
#    look for functions mgtune "knows about" ((not comment) and (wfdl[n]["name"] in line))
#    when such a function is found:
#        record location in file (maybe by inserting a keyword like mgtune_insert_N)
#        determine which parameters are unset
#        for each unset parameter:
#            add a starting value to NOMAD parameter file and record it's number
