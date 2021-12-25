import sys
sys.path.insert(0,'../')

from common import *

def find_pos(text, patterns, d):
    order = generate_suffix_array(text)
    bwt = build_bwt(text, order)        
    
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
    
    posions = []
    for pattern in patterns:
        posts = set()
        k = len(pattern) // (d+1)
        for p, offset in [(pattern[i*k:(i+1)*k], i*k) for i in range(d)] + [(pattern[d*k:len(pattern)], d*k)]:
            top = 0
            down = len(bwt) - 1
            curr = len(p) - 1
            while down >= top :
                if curr < 0:
                    for i in range(top, down + 1):
                        posts.add(order[i]-offset)
                    break
                else:
                    s = p[curr]
                    curr -= 1
                    if counts[s][down+1] - counts[s][top] > 0:
                        top = starts[s] + counts[s][top]
                        down = counts[s][down+1] + starts[s] - 1
                    else:
                        break
                    
        for pos in posts:
            if hamming_distance(text[pos:pos+len(pattern)], pattern, d):
                posions.append(pos)
    return posions
    
if __name__ == '__main__':
    data_path = 'input.txt'
    with open (data_path) as f:  
        data = f.read().strip().split()
        text = data[0] + '$'
        patterns = data[1:-1]
        d = int(data[-1])


    posions= find_pos(text, patterns, d)
    print(sorted(posions))
    f = open('output.txt', 'w')
    f.write(' '.join(map(str,sorted(posions))) )
    f.close()
    
