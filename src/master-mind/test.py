from solver import MasterMindSolver

s = MasterMindSolver()

s.add_result((0, 1, 2, 3), (1, 0))
print(s.get_valid_query())
