def get_kmer_for_dna(dna, k):
    k_mers = []
    for i in range(len(dna)-(k-1)):
        k_mer= dna[i:i+k]
        k_mers.append(k_mer)
    return k_mers

def get_all_kmer(dnas, k):
    k_mers = []
    for dna in dnas:
        for i in range(len(dna)-(k-1)):
            k_mer= dna[i:i+k]
            k_mers.append(k_mer)
    return k_mers

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def cal_min_kmer_dna(kmer, dna, k):
    d= 100000
    patterns= get_kmer_for_dna(dna, k)
    for p_ in patterns:
        lc= hamming_distance(kmer, p_)
        if lc < d:
            d = lc
    return d

def cal_min_kmer_dnas(kmer, dnas, k):
    ans= 0
    for dna in dnas:
        ans+=  cal_min_kmer_dna(kmer, dna, k)
    return ans

if __name__=="__main__":
    dnas = []
    with open("input.txt", "r") as f:
        k = int(f.readline())
        for x in f:
            dnas.append(x.strip())
    
    
    kmers = get_all_kmer(dnas, k)
    best= None
    d= 1000000
    for kmer in kmers:
        lc= cal_min_kmer_dnas(kmer, dnas, k)  
        if lc < d:
            d = lc
            best= kmer

    print(best)