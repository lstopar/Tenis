import sys
import json
import random as rand
from sets import Set

def has_static_points(lst):
    for i in xrange(len(lst)):
        if i == lst[i]:
            return True
    return False

if len(sys.argv) <= 2:
    print 'Usage: python gen_test.py $N_PLAYERS $FNAME'
    exit(1)

n = int(sys.argv[1])
fname = sys.argv[2]

edges = []

min_wgt = .1
eps = .05

players = range(n)
scheduled = [-1 for _ in range(n)]
has_pair = [False for _ in range(n)]

rand.shuffle(players)

while len(players) > 0:
    i = players.pop()
    j = players.pop()
    
    scheduled[i] = j
    scheduled[j] = i

used_players = Set()
used_pairs = Set()
for i,j in enumerate(scheduled):
    if i in used_players or j in used_players:
        continue

    p0 = i
    p1 = j
    if p0 > p1:
        p0,p1 = p1,p0
    edges.append((p0,p1,min_wgt))
    used_players.add(i)
    used_players.add(j)
    used_pairs.add((p0,p1))

for i in range(n):
    for j in range(i+1,n):
        pair = (i,j)
        if not pair in used_pairs:
            edges.append((i,j,min_wgt + rand.random() + eps))

# save JSON
edges_json = []
for i,j,wgt in edges:
    edges_json.append({ 'id1': i, 'id2': j, 'cost': wgt })

f = open(fname, 'w')
f.write(json.dumps(edges_json, sort_keys=True, indent=4, separators=(',', ': ')))
f.flush()
f.close()
