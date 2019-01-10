
let pairs_str = process.argv[2];
let pairs_json = JSON.parse(pairs_str);

// console.log('pairs: ' + JSON.stringify(pairs_json));

let costH = {};
for (let pair of pairs_json) {
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

let player_ids = Object.keys(costH);
let total_players = player_ids.length;

let total_matches = Math.floor(total_players / 2);

let best_cost = Number.POSITIVE_INFINITY;

player_ids.sort();

console.log('total players: ' + total_players);
// console.log('player ids:\n' + JSON.stringify(player_ids));
// console.log('cost: ' + JSON.stringify(costH));

function cost(id1, id2) {
    return costH[id1][id2];
}

function findMatch(player_pool, matches, curr_cost) {
    if (player_pool.length <= 1) {
        if (curr_cost < best_cost) {
            // console.log('found best cost: ' + curr_cost + ' with matches:\n' + JSON.stringify(matches));
            // console.log('player pool: ' + JSON.stringify(player_pool));
            best_cost = curr_cost;
            best_matches = matches.map(function (match) { return match; })
        }
        return;
    }

    let id1 = player_pool.shift();

    for (let playerN = 0; playerN < player_pool.length; playerN++) {
        let id2 = player_pool.splice(playerN, 1)[0];
        matches.push({ id1: id1, id2: id2 });

        findMatch(player_pool, matches, curr_cost + cost(id1, id2));

        matches.pop();
        player_pool.splice(playerN, 0, id2);
    }

    player_pool.unshift(id1);
}

// function findMatch(player_pool, matches, curr_cost, rec_level) {
//     if (player_pool.length <= 1) {
//         if (curr_cost < best_cost) {
//             console.log('found best cost: ' + curr_cost);
//             // console.log('player pool: ' + JSON.stringify(player_pool));
//             best_cost = curr_cost;
//             best_matches = matches.map(function (match) { return match; })
//         }
//         return;
//     }

//     for (let player1N = 0; player1N < player_pool.length; player1N++) {
//         let id1 = player_pool.splice(player1N, 1)[0];
//         if (rec_level == 0) {
//             console.log('id1: ' + id1);
//         }
//         for (let playerN = 0; playerN < player_pool.length; playerN++) {
//             let id2 = player_pool.splice(playerN, 1)[0];
//             matches.push({ id1: id1, id2: id2 });

//             findMatch(player_pool, matches, curr_cost + cost(id1, id2), rec_level+1);

//             matches.pop();
//             player_pool.splice(playerN, 0, id2);
//         }
//         player_pool.splice(player1N, 0, id1);
//     }
// }

function findBest() {
    let matches = [];
    let best_cost = findMatch(player_ids, matches, 0, 0)
}

findBest();

console.log('\n\ndone!');
console.log('best cost: ' + best_cost);
console.log('best matches: ' + JSON.stringify(best_matches));
