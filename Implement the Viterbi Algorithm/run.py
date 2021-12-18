import numpy as np

with open("input.txt") as f:
    lines = [line.strip() for line in f]

emission = lines[0].strip()
alphabet = lines[2].strip().split()
emission = [int(alphabet.index(em)) for em in emission]
states = lines[4].strip().split()

T = []
for line in lines[7:7+len(states)]:
    T.append(np.log(np.array(line.split()[1:], float)))
T= np.array(T)

E = []
for line in lines[9+len(states):]:
    E.append(np.log(np.array(line.split()[1:], float)))
E= np.array(E)

V = np.zeros(shape = (len(states), len(emission))) - 100000000
P = [[0 for e in range(len(emission))] for s in range(len(states))] 

for i in range(len(states)):
    V[i][0] = np.log(1 / len(states)) + E[i][emission[0]]
    P[i][0] = -1
    
for i in range(1, len(emission)):
    for s in range(len(states)):
        for prev in range(len(states)):
            value = E[s][emission[i]] + T[prev][s] + V[prev][i-1]
            if value > V[s][i]:
                V[s][i] = value
                P[s][i] = prev
                
score = -10000000
for i in range(len(states)):
    if V[i][len(emission)-1] > score:
        l = i
        score = V[i][len(emission)-1]

path = [l]
i = len(emission) - 1
while i > 0:
    p = P[l][i]
    path.append(p)
    l = p
    i -= 1

f = open('output.txt', 'w')
f.write(''.join(str(states[state]) for state in path[::-1]))
f.close()
