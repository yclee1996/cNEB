import numpy as np
import os
import sys
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
    return_list = [1] * len(the_log)
    for i in range(0, len(the_log)):
        return_list[i] = get_scf((the_log)[i])
    return return_list
######################################

def get_max_image(return_list):
    result = return_list.index(max(return_list))
    return result
#######################################
def get_local_ta(file1, file2, file3):
   # the_vec = [1] * tri
   # the_coord = np.array(the_vec).reshape(tot,3)
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
    return_list = [1] * img
    for i in range(0, img):
        return_list[i] = get_local_ta(the_log[i],the_log[i+1],the_log[i+2]).tolist()
    return return_list
#####################################
def get_vector(file1, file2):
    vec1 = get_coord(file1)
    vec2 = get_coord(file2)
    vec12 = vec2 - vec1
    return vec12
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
def get_ave_abs_force(the_list):
    return_list = []
    for i in range(1, len(the_list)-1):
        a = find_force1(all_log[i],all_log[i-1],all_log[i+1])
        for x in a:
            return_list.append(x)
    result = sorted(return_list)
    a = np.array(result).reshape((tot * img),1)
    b = np.sum(a, axis=0)
    ave_force = b / (tot * img)

    d = ave_force.tolist()
    e = 0
    for i in d:
        e += float(i)

    return e
###############################################
def get_max_index(the_list):
    return_list = []
    for i in range(1, len(the_list)-1):
        a = find_force1(all_log[i],all_log[i-1],all_log[i+1])
        for x in a:        
            return_list.append(x)
    result = return_list.index(max(return_list))
    return result
###############################################
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
def find_force2(file2, file1, file3):

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

    return_force = the_force.tolist()
    return_list = []
    for i in return_force:
        return_list.append(i)
    return return_list
##################################################
def get_force_list(the_list):
    return_list = []
    for i in range(1, len(the_list)-1):
        a = find_force2(all_log[i],all_log[i-1],all_log[i+1])
        for x in a:
            return_list.append(x)
    return return_list
#######################################
def find_force(file2, file1, file3,ave_force):

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

    my_coord = get_coord(file2)
#########################################
    if ave_force > 0.02:
        nmlized_fac = 0.018/ave_force
    elif (0.02 > ave_force) and (ave_force > 0.006):
        nmlized_fac = 0.3
    elif (0.006 > ave_force) and (ave_force > 0.003):
        nmlized_fac = 0.5
    elif 0.003 > ave_force:
        nmlized_fac = 0.6
#########################################

    ultimate_relax_force = normal_force * nmlized_fac

    coord_after_relax = my_coord + ultimate_relax_force.reshape(tot,3)

    coord_list = coord_after_relax.tolist()


    return coord_list
#######################################
def find_force_c(file2, file1, file3,ave_force):

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

    tot_force = my_force - (para_force * 2)

    my_coord = get_coord(file2)
#########################################
    if ave_force > 0.02:
        nmlized_fac = 0.018/ave_force
    elif (0.02 > ave_force) and (ave_force > 0.006):
        nmlized_fac = 0.3
    elif (0.006 > ave_force) and (ave_force > 0.003):
        nmlized_fac = 0.5
    elif 0.003 > ave_force:
        nmlized_fac = 0.6
#########################################

    ultimate_relax_force = tot_force * nmlized_fac

    coord_after_relax = my_coord + ultimate_relax_force.reshape(tot,3)

    coord_list = coord_after_relax.tolist()


    return coord_list

########################################   
def get_dist(ele1, ele2):
    cor1 = np.array(ele1).reshape(tri,1)

    cor2 = np.array(ele2).reshape(tri,1)
    vect = cor1 - cor2
    ab_square = np.power(vect, 2)
    total_dist = np.sum(ab_square, axis=0)
    dist = np.power(total_dist, 0.5)
    return dist
#######################################
def relax_between(all_log,ave_force):
    return_list = [1] * (len(all_log)-2)
    for i in range(0, len(all_log)-2):
        return_list[i] = find_force(all_log[i+1],all_log[i],all_log[i+2],ave_force)
    return return_list

####################################
def relax_between_c(all_log,ave_force):
    return_list = [1] * (len(all_log)-2)
    for i in range(0, len(all_log)-2):
        return_list[i] = find_force_c(all_log[i+1],all_log[i],all_log[i+2],ave_force)
    return return_list

####################################


def get_all_relax_list(a, all_log, c,max_en_image):
    return_list = [1] * len(all_log)
    return_list[0] = a
    for i in range(1, len(all_log)-1):
        if i != max_en_image:
            return_list[i] = relax_between(all_log,ave_force)[i-1]
        if i == max_en_image:
            return_list[i] = relax_between_c(all_log,ave_force)[i-1]

    return_list[-1] = c
    return return_list
