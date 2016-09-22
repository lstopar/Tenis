from math import log, ceil

def _draw(start, end, rounds, player_ids):
    n = end - start + 1
    
    if n > 1: # at least 2 players
        middle = int((start + end) / 2)
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

def round_robin(player_ids):
    table = [player_id for player_id in player_ids]
    
    if len(player_ids) % 2 == 1:
        table = [None] + table

    n = len(table)
    n_by_2 = int(n/2)
    n_rounds = n-1

    rounds = []
    for round_n in range(n_rounds):
        curr_round = None

        if round_n % 2 == 0:
            curr_round = [(table[i], table[-1-i]) for i in range(n_by_2) if table[i] is not None]
        else:
            curr_round = [(table[n-i-1], table[i]) for i in range(n_by_2) if table[i] is not None]

        #print(str(curr_round))
        rounds.append(curr_round)
        
        # shift
        last = table[-1]
        for i in range(n-1,0,-1):
            table[i] = table[i-1]
        table[1] = last
    
    return rounds

    
n = 18
rounds = round_robin(range(n))
rounds_old = draw(range(n))

matches = n*(n-1) / 2

match_set = set()

print('ROUND ROBIN:')
for _round in rounds:
    print(str(_round))

    # check that no player appears twice in this round
    player_set = set()
    for match in _round:
        player_set.add(match[0])
        player_set.add(match[1])
        match_set.add((match[0],match[1]) if match[0] < match[1] else (match[1],match[0]))
    
    if len(player_set) != 2*len(_round):
        print('Player appeared twice in a round!!')

print('=========================================')

print('DIVIDE & CONQUER:')
for _round in rounds_old:
    print(str(_round))
        
print('Number of matches: ' + str(len(match_set)) + ', expected: ' + str(matches))
print('Correct number of matches: ' + str(len(match_set) == matches))
    
