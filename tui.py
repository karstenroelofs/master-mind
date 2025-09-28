from game import MasterMind
from pegs import CodePeg, KeyPeg
import random as r


class MasterMindTui:
    game: MasterMind
    secret_length: int
    colours: int

    def __init__(self, secret_length=4, colours=6):
        self.secret_length = secret_length
        self.colours = colours
        code = input("Code: ")
        if code == "random":
            code = tuple(r.choice(range(colours)) for _ in range(secret_length))
        elif len(code) == secret_length:
            code = tuple(int(x) for x in code)
        else:
            print("Invallid code")
            return
        self.game = MasterMind(code)

    def start(self):
        while True:
            self.print_state()
            query_str = input("Query: ")
            if len(query_str) == self.secret_length:
                query = tuple(int(x) for x in query_str)
                self.game.guess_int(query)
            else:
                print("Invallid query")

    def print_state(self):
        if self.game.results == (
            KeyPeg.BLACK,
            KeyPeg.BLACK,
            KeyPeg.BLACK,
            KeyPeg.BLACK,
        ):
            print("Game won!")
        else:
            for qs, rs in zip(self.game.guesses, self.game.results):
                print(
                    " ".join(str(q.value) for q in qs)
                    + " | "
                    + " ".join(str(r.value) for r in rs)
                )


if __name__ == "__main__":
    g = MasterMindTui()
    g.start()
