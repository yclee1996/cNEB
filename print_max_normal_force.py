import numpy as np
import os 
import sys
import shutil
sys.path.append(os.path.abspath("/lustre/lwork/yclee/python_practice/cneb"))
from get_input import *

tri = tot * 3
img = image

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
######################################
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
def get_local_ta(file1, file2, file3):
    the_vec = [None] * tri
    the_coord = np.array(the_vec).reshape(tot,3)
    e1 = get_scf(file1)
    e2 = get_scf(file2)
    e3 = get_scf(file3)
    if (e3 > e2) and (e2 > e1):
        the_coord = (get_coord(file3) - get_coord(file2))
    elif (e3 < e2) and (e2 < e1):
        the_coord = (get_coord(file2) - get_coord(file1))
    elif (e3 > e2) and (e2 < e1):
        the_coord = (e3-e2)*(get_coord(file3) - get_coord(file2)) + (e1-e2)*(get_coord(file2) - get_coord(file1))
    elif (e3 < e2) and (e2 > e1):
        the_coord = (e2-e1)*(get_coord(file3) - get_coord(file2)) + (e2-e3)*(get_coord(file2) - get_coord(file1))
    return the_coord

######################################
def get_all_tangent_list(the_log):
    return_list = [None] * img
    for i in range(0, img):
        return_list[i] = get_local_ta(the_log[i],the_log[i+1],the_log[i+2]).tolist()
    return return_list
#####################################
def get_para_force(ori_force, file1, file2, file3):

    my_force = ori_force.reshape(tri, 1)

    vector_13 = get_local_ta(file1, file2, file3)

    c = vector_13.reshape(tri,1)

    ab_2 = np.power(c, 2)

    total_dist = np.sum(ab_2, axis=0)

    abc = my_force * c

    sum_inner_product = np.sum(abc, axis=0)

    k = sum_inner_product / total_dist

    para_vector = k * c

    return para_vector
####################################

def find_force1(file2, file1, file3):

    force=[]


    with open(file2, "r") as o:
        find = False
        first_time = True
        for i, line in enumerate(o):
            if first_time:
                if "Axes" in line:
                    number = i + 4
                    find = True
                    first_time = False

            if find:
                if (number + (tot+1) > i)and (i > number):
                   a = str_list2float_list(line.split()[2:5])
                   force += a

    full_real_force = np.array(force)
    
    my_force = full_real_force.reshape(tri,1)

    para_force = get_para_force(full_real_force, file1, file2, file3)

    normal_force = my_force - para_force

    the_force = normal_force.reshape(tot,3)
    sq_force = np.power(the_force, 2)
    sum_force = np.sum(sq_force, axis=1)
    at_force = np.power(sum_force, 0.5)
        


    return_force = at_force.tolist()
    return_list = []
    for i in return_force:
        return_list.append(i)
    return return_list
###############################################

def get_max_index(the_list):
    return_list = []
    for i in range(1, len(the_list)-1):
        a = find_force1(all_log[i],all_log[i-1],all_log[i+1])
        for x in a:        
            return_list.append(x)
    result = return_list.index(max(return_list))
    return result
#######################################
def get_ave_abs_force(the_list):
    return_list = []
    for i in range(1, len(the_list)-1):
        a = find_force1(all_log[i],all_log[i-1],all_log[i+1])
        for x in a:
            return_list.append(x)
    result = sorted(return_list)
    a = np.array(result).reshape((tot*img),1)
    b = np.sum(a, axis=0)
    ave_force = b / (tot*img)

    d = ave_force.tolist()
    e = 0
    for i in d:
        e += float(i)

    return e
##################################
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
#######################################
def get_max_abs_force(the_list):
    return_list = []
    for i in range(1, len(the_list)-1):
        a = find_force1(all_log[i],all_log[i-1],all_log[i+1])
        for x in a:        
            return_list.append(x)
    result = sorted(return_list)
    max_val = result[-1]
    return max_val
#######################################

all_log = get_all_log(".")
scf_list = get_all_scf(all_log)
ta_list = get_all_tangent_list(all_log)
max_index = get_max_index(all_log)
ave_force = get_ave_abs_force(all_log)
max_val = get_max_abs_force(all_log)
counter = get_counter("decision") -1


with open("max_normal_force", "a") as p:
    p.write(str(counter)+"."+"\t"+ str(max_val)+ " \t"  + str(max_index)+ "\n")
