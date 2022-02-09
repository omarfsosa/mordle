import random
from mordle.patterns import Pattern
from mordle.distribution import list_corpus, calculate_entropies, make_search_condition


class Bot:
    def __init__(self):
        self.guesses = []
        self.patterns = []
        self.options = list_corpus()

    @property
    def entropies(self):
        return calculate_entropies(self.options)

    @property
    def best_guess(self):
        return max(self.entropies, key=self.entropies.get)

    def update_options(self):
        guess, pattern = self.guesses[-1], self.patterns[-1]
        condition = make_search_condition(guess, pattern)
        options = [word for word in self.options if condition(word)]
        self.options = options

    def respond(self):
        return self.best_guess


class Game:
    LIMIT_ATTEMPTS = 7

    def __init__(self, player, answer):
        self.player = player
        self._answer = answer

    def run(self, verbose=True):
        for attempt in range(1, Game.LIMIT_ATTEMPTS + 1):
            guess = self.player.respond()
            pattern = Pattern.from_words(guess, self._answer)
            self.player.guesses.append(guess)
            self.player.patterns.append(pattern)
            self.player.update_options()
            if verbose:
                print(attempt, pattern.display(guess), pattern)
            if all(x == 0 for x in pattern):
                break

        return attempt


def simulate(n=1000):
    corpus = list_corpus()
    scores = []
    for _ in range(n):
        player = Bot()
        answer = random.choice(corpus)
        game = Game(player, answer)
        score = game.run(verbose=False)
        scores.append(score)

    return sum(scores) / n


if __name__ == "__main__":
    print(simulate(100))
