from random import randint

def score(motifs):
    def hamming_distance(s1, s2):
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))

    score = 0
    for i in range(len(motifs[0])):
        motif = ''.join([motifs[j][i] for j in range(len(motifs))])
        score += min([hamming_distance(motif, h*len(motif)) for h in 'ACGT'])
    return score

def profile(dna):
    dna_count = float(len(dna))
    array = []
    for i in range(len(dna[0])):
        col_i = [seq[i] for seq in dna]
        array.append([float(col_i.count(n) + 1)/float(dna_count + 4) for n in 'ACGT'])
    return [list(i) for i in zip(*array)]

def motfis(dna, k, array):
    pr = []
    for i in range(len(dna)-k+1):
        k_mer_pr = 1
        pattern = dna[i:i+k]
        for j in range(len(pattern)):
            profile = {'A': array[0][j], 'C': array[1][j], 'G': array[2][j], 'T': array[3][j]}
            k_mer_pr *= profile[pattern[j]]
        pr.append(k_mer_pr)
    i = pr.index(max(pr))
    maxKmer = dna[i:i+k]
    return maxKmer

def randomized_motif_search(dna, k):
    random_indices = [randint(0, len(dna[0]) - k) for i in range(len(dna))]
    motfis_list = [dna[i][j:j+k] for i, j in enumerate(random_indices)]
    best_motfis = motfis_list
    while True:
        tmp_profile = profile(motfis_list)
        tmp_motfis = [motfis(dna[i], k, tmp_profile) for i in range(len(dna))]
        if score(tmp_motfis) < score(best_motfis):
            best_motfis = tmp_motfis
        else:
            return best_motfis, score(best_motfis)

if __name__== "__main__":
    with open("input.txt", "r") as f:
        k, t= f.readline().strip().split(" ")
        k, t= int(k), int(t)
        dna = [x.strip() for x in f]

    res = []
    for i in range(0,t):
        res.append(randomized_motif_search(dna, k))

    res = sorted(res, key=lambda tup: tup[1])

    for i in res[0][0]:
        print (i)