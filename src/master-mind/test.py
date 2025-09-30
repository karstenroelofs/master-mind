from solver import MasterMindSolver
from game import MasterMind
from game_cli import print_game_state

n, m = 10, 10
s = MasterMindSolver(n, m)
g = MasterMind([], n, m)

while not g.won:
    q = s.get_valid_query()
    r = g.guess(q)
    s.add_constraints(q, r)

print_game_state(g)
tries = len(g.guesses)
print(f"Tries: {tries}")
