import web
import logging
import json
import math
import random as rand
from sets import Set
from lib.mwmatching import maxWeightMatching

#===============================================
# LOGGING
#===============================================

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

log = logging.getLogger('scheduler')
log.setLevel(logging.DEBUG)

#===============================================
# HANDLERS
#===============================================

def _transform(data):
    if log.isEnabledFor(logging.DEBUG):
        log.debug('transforming data ...')

    id_to_idx_h = {}
    idx_to_id_h = {}
    pair_cost_h = {}
    edges = []

    costs_arr = data
    rand.shuffle(costs_arr)     # shuffle to ensure random results if weights are the same

    curr_idx = 0
    used_pairs = Set()
    for el in costs_arr:
        id1 = el['id1']
        id2 = el['id2']
        cost = el['cost']

        # make id1 the smallest of the two IDs
        if id1 > id2:
            id1, id2 = id2, id1
            if log.isEnabledFor(logging.DEBUG):
                log.debug('Swapped ids, id1: ' + str(id1) + ', id2: ' + str(id2))

        pair = (id1,id2)

        if pair in used_pairs:
            raise ValueError('Match ' + str(pair) + ' appears twice!')
        if math.isnan(cost):
            raise ValueError('Cost for match ' + str((id1,id2)) + ' is NaN!')
        if cost < 0:
            raise ValueError('Cost for match ' + str((id1,id2)) + 'is negative!')
        if id1 == id2:
            raise ValueError('Player ' + id1 + ' is playing against himself!')


        if not id1 in id_to_idx_h:
            id_to_idx_h[id1] = curr_idx
            idx_to_id_h[curr_idx] = id1
            curr_idx += 1
        if not id2 in id_to_idx_h:
            id_to_idx_h[id2] = curr_idx
            idx_to_id_h[curr_idx] = id2
            curr_idx += 1

        i = id_to_idx_h[id1]
        j = id_to_idx_h[id2]

        if i > j:
            i,j = j,i

        w = -cost

        edges.append((i,j,w))
        pair_cost_h[pair] = cost

        used_pairs.add(pair)

    if log.isEnabledFor(logging.DEBUG):
        log.debug('Found ' + str(len(id_to_idx_h)) + ' nodes, ' + str(len(edges)) + ' edges ...')

    return edges, idx_to_id_h, pair_cost_h

def _match(edges):
    if log.isEnabledFor(logging.DEBUG):
        log.debug('matching ' + str(len(edges)) + ' edges ...')

    return maxWeightMatching(edges, maxcardinality=True)

def process_schedule(data):
    edges, idx_to_id_h, pair_cost_h = _transform(data)

    matches_arr = _match(edges)

    if log.isEnabledFor(logging.DEBUG):
        log.debug('transforming back ...')

    matches = []
    used_matches = Set()
    total_cost = 0
    for player1_n, player2_n in enumerate(matches_arr):
        if player2_n == -1:   # player 1 is not matched
            continue

        id1 = idx_to_id_h[player1_n]
        id2 = idx_to_id_h[player2_n]

        if id1 > id2:
            id1, id2 = id2, id1

        match = (id1,id2)
        if not match in used_matches:
            cost = pair_cost_h[match]
            used_matches.add(match)
            matches.append({ 'id1': id1, 'id2': id2, 'cost': cost })
            total_cost += pair_cost_h[match]

    result = { 'cost': total_cost, 'matches': matches }
    return result

#===============================================
# REST API
#===============================================

class schedule:
    def POST(self):
        global process_schedule

        try:
            data_str = web.data()

            if (log.isEnabledFor(logging.INFO)):
                log.info('received new request ...')

            data = json.loads(data_str)
            result = process_schedule(data)
            
            if log.isEnabledFor(logging.INFO):
                log.info('request processed, returning result ...')

            web.header('Content-Type', 'application/json')
            return json.dumps(result)
        except:
            log.exception('Exception while processing request!')


if __name__ == '__main__':
    urls = ('/', 'schedule')
    app = web.application(urls, globals())
    app.run()
