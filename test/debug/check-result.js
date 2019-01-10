
let req_str = process.argv[2];
let req_spl = req_str.split('\n');

let req = JSON.parse(req_spl[1])
let res = JSON.parse(req_spl[3])

let possible_pairs = req;
let matches = res.matches;
let service_cost = res.cost;

let costH = {};
for (let pair of possible_pairs) {
    let id1 = pair.id1;
    let id2 = pair.id2;
    let match_cost = pair.cost;

    if (!(id1 in costH)) { costH[id1] = {}; }
    if (!(id2 in costH)) { costH[id2] = {}; }

    if (id1 in costH[id2]) throw new Error('Cost for pair ' + id2 + ' vs ' + id1 + ' duplicated!');
    if (id2 in costH[id1]) throw new Error('Cost for pair ' + id1 + ' vs ' + id2 + ' duplicated!');

    costH[id1][id2] = match_cost;
    costH[id2][id1] = match_cost;
}

let actual_cost = 0;
for (let match of matches) {
    let id1 = match.id1;
    let id2 = match.id2;
    let match_cost = costH[id1][id2];
    actual_cost += match_cost;
}

if (actual_cost != service_cost) {
    console.error('Service output cost ' + service_cost + ' but actual cost is: ' + expected_cost);
    process.exit(1)
}

console.log('cost is: ' + actual_cost);
