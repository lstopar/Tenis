import web
import logging
import json
import math
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
    id_to_idx_h = {}
    pair_cost_h = {}
    edges = []

    costs_arr = data
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
            curr_idx += 1
        if not id2 in id_to_idx_h:
            id_to_idx_h[id2] = curr_idx
            curr_idx += 1

        i = id_to_idx_h[id1]
        j = id_to_idx_h[id2]
        w = -cost

        edges.append((i,j,w))
        pair_cost_h[pair] = cost

        used_pairs.add(pair)
    return edges, id_to_idx_h, pair_cost_h

def process_schedule(data):
    edges, id_to_idx_h, pair_cost_h = _transform(data)

    log.info('Edges:\n' + str(edges))

    matches_arr = maxWeightMatching(edges, maxcardinality=True)

    if log.isEnabledFor(logging.DEBUG): # TODO write this to file
        log.debug('Generated matches: ' + str(matches_arr))

    matches = []
    used_matches = Set()
    total_cost = 0
    for player1_n, player2_n in enumerate(matches_arr):
        if player2_n == -1:   # player 1 is not matched
            continue

        id1 = id_to_idx_h[player1_n]
        id2 = id_to_idx_h[player2_n]

        if id1 > id2:
            id1, id2 = id2, id1

        match = (id1,id2)
        if not match in used_matches:
            used_matches.add(match)
            matches.append((id1, id2))
            total_cost += pair_cost_h[(id1,id2)]

    result = { 'cost': total_cost, 'matches': matches }
    if log.isEnabledFor(logging.DEBUG):
        log.debug('Generated result:\n' + str(result))
    return result

#===============================================
# REST API
#===============================================

class schedule:
    def POST(self):
        global process_schedule

        try:
            data_str = web.data()

            if log.isEnabledFor(logging.DEBUG):
                log.debug('Processing request, data=' + data_str + ' ...')      # TODO write this to file

            data = json.loads(data_str)
            
            result = process_schedule(data)

            web.header('Content-Type', 'application/json')

            return json.dumps(result)
        except:
            log.exception('Exception while processing request!')


if __name__ == '__main__':
    urls = ('/', 'schedule')
    app = web.application(urls, globals())
    app.run()
