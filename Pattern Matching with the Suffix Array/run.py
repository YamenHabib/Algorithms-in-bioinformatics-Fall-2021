ALPHABET = ['$', 'A', 'C', 'G', 'T']

def generate_suffix_array(text):
    """
    Build suffix array of the string text 
    res[i] is the index in text where the i-th lexicographically smallest suffix starts.

    AATCGGGTTCAATCGGGGT        sorted to        AATCGGGGT [10]
    ATCGGGTTCAATCGGGGT                          AATCGGGTTCAATCGGGGT [0]
    TCGGGTTCAATCGGGGT                           ATCGGGGT [11]
    CGGGTTCAATCGGGGT                            ATCGGGTTCAATCGGGGT [1]
    GGGTTCAATCGGGGT                             CAATCGGGGT [9]
    GGTTCAATCGGGGT                              CGGGGT [13]
    GTTCAATCGGGGT                               .
    TTCAATCGGGGT                                .
    TCAATCGGGGT                                 .
    CAATCGGGGT
    AATCGGGGT
    ATCGGGGT
    TCGGGGT
    CGGGGT
    GGGGT
    GGGT
    GGT
    GT
    T

    """
    suffexis = []
    for i in range(len(text)):
        suffexis.append((text[i:], i))
    suffexis = sorted(suffexis, key=lambda x: x[0])
    order = [x[1] for x in suffexis]
    return order


def build_bwt(text, suffix_array):
    """
        Burrows-Wheeler Transform rearranges a character string into runs of similar characters.
    """

    bwt = [''] * len(text)
    
    # Burrows-Wheeler Transform
    for i in range(len(text)):
        bwt[i] = text[(suffix_array[i] + len(text) - 1) % len(text)]
    
    return bwt


def search_patterns(text, patterns):
    suffix_array = generate_suffix_array(text)
    bwt = build_bwt(text, suffix_array)    
    
    counts = dict()
    starts = dict()
    
    for char in ALPHABET:
        counts[char] = [0] * (len(text) + 1)
    
    for i in range(len(text)):
        curr = bwt[i]
        for c, count in counts.items():
            counts[c][i+1] = counts[c][i]
        counts[curr][i+1] += 1
    
    idx = 0
    
    for c in sorted(ALPHABET):
        starts[c] = idx
        idx += counts[c][len(text)]

    occs = set()
    
    for p in patterns:
        top = 0
        bottom = len(bwt) - 1
        idx = len(p) - 1
        while top <= bottom:
            if idx >= 0:
                s = p[idx]
                idx -= 1
                if counts[s][bottom+1] - counts[s][top] > 0:
                    top = starts[s] + counts[s][top]
                    bottom = starts[s] + counts[s][bottom+1] - 1
                else:
                    break
            else:
                for i in range(top, bottom + 1):
                    occs.add(suffix_array[i])
                break
    return occs
    
if __name__ == '__main__':
    data_path = 'input.txt'
    with open (data_path) as f:  
        data = f.read().strip().split()
        text = data[0] + '$'
        patterns = data[1:]

    occs= search_patterns(text, patterns)
    f = open('output.txt', 'w')
    f.write(' '.join(map(str,sorted(occs))) )
    f.close()
    