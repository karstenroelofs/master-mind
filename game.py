import random as r


class MasterMind:
    code_length: int
    colours: int
    code: list[int]
    guesses: list[list[int]]
    results: list[tuple[int, int]]
    won: bool

    def __init__(self, code: list[int] = [], code_length=4, colours=6):
        if code == []:
            self.code = [r.choice(range(colours)) for _ in range(code_length)]
        elif len(code) == code_length and all(c in range(colours) for c in code):
            self.code = code
        else:
            raise ValueError("Invalid code provided")
        self.code_length = code_length
        self.colours = colours
        self.guesses = []
        self.results = []
        self.won = False

    def guess(self, input: list[int]) -> tuple[int, int]:
        if len(input) == self.code_length & all(
            c in range(self.colours) for c in input
        ):
            if input == self.code:
                self.won = True
                return (4, 0)
            self.guesses.append(input)

            black = sum(1 if a == b else 0 for a, b in zip(input, self.code))
            white = (
                sum(
                    min(input.count(c), self.code.count(c)) for c in range(self.colours)
                )
                - black
            )

            self.results.append((black, white))
            return (black, white)
        else:
            raise ValueError("Invalid query")
