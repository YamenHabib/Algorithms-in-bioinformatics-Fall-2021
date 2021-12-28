import numpy as np
def colored_edges_cycles(blue, red):
    size = len(blue)+len(red)+1
    adj = np.zeros(shape=(size,2),dtype=int)
    visited = [0]*(size)
    for e in blue:
        adj[e[0],0] = e[1]
        adj[e[1],0] = e[0]
    for e in red:
        adj[e[0],1] = e[1]
        adj[e[1],1] = e[0]
    cycles = []
    for v in range(1,size):
        if visited[v]==1:
            continue
        visited[v]==1
        head = v
        c = [head]
        color = 0
        while(True):
            v = adj[v,color]
            if v == head:
                cycles.append(c)
                break
            visited[v] = 1
            c.append(v)
            color = (color+1)%2
    return cycles


def count_block(p,q):
    s = set()
    for i in p[0]:
        s.add(abs(i))
    for i in q[0]:
        s.add(abs(i))
    return len(s)
    
def graph_2_gen(g):
    size = len(g)*2+1
    visited = []
    adj = np.zeros(shape=size,dtype=int) ##
    for e in g:
        adj[e[0]] = e[1]
        adj[e[1]] = e[0]
    genome = []
    for e in g:
        orig = e[0]
        if orig in visited:
            continue
        visited.append(orig)
        if orig%2 == 0:
            close = orig-1
        else:
            close = orig+1
        tmp = []
        while(True):
            if orig%2 ==0:
                tmp.append(int(orig/2))
            else:
                tmp.append(int(-(orig+1)/2))
            dest = adj[orig]
            visited.append(dest)
            if dest==close:
                genome.append(tmp)
                break
            
            if dest%2 == 0:
                orig = dest-1
            else:
                orig = dest+1
            visited.append(orig)
    return genome

def edge_color(genome):
    edges = []
    cyc = []
    for chromo in genome:
        tmp = []
        for i in range(len(chromo)):
            if chromo[i]>0:
                tmp.append([chromo[i]*2-1,chromo[i]*2])
            else:
                tmp.append([chromo[i]*(-2),chromo[i]*(-2)-1])
        cyc.append(tmp)

    for chromo in cyc:
        if len(chromo)==1:
            edges.append(chromo[0][::-1])
            continue
        for i in range(len(chromo)-1):
            edges.append([ chromo[i][1],chromo[i+1][0] ])
        edges.append([chromo[i+1][1],chromo[0][0]])
    return edges

def two_break(p,a1,a2,b1,b2):
    g = edge_color(p)
    rem = [[a1,a2],[a2,a1],[b1,b2],[b2,b1]]
    bg = []
    for e in g:
        if e not in rem:
            bg.append(e)
    bg.append([a1,b1])
    bg.append([a2,b2])
    g = bg
    return graph_2_gen(g)

def two_break(p,q):
    red = edge_color(q)
    path = [p]
    blue = edge_color(p)
    red = edge_color(q)
    cycles = colored_edges_cycles(blue,red)
    cnt_cyc = len(cycles)
    cnt_block = count_block(p,q)

    while(cnt_block - cnt_cyc>0):
        blue = edge_color(p)
        cycles = colored_edges_cycles(blue,red)
        for c in cycles:
            if len(c)>=4:
                p = two_break(p,c[0],c[1],c[3],c[2])
                path.append(p)
                break
        blue = edge_color(p)
        red = edge_color(q)
        cycles = colored_edges_cycles(blue,red)
        cnt_cyc = len(cycles)
        cnt_block = count_block(p,q)
    return path

if __name__ == '__main__':
    lines = open('input.txt').read().split('\n')
    genome1 = [list(map(int,lines[0].strip('(').strip(')').split()))]
    genome2 = [list(map(int,lines[1].strip('(').strip(')').split()))]
    
    path = two_break(genome1,genome2)
    with open('output.txt', 'w') as f:
        for line in path:
            for chromo in line:
                for i in range(len(chromo)):
                    if i==0:
                        f.write('(')
                    else:
                        f.write(' ')
                    if chromo[i]>0:
                        f.write('+'+str(chromo[i]))
                    else:
                        f.write(str(chromo[i]))
                f.write(')')
            f.write('\n')