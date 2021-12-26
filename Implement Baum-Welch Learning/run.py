def form_res(a):
    res=[]    
    for i in range(len(a[0])):
        res.append([])
        for j in range(len(a)):
            res[-1].append(a[j][i])
    return res

def forward(p_states, p_strings):
    mat=[]
    P=[]
    for n in range(len(states)):
        P.append(1/len(states) * float(p_strings[n][strings.index(observe[0])]))
    mat.append(P)    
    for i in range(1, len(observe)):
        tmp = []
        for j in range(len(states)):
            s=0
            for k in range(len(states)):
                s += float(p_states[k][j]) * P[k] * float(p_strings[j][strings.index(observe[i])])
            tmp.append(s)
        P = tmp[:]
        mat.append(P)
    
    return form_res(mat), sum(mat[-1])

def backward(p_states, p_strings):
    back=[]
    P=[]
    for n in range(len(states)):
        P.append(1)
    back.append(P)    
    for i in range(len(observe)-2, -1, -1):
        tmp = []
        for j in range(len(states)):
            s=0
            for k in range(len(states)):
                s += float(p_states[j][k]) * P[k] * float(p_strings[k][strings.index(observe[i+1])])
            tmp.append(s)
        P = tmp[:]
        back.append(P)
    back = back[::-1]
    
    return form_res(back)


def estimate_emission_mat(p):
    e=[]
    for i in range(len(states)):
        e.append([])
        for j in range(len(strings)):
            c=0
            for k in range(len(observe)):
                if observe[k] == strings[j]:
                    c += p[i][k]
            e[-1].append(c)
    return e
    
def cal_transition_mat(p):
    t=[]
    c=0
    for i in range(len(states)):
        t.append([])
        for j in range(len(states)):
            t[-1].append(sum(p[c]))
            c+=1
    return t

def update(f, back, p):
    tmp=[]
    for i in range(len(states)):
        for j in range(len(states)):
            tmp.append([])
            for k in range(len(observe)-1):
                tmp[-1].append(f[i][k] * float(p_states[i][j]) * float(p_strings[j][strings.index(observe[k+1])]) * back[j][k+1] / p)

    updated_p_states=[]
    for i in cal_transition_mat(tmp):
        updated_p_states.append([])
        for j in i:
            updated_p_states[-1].append(j/sum(i))

    tmp=[]
    for i in range(len(states)):
        tmp.append([])
        for j in range(len(observe)):
            tmp[-1].append(f[i][j] * back[i][j] / p)
    

    updated_p_strings=[]
    for i in estimate_emission_mat(tmp):
        updated_p_strings.append([])
        for j in i:
            updated_p_strings[-1].append(j/sum(i))

    return updated_p_states, updated_p_strings

if __name__ == "__main__":
    with open('input.txt') as f:
        lines = f.read().strip().split('\n')        
        observe = lines[2]
        strings = lines[4].split()
        states = lines[6].split()
        p_states=[line[1:].split() for line in lines[9:9+len(states)]]
        p_strings = [line[1:].split() for line in lines[11+len(states):11+ 2 * len(states)]]


    for i in range(100):
        f, p = forward(p_states, p_strings)
        back = backward(p_states, p_strings)
        p_states, p_strings = update(f, back, p)


    with open('output.txt', 'w') as f1:
        f1.write('\t' + '\t'.join(states) + '\n')
        for i in range(len(p_states)):
            f1.write(states[i] + '\t' + '\t'.join(map(str, p_states[i])) + '\n')
        f1.write('--------' + '\n')
        f1.write('\t' + '\t'.join(strings) + '\n')
        for i in range(len(p_strings)):
            f1.write(states[i] + '\t' + '\t'.join(map(str, p_strings[i])) + '\n')


