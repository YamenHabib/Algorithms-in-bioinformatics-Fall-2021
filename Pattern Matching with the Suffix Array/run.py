import sys
sys.path.insert(0,'../')

from common import *


def search_patterns(text, patterns):
    suffix_array = generate_suffix_array(text)
    bwt = build_bwt(text, suffix_array)    
    
    counts = {}
    for char in ALPHABET:
        counts[char] = [0] * (len(text) + 1)
    
    for i in range(len(text)):
        curr = bwt[i]
        for c, _ in counts.items():
            counts[c][i+1] = counts[c][i]
        counts[curr][i+1] += 1
    
    idx = 0
    starts = {}
    for c in sorted(ALPHABET):
        starts[c] = idx
        idx += counts[c][len(text)]

    positions = set()
    
    for p in patterns:
        top = 0
        down = len(bwt) - 1
        idx = len(p) - 1
        while top <= down:
            if idx >= 0:
                s = p[idx]
                idx -= 1
                if counts[s][down+1] - counts[s][top] > 0:
                    top = starts[s] + counts[s][top]
                    down = starts[s] + counts[s][down+1] - 1
                else:
                    break
            else:
                for i in range(top, down + 1):
                    positions.add(suffix_array[i])
                break
    return positions
    
if __name__ == '__main__':
    data_path = 'input.txt'
    with open (data_path) as f:  
        data = f.read().strip().split()
        text = data[0] + '$'
        patterns = data[1:]

    positions= search_patterns(text, patterns)
    f = open('output.txt', 'w')
    f.write(' '.join(map(str,sorted(positions))) )
    f.close()
    