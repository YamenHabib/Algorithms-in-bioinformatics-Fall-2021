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

def hamming_distance(s1, s2, d):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2)) <= d