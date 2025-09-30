from solver import MasterMindSolver
from game import MasterMind
from game_cli import print_game_state
from itertools import product
import json
from statistics import mean

max_n, max_m = 10, 10
sample_size = 10

log = {}

for n, m in product(range(1, max_n), range(1, max_m)):
    all_tries = []
    for _ in range(sample_size):
        s = MasterMindSolver(n, m)
        g = MasterMind([], n, m)

        while not g.won:
            q = s.get_valid_query()
            r = g.guess(q)
            s.add_constraints(q, r)

        print_game_state(g)
        tries = len(g.guesses)
        print(f"Tries: {tries}")
        all_tries.append(tries)
    growing_avg = [mean(all_tries[:i]) for i in range(1, sample_size)]
    print(growing_avg)
    log[f"{n}_{m}"] = growing_avg

with open("data.json", "w") as f:
    json.dump(log, f)
