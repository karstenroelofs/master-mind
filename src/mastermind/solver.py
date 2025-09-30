from z3 import Solver, Bool, Sum, If
from typing import Iterable


class MasterMindSolver:
    code_length: int
    colours: int
    history: list[tuple[tuple, tuple]]
    x: list
    s: Solver

    def __init__(self, code_length=4, colours=6) -> None:
        self.code_length = code_length
        self.colours = colours
        self.history = []
        self.x = [
            [Bool(f"x_{i}_{j}") for j in range(self.colours)]
            for i in range(self.code_length)
        ]
        self.s = Solver()

        self.s.add(
            [
                self.__sym_bool_sum([self.x[i][j] for j in range(colours)]) == 1
                for i in range(code_length)
            ]
        )

    def add_result(self, query, response):
        self.history.append((query, response))
        self.add_constraints(query, response)

    def add_constraints(self, query, response):
        self.s.add(
            self.__sym_bool_sum([self.x[i][query[i]] for i in range(self.code_length)])
            == response[0],
        )
        self.s.add(
            Sum(
                [
                    self.__sym_min(
                        query.count(c),
                        sum([self.x[i][c] for i in range(self.code_length)]),
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
            raise Exception("Unsat, don't know if / how this is possible")
        else:
            m = self.s.model()
            r = [
                [m[self.x[i][j]] for j in range(self.colours)].index(True)
                for i in range(self.code_length)
            ]
            return r

    def __sym_bool_sum(self, list: Iterable):
        return Sum(If(x, 1, 0) for x in list)

    def __sym_min(self, x, y):
        return If(x < y, x, y)
