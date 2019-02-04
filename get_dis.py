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

def get_coord(file_target):
    coord_1 = []

    with open(file_target, "r") as p:
        find = False
        first_time = True
        for i, line in enumerate(p):
            if first_time:
                if "orientation" in line:
                    number = i + 4
                    find = True
                    first_time = False
            if find:
                if (number + (tot+1) > i)and (i > number):
                    b = str_list2float_list(line.split()[3:6])
                    coord_1 += b

    all_coord_1 = np.array(coord_1)
    coord = all_coord_1.reshape(tot,3)
    return coord

#################################################

def get_dist_o(dis1, dis2):
    cor1 = get_coord(dis1)
    cor2 = get_coord(dis2)
    vect = cor1 - cor2
    cc = vect.reshape(tri,1)
    ab_square = np.power(cc, 2)
    total_dist = np.sum(ab_square, axis=0)
    dist = np.power(total_dist, 0.5)
    return dist.tolist()
#####################################
def get_all_dis(the_list):
    return_list = []
    for i in range(0, len(the_list)-1):
        return_list.append(get_dist_o(the_list[i],the_list[i+1])[0])
    return return_list

##################################### 

all_log = get_all_log(".")
img = len(all_log) - 2
print (get_all_dis(all_log))
