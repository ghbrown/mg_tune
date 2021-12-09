
import sys

def obj():
    x_file_name = sys.arv[1]
    with open(x_file_name,'r') as f:
        line = f.readlines()[0]

    x_strings = line.split()
    x = [int(elem) for elem in x_strings]
    print(x)
    
    print(f)

obj()
