import networkx as nx

G = nx.DiGraph()
# read the input file and add the prefix and suffix of 
with open('input.txt') as f:
    lines = f.read().rstrip().splitlines()
    k, d = [int(i) for i in lines[0].split()]
    for i in lines[1:]:
        Pattern1, Pattern2 = i.split('|')
        G.add_edge((Pattern1[:-1], Pattern2[:-1]), (Pattern1[1:], Pattern2[1:]))

# Eulerian trail (or Eulerian path) is a trail in a finite graph that visits every edge exactly once 
path = nx.eulerian_path(G)
start = next(path)

p1 = start[0][0] + start[1][0][-1]
p2 = start[0][1] + start[1][1][-1]

for i in range(d):
    nxt = next(path)
    p1 += nxt[1][0][-1]
    p2 += nxt[1][1][-1]

seq = p1 + p2
for e in path: seq += e[1][1][-1]

with open('output.txt', 'w') as f:
    f.write(seq)