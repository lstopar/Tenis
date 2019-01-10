import sys
import os
import web
import logging
import json
import math
import time
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

log_dir = None

#===============================================
# GENERAL FUNCTIONS 
#===============================================

def _read_conf(fname):
    log.info('Reading configuration from file: \'' + fname + '\' ...')
    
    if not os.path.isfile(fname):
        print 'Configuration file: \'' + fname + '\' missing!'
        exit(2)

    f = open(fname, 'r')
    config_str = f.read()
    f.close()

    return json.loads(config_str)

def _log_data(data_str):
    log.info('Writing input data to directory: \'' + log_dir + '\'')
    fname = log_dir + str(time.time()).replace('.', '') + '-data.log'
    f = open(fname, 'w')
    f.write(data_str)
    f.flush()
    f.close()
    log.info('Data logged to file: ' + fname)

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

#===============================================
# HANDLERS
#===============================================

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
            matches.append({ 'id1': id1, 'id2': id2 })
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

            if log.isEnabledFor(logging.INFO):
                log.info('logging data ...')

            _log_data(data_str)

            data = json.loads(data_str)
            result = process_schedule(data)
            
            if log.isEnabledFor(logging.INFO):
                log.info('request processed, returning result ...')

            web.header('Content-Type', 'application/json')
            return json.dumps(result)
        except ValueError, e:
            _log_data(data_str)
            log.exception('Exception while processing request!')
            # web.output(str(e))
            raise web.badrequest(str(e))
        except:
            _log_data(data_str)
            log.exception('Exception while processing request!')
            raise web.internalerror()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'Usage: python server.py $CONF_FILE'
        exit(1)

    fname = sys.argv[1]
    config = _read_conf(fname)

    port = config['port']
    log_dir = config['log_dir']

    if not os.path.isdir(log_dir):
        print 'Log directory directory ' + log_dir + ' does not exist! Terminating!'
        exit(1)

    urls = ('/', 'schedule')
    app = web.application(urls, globals())
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
