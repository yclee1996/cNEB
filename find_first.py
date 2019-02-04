import numpy as np
import os 
import sys


####################################
def get_all_log(directory):
    all_log = []
    for i in os.listdir(directory):
        if os.path.isfile(directory + os.sep +i) and i[-4:]== ".inp":
            all_log.append(i)
    return sorted(all_log)
####################################
print (get_all_log(".")[0])
