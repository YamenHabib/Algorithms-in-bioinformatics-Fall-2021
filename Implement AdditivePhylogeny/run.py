import networkx as nx
from limb_length import cal_limb_length 


def AdditivePhylogeny(D, n, m):
    graph = nx.Graph()

    if n == 2:
        graph.add_edge(0, 1, weight = D[0][1])
        return graph

    limbLength = cal_limb_length(D, n - 1, n)

    for j in range(n - 1):
        D[j][n - 1] -= limbLength
        D[n - 1][j] = D[j][n - 1]

    # (i,n,k) ← three leaves such that Di,k = Di,n + Dn,k
    lvs = [i for i in range(n) if i != n - 1]

    for u in range(len(lvs) - 1):
        for v in range(u + 1, len(lvs)):
            i = lvs[u]
            k = lvs[v]
            if D[i][n - 1] + D[n - 1][k] == D[i][k]:
                _i = i
                _k = k

    x = D[_i][n - 1]

    # remove row n and column n from D
    del D[-1]
    for i in range(len(D)):
        del D[i][-1]

    while m in list(graph.nodes):
        m += 1

    # AdditivePhylogeny(D, n - 1)
    T = AdditivePhylogeny(D, n - 1, m)
    
    
    #v ← the (potentially new) node in T at distance x from i on the path between i and k 
    v = None

    path = nx.shortest_path(T, source=_i, target=_k)
    dist = 0
    for j in range(1, len(path) - 1):
        dist += T[path[j - 1]][path[j]]['weight']
        if dist == x:
            v = path[j]

    if v is None:
        v = m
        while v in list(T.nodes):
            v += 1
        dist = 0
        j = 0
        while dist < x:
            j += 1
            pdist = dist
            dist += T[path[j - 1]][path[j]]['weight']

        # add leaf n back to T by creating a limb (v, n) of length limbLength
        T.remove_edge(path[j - 1], path[j])
        T.add_edge(v, path[j], weight=dist - x)
        T.add_edge(v, path[j - 1], weight=x - pdist)

    T.add_edge(v, n - 1, weight=limbLength)

    return T


def print_weighted_adjacency_list(T):
    adj_dict = nx.to_dict_of_lists(T)
    output = []
    for k, value in adj_dict.items():
        for val in value:
            output.append(str(k) + '->' + str(val) + ':' + str(int(T[k][val]['weight'])))
    
    output.sort()
    return output

if __name__ == "__main__":
    with open('input.txt', 'r') as file:
        ins = file.read().splitlines()
        n = int(ins[0])
        D = []
        for line in ins[1:]:
            D.append([int(x) for x in line.split()])

    graph = nx.Graph()
    with open('output.txt', 'w') as file:
        outs = print_weighted_adjacency_list(AdditivePhylogeny(D, n, n))
        for out in outs:
            file.write(out+"\n")
    

    

