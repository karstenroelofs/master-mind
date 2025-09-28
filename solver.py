from z3 import Int, Solver, Ints, Bool, Sum, If
from typing import Iterable


class MasterMindSolver:
    secret_length: int
    colours: int
    history: list[tuple[tuple, tuple]]
    x: list
    s: Solver

    def __init__(self, secret_length=4, colours=6) -> None:
        self.secret_length = secret_length
        self.colours = colours
        self.history = []
        self.x = [
            [Bool(f"x_{i}_{j}") for j in range(self.colours)]
            for i in range(self.secret_length)
        ]
        self.s = Solver()

        # For each code peg, exactly one colour bool is true
        self.s.add(
            [
                self.sym_bool_sum([self.x[i][j] for j in range(colours)]) == 1
                for i in range(secret_length)
            ]
        )

    def add_result(self, query, response):
        self.history.append((query, response))
        self.add_constraints(query, response)

    def add_constraints(self, query, response):
        # The amount of correct pegs is equal to the amount of black pegs
        self.s.add(
            self.sym_bool_sum([self.x[i][query[i]] for i in range(self.secret_length)])
            == response[0],
        )
        self.s.add(
            Sum(
                [
                    self.sym_min(
                        query.count(c),
                        sum([self.x[i][c] for i in range(self.secret_length)]),
                    )
                    for c in range(self.colours)
                ]
            )
            == response[0] + response[1]
        )

    def get_valid_query(self):
        c = self.s.check()
        if c == "unsat":
            print("Unsat")
            return
        else:
            m = self.s.model()
            r = tuple(
                [m[self.x[i][j]] for j in range(self.colours)].index(True)
                for i in range(self.secret_length)
            )
            return r

    def sym_bool_sum(self, list: Iterable):
        return Sum(If(x, 1, 0) for x in list)

    def sym_min(self, x, y):
        return If(x < y, x, y)
