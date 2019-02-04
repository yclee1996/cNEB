import numpy as np
import os 
import sys
sys.path.append(os.path.abspath("/lustre/lwork/yclee/python_practice/cneb"))
from get_input import *

#######################
def get_counter(file_target):
    b = []
    with open(file_target, "r") as p:
        find = False
        for i, line in enumerate(p):
            if "True" in line:
                number = i
                find = True
            elif "False" in line:
                number = i
                find = True
            if find:
                if i == number+1:
                    b.append(line)
    return int(b[0])
#######################
def new(a):
    if a > (nsw+1):
        f = open("decision", 'w')
        f.write("False\n")
        f.close()

######################
new(get_counter("decision"))