####################################
def get_new_relax_list(the_list):
    return_list = [1] * len(the_list)
    a = max_image
    for i in range(0, len(the_list)):
        if i != a:
            return_list[i] = the_list[i]
        elif i == a:
            sp_list = [1] * tot
            b = max_atom
            for x in range(0, tot):
                if x != b:
                    sp_list[x] = (the_list[a])[x]
                elif x == b:
                    a1 = np.array((the_list[i])[b])
                    a2 = np.array(force_list[max_index]) * 0.5
                    a3 = (a1 + a2).tolist()
                    sp_list[x] = a3  
            return_list[i] = sp_list
    return return_list
####################################
def get_dist_o(dis1, dis2):
    cor1 = get_coord(dis1)
    cor2 = get_coord(dis2)
    vect = cor1 - cor2
    cc = vect.reshape(tri,1)
    ab_square = np.power(cc, 2)
    total_dist = np.sum(ab_square, axis=0)
    dist = np.power(total_dist, 0.5)
    return dist
#####################################
def get_ave_dis(the_list):
    all_dis = 0
    for i in range(0, len(the_list)-1):
        dis = get_dist(the_list[i], the_list[i+1])
        all_dis += dis
        ave_dis = all_dis/tot
    return ave_dis

#####################################
def find_sp_k(the_list,en_max,en_ref):
    return_list = [1] * (len(the_list)-1)
    for i in range(0, (len(the_list)-1)):
        if the_list[i] > en_ref:
            return_list[i]= 2 - (1 * (en_max - max(the_list[i],the_list[i+1]))/(en_max - en_ref))
        elif the_list[i] < en_ref:
            return_list[i] = 1
        elif the_list[i] == en_ref:
            return_list[i] = 1
    return return_list
#####################################
def coord_after_sp(ele1, ele2, ele3, the_list, the_k_1, the_k_2, ta_coord):
    cod2 = np.array(ele2)
    cod3 = np.array(ele3)   

    ori_coord = np.array(ele1)
    ori = ori_coord.reshape(tri,1)

    delta1 = get_dist(ele1, ele2) - get_ave_dis(the_list)
    direct1 = cod2 - ori_coord
    b = direct1.reshape(tri,1)
    sp_force1 = delta1 * b * the_k_1
    
    delta2 = get_dist(ele1, ele3) - get_ave_dis(the_list)
    direct2 = cod3 - ori_coord
    d = direct2.reshape(tri,1)
    sp_force2 = delta2 * d * the_k_2

    sp_total = sp_force1 + sp_force2
    
    my_force = sp_total.reshape(tri, 1)

    vector_13 = np.array(ta_coord)

    c = vector_13.reshape(tri,1)

    ab_2 = np.power(c, 2)

    total_dist = np.sum(ab_2, axis=0)

    abc = my_force * c

    sum_inner_product = np.sum(abc, axis=0)

    k = sum_inner_product / total_dist

    para_vector = k * c


    the_sp = para_vector * 0.1    

    aft = ori + the_sp
    aft_coord = aft.reshape(tot,3)
    return aft_coord.tolist()

#####################################
def get_max_dis(relax_list):
    list_dis_ = []
    for i in range(0, len(relax_list)-1):
        list_dis_.append(get_dist(relax_list[i], relax_list[i+1]).tolist())
    list_dis = sorted(list_dis_)
    a = np.array(list_dis[-1])
    b = np.array(list_dis[0])
    return float(a-b)

#####################################

def sp_iterator(relax_list,ta_list):

    stop = 0.003

    return_list = [1] * len(relax_list)
    return_list[0] = relax_list[0]
    return_list[-1] = relax_list[-1]
    for i in range(1, len(relax_list)-1):
        return_list[i] = coord_after_sp(relax_list[i],relax_list[i-1],relax_list[i+1], relax_list, k_list[i-1], k_list[i], ta_list[i-1])

    dis_diff = get_max_dis(return_list)

    list_toberead = return_list
    counter = 0
    while counter < 7:
        return_list = [1] * len(relax_list)
        return_list[0] = relax_list[0]
        return_list[-1] = relax_list[-1]
        for i in range(1, len(relax_list)-1):
            return_list[i] = coord_after_sp(list_toberead[i],list_toberead[i-1],list_toberead[i+1], list_toberead, k_list[i-1], k_list[i], ta_list[i-1])

        dis_diff = get_max_dis(return_list)
        counter += 1
        list_toberead = return_list
    return return_list

##############################################

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

 
all_log = get_all_log(".")
max_en_image = get_max_image(get_all_scf(all_log))
scf_list = get_all_scf(all_log)
en_max = max(scf_list)
en_ref = max(scf_list[0],scf_list[-1])
ta_list = get_all_tangent_list(all_log)
ave_force = get_ave_abs_force(all_log)
max_val = get_max_abs_force(all_log)
force_list = get_force_list(all_log)
max_index = get_max_index(all_log)
max_image = int(max_index/tot) + 1
max_atom = max_index%tot
relax_IS = get_coord(all_log[0]).tolist()
relax_P  = get_coord(all_log[-1]).tolist()
all_relax_list = get_all_relax_list(relax_IS, all_log, relax_P,max_en_image)
all_relax_list1 = get_new_relax_list(all_relax_list)
k_list = find_sp_k(scf_list,en_max,en_ref)
all_new_pos(sp_iterator(all_relax_list,ta_list))
