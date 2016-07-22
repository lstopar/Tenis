from math import log, ceil

def _draw(start, end, rounds, player_ids):
    n = end - start + 1
    
    if n > 1: # at least 2 players
        middle = (start + end) / 2
        l1 = middle - start + 1
        l2 = end - middle
        n_rounds = max(l1, l2)
        
        # divide
        offset1 = _draw(start, middle, rounds, player_ids)
        offset2 = _draw(middle+1, end, rounds, player_ids)
        
        # conquer
        round_offset = max(offset1, offset2) + 1# = (1 << (int(ceil(log(n, 2))) - 1)) - 1
        max_round = 0;
        for i in range(l1):
            for j in range(l2):
                diff = i - j
                local_round = diff % n_rounds
                _round = local_round + round_offset
                rounds[_round].append((player_ids[start + i], player_ids[middle + j + 1]))
                if _round > max_round:
                    max_round = _round
                    
        return max_round
    else:
        return -1

def draw(player_ids):
    n_players = len(player_ids)
    max_depth = int(ceil(log(n_players, 2)))
    
    possible_rounds = (1 << (max_depth)) - 1
    rounds = [[] for _ in range(possible_rounds)]
    
    _draw(0, n_players - 1, rounds, player_ids)
    
    return rounds
    
n = 7
rounds = draw(range(n))

matches = n*(n-1) / 2
count = 0

for _round in rounds:
    print(str(_round))
    for match in _round:
        count += 1
        
print('Number of matches: ' + str(count) + ', expected: ' + str(matches))
print('Correct number of matches: ' + str(count == matches))
    
