import numpy as np
import sys


def cal_limb_length(dm, j, n):
    lvs = list(range(n))
    lvs.remove(j)
    v= 1e9
    for id1 in range(len(lvs) - 1):
        for id2 in range(id1, len(lvs)):
            i = lvs[id1]
            k = lvs[id2]
            tmp =  dm[i][j] + dm[j][k] - dm[i][k]
            tmp /= 2
            if tmp < v:
                v = tmp
    return int(v)


if __name__ == "__main__":
    with open('limb_length_input.txt', 'r') as file:
        ins = file.read().splitlines()
        n = int(ins[0])
        j = int(ins[1])

        distance_matrix  = []
        for line in ins[2:]:
            distance_matrix.append([int(x) for x in line.split()]) 
    
    
    print(cal_limb_length(distance_matrix, j, n))