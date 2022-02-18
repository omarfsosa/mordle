import abc
import heapq
import json
import math
from collections import defaultdict
from pathlib import Path

from tqdm.auto import tqdm

from mordle.corpus import SIZE, Corpus
from mordle.patterns import Pattern


def _load_corpus_entropies_from_disk():
    """
    Load a pre-computed file with entropies
    for the whole corpus. Assuming uniform
    prior probabilities on each word.
    """
    pkg = Path(__name__).resolve()
    path_data = pkg.parent / "mordle" / "data" / "entropies.json"
    with open(path_data, "r") as f:
        return json.load(f)


def entropy(probabilities):
    return sum(p * math.log(1 / p, 2) for p in probabilities)


def calculate_entropies(corpus):
    num_options = len(corpus)
    if num_options == SIZE:
        try:
            return _load_corpus_entropies_from_disk()
        except FileNotFoundError:
            pass

    entropies = {}
    for guess in tqdm(corpus):
        probas = defaultdict(lambda: 0)
        for answer in corpus:
            pattern = Pattern.from_words(guess, answer)
            # probas[pattern] += prior(answer) # if prior is not uniform
            probas[pattern] += 1 / num_options

        entropies[guess] = entropy(probas.values())

    return entropies


class Player(abc.ABC):
    @abc.abstractmethod
    def respond(self, context):
        """
        Return 5 letter word given the game context.
        """

    @abc.abstractmethod
    def update(self, result):
        """
        Update any player attributes given
        the result of the last trial.
        """


class Bot(Player):
    def __init__(self):
        self.corpus = Corpus()
        self.entropies = calculate_entropies(self.corpus)

    @property
    def best_guess(self):
        return max(self.entropies, key=self.entropies.get)

    def top_guesses(self, n):
        return sorted(self.entropies, key=self.entropies.get, reverse=True)[:n]

    def update(self, result):
        guess, pattern = result.guess, result.pattern
        self.corpus = self.corpus.reduce(guess, pattern)
        self.entropies = calculate_entropies(self.corpus)

    def respond(self, context):
        return self.best_guess


class Human(Player):
    def respond(self, result):
        return input("Your guess: ")

    def update(self, context):
        pass


class SemiHuman(Player):
    def __init__(self):
        self.bot = Bot()
        self.human = Human()

    def respond(self, context):
        self.show_best_options()
        return self.human.respond(context)

    def update(self, result):
        self.bot.update(result)
        self.human.update(result)

    def show_best_options(self):
        best_options = heapq.nlargest(5, self.bot.entropies, key=self.bot.entropies.get)
        indent = " " * 4
        for option in best_options:
            print(f"{indent}{option}: {self.bot.entropies[option]:3.2f}")
