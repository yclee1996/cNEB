#############################
def get_element(file_target):
    return_list = []
    c = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "system" in line:
                number = i
                find = True
            
            if find:
                if i == number:
                    b = line.split("system = ")[1]
                    c += b.split()
        for x in range(0, len(c)):
            if (x % 2) == 0:
                return_list.append(c[x])
    return return_list
###############################
def get_ele_num(file_target):
    return_list = []
    c = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "system" in line:
                number = i
                find = True

            if find:
                if i == number:
                    b = line.split("system = ")[1]
                    c += b.split()
        for x in range(0, len(c)):
            if (x % 2) == 1:
                return_list.append(c[x])
    return return_list

###############################
def get_tot_number(the_list):
    a = 0
    for i in the_list:
        a += int(i)
    return a
##############################
def get_together(list_1, list_2):
    a = ""
    for x in range(0,len(list_1)):
        b = str(list_1[x]) + str(list_2[x])
        a += b
    return a
##################################
def get_ele_list(list_1, list_2):
    
    ele_list = [None]*tot
    list_2.insert(0,0)
    for i in range(0,len(list_1)):
        for x in range(list_2[i],list_2[i+1]):
            ele_list[x] = list_1[i]
  
    
    return ele_list
###################################
def get_new_num(the_list):
    return_list = []
    for i in range(0, len(the_list)):
        a = the_list[0:(i+1)]
        b = []
        for x in range(0, len(a)):
            d = int(a[x])
            b.append(d)
        return_list.append(sum(b))

    return return_list
###############################
def get_image(file_target):
    return_list = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "image" in line:
                number = i
                find = True

            if find:
                if i == number:
                    b = line.split("image = ")[1]
                    return int(b)

############################
def get_NSW(file_target):
    return_list = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "nsw" in line:
                number = i
                find = True

            if find:
                if i == number:
                    b = line.split("nsw = ")[1]
                    return int(b)
############################
def get_charge(file_target):
    return_list = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "charge" in line:
                number = i
                find = True

            if find:
                if i == number:
                    b = line.split("charge = ")[1]
                    return int(b)

############################
def get_multi(file_target):
    return_list = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "multiplicity" in line:
                number = i
                find = True

            if find:
                if i == number:
                    b = line.split("multiplicity = ")[1]
                    return int(b)
############################
def get_conv(file_target):
    return_list = []
    find = False
    with open(file_target, "r") as p:
        for i, line in enumerate(p):
            if "converge" in line:
                number = i
                find = True

            if find:
                if i == number:
                    b = line.split("converge = ")[1]
                    return float(b)


############################


ele = get_element("input")
num = get_ele_num("input")
tot = get_tot_number(num)
ele_string = get_together(ele, num)
num2 = get_new_num(num)
ele_list = get_ele_list(ele, num2)
image = get_image("input")
nsw = get_NSW("input")
charge = get_charge("input")
multi = get_multi("input")
conv = get_conv("input")
