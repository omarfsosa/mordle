import random
from dataclasses import dataclass, field

from mordle.corpus import Corpus
from mordle.patterns import Pattern
from mordle.player import SemiHuman


@dataclass
class Result:
    guess: str
    pattern: Pattern

    def is_correct(self):
        return all(x == 0 for x in self.pattern)

    def __str__(self):
        return self.pattern.display(self.guess.upper())


@dataclass
class Context:
    results: list = field(default_factory=list)


class Game:
    LIMIT_ATTEMPTS = 7

    def __init__(self, player, answer):
        self.player = player
        self._answer = answer.lower()
        self._context = Context()

    @property
    def context(self):
        return self._context

    def run(self, verbose=True):
        for attempt in range(1, Game.LIMIT_ATTEMPTS + 1):
            guess = self.player.respond(self.context).lower()
            pattern = Pattern.from_words(guess, self._answer)
            result = Result(guess, pattern)
            if verbose:
                print(attempt, result)

            if result.is_correct():
                break

            self.context.results.append(result)
            self.player.update(result)
        else:
            print(f"The answer was {self._answer}")
            attempt = Game.LIMIT_ATTEMPTS + 1

        return attempt


def simulate(n=1000, verbose=False):
    corpus = Corpus()
    scores = []
    for _ in range(n):
        player = SemiHuman()
        answer = random.choice(corpus)
        game = Game(player, answer)
        score = game.run(verbose=verbose)
        scores.append(score)

    return sum(scores) / n


if __name__ == "__main__":
    print(simulate(1, True))
