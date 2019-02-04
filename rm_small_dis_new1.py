import numpy as np
import os
import sys
sys.path.append(os.path.abspath("/lustre/lwork/yclee/python_practice/cneb"))
from get_input import *

tri = tot * 3

####################################
def get_all_inp(directory):
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
    return_list = [None] * tot

    with open(file_target, "r") as p:
        find = False
        first_time = True
        for i, line in enumerate(p):
            if first_time:
                if "%mem" in line:
                    number = i + 5
                    find = True
                    first_time = False
            if find:
                for x in range (0, tot):
                    if ((number+x+2) > i)and (i > (number+x)):
                        b = str_list2float_list(line.split()[1:4])
                        return_list[x] = b

    return return_list
######################################
def find_dis(the_list):
    return_list = the_list
    counter = 0
    while counter < 7:
        read_list = return_list
        for i in range(0, len(the_list)-1):
            for x in range(1, len(the_list)-i):
                ele1 = np.array(read_list[i]).reshape(1,3)
                ele2 = np.array(read_list[i+x]).reshape(1,3)
                ele3 = ele1 - ele2
                sq = np.power(ele3, 2)
                sum1 = np.sum(sq, axis=1)
                dis = np.power(sum1, 0.5)
                if dis < 0.8 :
                    ele2new = (ele2-ele1) * ((1/dis) ** 0.5) + ele2
                    return_list[i+x] = ele2new.tolist()   
                else :
                    return_list[i+x] = read_list[i+x]
        read_list = return_list
        counter += 1
    return return_list
##############################################
def no_list(the_list):
    return_list = []
    for i in range(0,len(the_list)):
        if type(the_list[i]) == float:
            return_list.append(the_list[i])
        elif type(the_list[i]) == list:
            for x in range(0, len(the_list[i])):
                return_list.append((the_list[i])[x])
    return return_list
##################################################
def get_rid_of(the_list):
    return_list = []
    for i in range(0,len(the_list)):
        return_list += the_list[i]
    return return_list
##############################################
def get_all_new_list(inp_list):
    return_list = [None] *len(inp_list)
    for i in range(0, len(inp_list)):
        return_list[i] = no_list(get_rid_of(find_dis(get_coord(inp_list[i]))))
    return return_list
#############################################
def get_to_poscar(name, list_aft_sp):
    f = open(name, 'w')
    ori_name = str(name)
    fi_name = ori_name[:1]
    a = list_aft_sp
    b = np.array(a).reshape(tot,3)
    c = b.tolist()
    str1  =""
    xyz_list= ["\t \t".join(str(j) for j in i) for i in c]
    element_list = ele_list
    for x in range(0, len(xyz_list)):
        str1 += element_list[x] +"\t" + xyz_list[x] +"\n"

    str_initial = "%chk="+fi_name+".chk" +" \n" + "%nprocshared=12 \n" + "%mem=4GB \n" + "# force rb3lyp/6-311+g(d,p) Guess=TCheck  \n \n" + ele_string + "\n \n" + str(charge) + " " + str(multi) + "\n" 
    add = "\n"
    f.write(str_initial)
    f.write(str1)
    f.write(add)
    f.close()

###############################################

def all_new_pos(the_list):
    for i in range(1, len(the_list)-1):
        get_to_poscar(str(i)+".inp", the_list[i])

###############################################

all_inp = get_all_inp(".")
img = image
all_new_list = get_all_new_list(all_inp)
all_new_pos(all_new_list)
