import numpy as np
import os
import sys

####################################
def get_all_log(directory):
    all_log = []
    for i in os.listdir(directory):
        if os.path.isfile(directory + os.sep +i) and i[-4:]== ".log":
            all_log.append(i)
    return sorted(all_log)
####################################

def str_list2float_list(str_l):
    return_list = []
    for x in str_l:
        return_list.append(float(x))
    return return_list
#######################################
def get_scf(the_file):
    return_list = []
    with open(the_file, "r") as p:
        find = False
        first_time = True
        for i, line in enumerate(p):
            if first_time:
                if "SCF" in line:
                    number = i
                    find = True
                    first_time = False
            if find:
                if i == number:
                    b = str_list2float_list(line.split()[4:5])

                    return_list += b
    energy = 0
    for i in return_list:
        energy += float(i)
    return energy
#######################################
def get_all_scf(the_log):
    return_list = [None] * len(the_log)
    for i in range(0, len(the_log)):
        return_list[i] = get_scf((the_log)[i])
    return return_list
######################################

def get_max_image(return_list):
    result = return_list.index(max(return_list))
    return result
#######################################

all_log = get_all_log(".")
img = len(all_log) - 2 
max_image = get_max_image(get_all_scf(all_log))
scf_list = get_all_scf(all_log)




print (max_image)
print (scf_list) 
