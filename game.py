from pegs import CodePeg, KeyPeg


class MasterMind:
    code: tuple[CodePeg, CodePeg, CodePeg, CodePeg]
    guesses: list[tuple[CodePeg, CodePeg, CodePeg, CodePeg]]
    results: list[list[KeyPeg]]

    def __init__(self, code: tuple[int, int, int, int]):
        self.code = self.__int_to_pegs(code)
        self.guesses = []
        self.results = []

    def guess(self, input: tuple[CodePeg, CodePeg, CodePeg, CodePeg]) -> list[KeyPeg]:
        self.guesses.append(input)
        guess_list = list(input)
        code_list = list(self.code)

        result = []

        # Black pegs
        for a, b in zip(input, self.code):
            if a == b:
                result.append(KeyPeg.BLACK)
                guess_list.remove(a)
                code_list.remove(a)
        if not guess_list:
            return result

        # White pegs
        for a in guess_list:
            if a in code_list:
                result.append(KeyPeg.WHITE)
                guess_list.remove(a)
                code_list.remove(a)

        self.results.append(result)
        return result

    def guess_int(self, input: tuple[int, int, int, int]) -> tuple[int, int]:
        result = self.guess(self.__int_to_pegs(input))
        return (result.count(KeyPeg.BLACK), result.count(KeyPeg.WHITE))

    def __int_to_pegs(
        self,
        input: tuple[int, int, int, int],
    ) -> tuple[CodePeg, CodePeg, CodePeg, CodePeg]:
        return (
            CodePeg(input[0]),
            CodePeg(input[1]),
            CodePeg(input[2]),
            CodePeg(input[3]),
        )


if __name__ == "__main__":
    g = MasterMind((1, 2, 3, 4))
    print(g.guess_int((1, 1, 1, 1)))
    print(g.guess_int((2, 1, 1, 1)))
