import itertools


class BGColour:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def coloured(x, colour):
    return f"{colour}{x}{BGColour.ENDC}"


def _yellow(x):
    return coloured(x, BGColour.WARNING)


def _green(x):
    return coloured(x, BGColour.OKGREEN)


class Pattern(tuple):
    """
    A sequence of indicator integers.
    Matched:   0 (Green)
    Misplaced: 1 (Yellow)
    Failed:    2 (Black)
    """

    SIZE = 5

    def __new__(cls, *args):
        assert all(x in (0, 1, 2) for x in args)
        assert len(args) == Pattern.SIZE
        return super().__new__(cls, args)

    def __repr__(self):
        squares = "🟩🟨⬛"
        return "".join(squares[x] for x in self)

    @classmethod
    def from_words(cls, guess, answer):
        return cls(*Pattern._generate_comparison(guess, answer))

    @staticmethod
    def _generate_comparison(guess, answer):
        is_exact = [g == a for a, g in zip(guess, answer)]
        remaining = [w for exact, w in zip(is_exact, answer) if not exact]
        for exact, g in zip(is_exact, guess):
            if exact:
                yield 0
            elif g in remaining:
                remaining.remove(g)
                yield 1
            else:
                yield 2

    def display(self, guess):
        funcs = {0: _green, 1: _yellow, 2: lambda x: x}
        return "".join(funcs[value](letter) for value, letter in zip(self, guess))

    @staticmethod
    def iterpatterns():
        values = (0, 1, 2)
        repeat = 5
        for prod in itertools.product(values, repeat=repeat):
            yield Pattern(*prod)


if __name__ == "__main__":
    answer = "abbey"
    for guess in ("algae", "keeps", "orbit", "abate", "bxxbb", "abbey"):
        pat = Pattern.from_words(guess, answer)
        print(guess, pat.display(guess), pat)

    answer = "mouse"
    for guess in ("ooxxx",):
        pat = Pattern.from_words(guess, answer)
        print(guess, pat.display(guess), pat)
