import numpy as np
import os
import sys
sys.path.append(os.path.abspath("/lustre/lwork/yclee/python_practice/cneb"))
from get_input import *

tri = tot * 3

####################################
def get_all_inp(directory):
    all_inp = []
    for i in os.listdir(directory):
        if os.path.isfile(directory + os.sep +i) and i[-4:]== ".inp":
            all_inp.append(i)
    return sorted(all_inp)
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
#####################################
def coord_between(ele1, ele2):
    cod_between = [None] * image
    for i in range(1, (image+1)):
        cod_between[i-1] = ele1 + (ele2-ele1)/(image+1)*i
   
    return cod_between
###################################

########################################
def get_to_poscar(name, image_list):
    f = open(name, 'w')
    ori_name = str(name)
    fi_name = ori_name[:1]
    a = image_list
    b = np.array(a).reshape(tot,3)
    c = b.tolist()
    str1  =""
    xyz_list= ["\t \t".join(str(j) for j in i) for i in c]
    element_list = ele_list
    for x in range(0, len(xyz_list)):
        str1 += element_list[x] +"\t" + xyz_list[x] +"\n"

    str_initial = "%chk="+fi_name+".chk" +" \n" + "%nprocshared=12 \n" + "%mem=4GB \n" + "# force rb3lyp/6-311+g(d,p) \n \n" + ele_string + "\n \n" + str(charge) + " " + str(multi) + "\n"

    add = "\n"
    f.write(str_initial)
    f.write(str1)
    f.write(add)
    f.close()

###############################################

def all_new_pos(the_list):
    for i in range(0, image):
        get_to_poscar(str(i+1)+".inp", the_list[i])
###############################################
all_inp = get_all_inp(".")
coord_ini = get_coord(all_inp[0])
coord_fin = get_coord(all_inp[-1])
cod_list = coord_between(coord_ini, coord_fin)
all_new_pos(cod_list)
