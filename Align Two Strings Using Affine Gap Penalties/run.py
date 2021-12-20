import numpy as np

gap_opening_penalty = 11
gap_extension_penalty = 1

alignment_1 = ""
alignment_2 = ""

def my_append(c1, c2):
    global alignment_1
    global alignment_2
    alignment_1 += c1
    alignment_2 += c2


with open('BLOSUM62', 'r') as file:
    alphab = file.readline().rstrip().split()
    matr = []
    for _ in range(len(alphab)):
        line = file.readline().rstrip().split()
        matr.append([int(line[i]) for i in range(1, len(line))])


with open('input.txt', 'r') as file:
    v = file.readline().rstrip()
    w = file.readline().rstrip()


len_v = len(v)
len_w = len(w)

low = np.zeros((len_v + 1, len_w + 1))
trans_low = [[0]*(len_w+1) for _ in range(len_v+1) ]

trans_mid = [[0]*(len_w+1) for _ in range(len_v+1) ]
mid = np.zeros((len_v + 1, len_w + 1))

trans_up =  [[0]*(len_w+1) for _ in range(len_v+1) ]
up =  np.zeros((len_v + 1, len_w + 1))



for i in range(1, len(v) + 1):
    for j in range(1, len_w + 1):
        low[i][j] = max(low[i-1][j] - gap_extension_penalty, mid[i-1][j] - gap_opening_penalty)
        
        if low[i][j] == low[i-1][j] - gap_extension_penalty:
            trans_low[i][j] = ('l', i-1, j)
        else:
            trans_low[i][j] = ('m', i-1, j)

        up[i][j] = max(up[i][j-1] - gap_extension_penalty, mid[i][j-1] - gap_opening_penalty)
        
        if up[i][j] == up[i][j-1] - gap_extension_penalty:
            trans_up[i][j] = ('u', i, j-1)
        else:
            trans_up[i][j] = ('m', i, j-1)

        mid[i][j] = max(low[i][j],
                                mid[i-1][j-1] + matr[alphab.index(v[i-1])][alphab.index(w[j-1])],
                                up[i][j])
        if mid[i][j] == low[i][j]:
            trans_mid[i][j] = ('l', i, j)
        elif mid[i][j] == up[i][j]:
            trans_mid[i][j] = ('u', i, j)
        else:
            trans_mid[i][j] = ('m', i-1, j-1)

f = trans_mid[len(v)][len(w)]
cur = 'm'

while f != 0:
    if cur == 'l':
        if f[0] == 'l':
            my_append(v[f[1] - 1], "-")
            f = trans_low[f[1]][f[2]]
        else:
            f = trans_mid[f[1]][f[2]]
            cur = 'm'
    elif cur == 'u':
        if f[0] == 'u':
            my_append("-", w[f[2] - 1])
            f = trans_up[f[1]][f[2]]
        else:
            f = trans_mid[f[1]][f[2]]
            cur = 'm'
    elif cur == 'm':
        if f[0] == 'l':
            my_append(v[f[1] - 1], "-")
            f = trans_low[f[1]][f[2]]
            cur = 'l'
        elif f[0] == 'm':
            my_append(v[f[1]], w[f[2]])
            f = trans_mid[f[1]][f[2]]
        else:
            my_append("-", w[f[2]-1])
            f = trans_up[f[1]][f[2]]
            cur = 'u'
    else:
        break

f = open('output.txt', 'w')
f.write(str(int(mid[-1][-1])))
f.write("\n")
f.write(alignment_1[::-1])
f.write("\n")
f.write(alignment_2[::-1])
f.close()