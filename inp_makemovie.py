import numpy as np
import os
import sys
sys.path.append(os.path.abspath("/lustre/lwork/yclee/python_practice/cneb"))
from get_input import *

tri = tot * 3



####################################
def get_all_log(directory):
    all_log = []
    for i in os.listdir(directory):
        if os.path.isfile(directory + os.sep +i) and i[-4:]== ".inp":
            all_log.append(i)
    return sorted(all_log)
####################################
def str_list2float_list(str_l):
    return_list = []
    for x in str_l:
        return_list.append(float(x))
    return return_list
#######################################

def get_coord(file_target):
    coord_1 = []

    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if (len(line.split()) == 4) and i > 5:
                number = i
                if (i > (number-1)) and ((tot+number) > i):
                    b = str_list2float_list(line.split()[1:4])
                    coord_1 += b

    all_coord_1 = np.array(coord_1)
    coord = all_coord_1.reshape(tot,3)
    return coord
#######################################
def get_list(target):
    return_list = [None] * len(target)
    for i in range(0, len(target)):
        return_list[i] = get_coord(target[i]).tolist()
    return return_list
#####################################
def movie(name, target):
    f = open(name, 'w')
    for i in range(0, len(target)):
        a = target[i]
        xyz_list= ["\t \t".join(str(j) for j in i) for i in a]
        element_list = ele_list

        ss = str(tot)
        first = "\n \n"
        f.write(ss)
        f.write(first)
        c = ""
        for x in range(0, len(element_list)):
            c += element_list[x] +"\t" + xyz_list[x] +"\n"  
        f.write(c)
    f.close()
####################################
all_log = get_all_log(".")
the_list = get_list(all_log)
movie("movie.xyz", the_list)
