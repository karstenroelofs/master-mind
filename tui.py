from game import MasterMind


class MasterMindTui:
    game: MasterMind
    code_length: int
    colours: int

    def __init__(self, code_length=4, colours=6):
        self.code_length = code_length
        self.colours = colours
        self.game = MasterMind(self.get_code(), code_length, colours)

    def get_code(self) -> list[int]:
        code = []
        while not code:
            input_str = input("Code: ")
            if input_str in ["random", "r", ""]:
                return []
            elif len(input_str) == self.code_length and all(
                int(c) in range(self.colours) for c in input_str
            ):
                return [int(c) for c in input_str]
            else:
                print(f"Invalid code {input_str}, please try again")
        return []

    def start(self):
        while not self.game.won:
            self.print_state()
            query_str = input("Query: ")
            if len(query_str) == self.code_length and all(
                int(c) in range(self.colours) for c in query_str
            ):
                query = [int(x) for x in query_str]
                self.game.guess(query)
            else:
                print("Invalid query")
        print("Game won!")

    def print_state(self):
        for qs, rs in zip(self.game.guesses, self.game.results):
            print(" ".join(str(q) for q in qs) + " | " + " ".join(str(r) for r in rs))


def print_game_state(game: MasterMind):
    for qs, rs in zip(game.guesses, game.results):
        print(" ".join(str(q) for q in qs) + " | " + " ".join(str(r) for r in rs))


if __name__ == "__main__":
    g = MasterMindTui(6, 10)
    g.start()
