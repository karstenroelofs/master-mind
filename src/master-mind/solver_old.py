from sys import getunicodeinternedsize
from z3 import Int, Solver, Ints
from game import MasterMind
from pegs import KeyPeg, CodePeg
from itertools import permutations, product

eq = lambda a, b: a == b
neq = lambda a, b: a != b


class MasterMindSolver:
    guesses = []
    results = []

    c1, c2, c3, c4 = Ints("c1 c2 c3 c4")

    s = Solver()

    def __init__(self) -> None:
        pass

    def add_result(self, guess, result):
        self.guesses.append(guess)
        self.results.append(result)

    def add_constraints(self, guess, result):
        match result:
            #
            case []:
                for peg in set(guess):
                    self.s.add(self.c1 != peg)
                    self.s.add(self.c2 != peg)
                    self.s.add(self.c3 != peg)
                    self.s.add(self.c4 != peg)
            # 0
            case [0]:
                self.s.add(
                    all(
                        [
                            any(
                                [
                                    all([op(getattr(self, f"c{1}"), peg) for op in ops])
                                    for ops in permutations([eq, neq, neq, neq])
                                ]
                            )
                            for peg in guess
                        ]
                    )
                )
                # for peg in set(guess):
                #     self.s.add(
                #         (
                #             self.c1
                #             == peg & self.c2
                #             != peg & self.c3
                #             != peg & self.c4
                #             != peg
                #         )
                #         | (
                #             self.c1
                #             != peg & self.c2
                #             == peg & self.c3
                #             != peg & self.c4
                #             != peg
                #         )
                #         | (
                #             self.c1
                #             != peg & self.c2
                #             != peg & self.c3
                #             == peg & self.c4
                #             != peg
                #         )
                #         | (
                #             self.c1
                #             != peg & self.c2
                #             != peg & self.c3
                #             != peg & self.c4
                #             == peg
                #         )
                #     )

            # 00
            case [0, 0]:
                self.s.add(
                    all(
                        [
                            any(
                                [
                                    all([op(getattr(self, f"c{1}"), peg) for op in ops])
                                    for ops in permutations([eq, eq, neq, neq])
                                ]
                            )
                            for peg in guess
                        ]
                    )
                )
            # 000
            case [0, 0, 0]:
                self.s.add(
                    all(
                        [
                            any(
                                [
                                    all([op(getattr(self, f"c{1}"), peg) for op in ops])
                                    for ops in permutations([eq, eq, eq, neq])
                                ]
                            )
                            for peg in guess
                        ]
                    )
                )
            # 0000
            case [0, 0, 0, 0]:
                self.s.add(
                    any(
                        [
                            self.c1
                            == col1 & self.c2
                            == col2 & self.c3
                            == col3 & self.c4
                            == col4
                            for (col1, col2, col3, col4) in permutations(guess)
                        ]
                    )
                )
            # 1
            case [1]:
                self.s.add(
                    any(
                        [
                            all(
                                [
                                    op(getattr(self, f"c{i + 1}"), guess[i])
                                    for i, op in enumerate(ops)
                                ]
                            )
                            for ops in permutations([eq, neq, neq, neq])
                        ]
                    )
                )
            # 11
            case [1, 1]:
                self.s.add(
                    any(
                        [
                            all(
                                [
                                    op(getattr(self, f"c{i + 1}"), guess[i])
                                    for i, op in enumerate(ops)
                                ]
                            )
                            for ops in permutations([eq, eq, neq, neq])
                        ]
                    )
                )
            # 111
            case [1, 1, 1]:
                self.s.add(
                    any(
                        [
                            all(
                                [
                                    op(getattr(self, f"c{i + 1}"), guess[i])
                                    for i, op in enumerate(ops)
                                ]
                            )
                            for ops in permutations([eq, eq, eq, neq])
                        ]
                    )
                )
            # 10
            # One of the pegs is the correct colour and in the correct place
            # And, of the other pegs is the correct colour and not in the correct place
            case [1, 0]:
                self.s.add(
                    any(
                        [
                            all(
                                [
                                    op(getattr(self, f"c{i + 1}"), guess[i])
                                    for i, op in enumerate(ops)
                                ]
                            )
                            for ops in permutations([eq, eq, eq, neq])
                        ]
                    )
                )
            # 100
            # 1000
            # 110
            # 1100
            # 1110

    def check_sat(self):
        if self.s.check() == "sat":
            m = self.s.model()
            print(f"{m[self.c1]} {m[self.c2]} {m[self.c3]} {m[self.c4]}")
        else:
            print("No certainty yet")
