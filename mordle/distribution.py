import json
import math
from collections import defaultdict
from pathlib import Path

from mordle.patterns import Pattern


def list_corpus():
    here = Path(__file__).resolve()
    path_data = here.parent.parent / "data" / "wordle-corpus.txt"
    with open(path_data, "r") as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


SIZE_CORPUS = len(list_corpus())


def _load_corpus_entropies_from_disk():
    here = Path(__file__).resolve()
    path_data = here.parent.parent / "data" / "entropies.json"
    with open(path_data, "r") as f:
        return json.load(f)


def make_search_condition(guess, pattern):
    def condition(word):
        pat = Pattern.from_words(guess, word)
        return pat == pattern

    return condition


def entropy(probabilities):
    return sum(p * math.log(1 / p, 2) for p in probabilities)


def calculate_entropies(options):
    num_options = len(options)
    if num_options == SIZE_CORPUS:
        try:
            return _load_corpus_entropies_from_disk()
        except FileNotFoundError:
            pass

    entropies = {}
    for guess in options:
        probas = defaultdict(lambda: 0)
        for answer in options:
            pattern = Pattern.from_words(guess, answer)
            # probas[pattern] += prior(answer) # if prior is not uniform
            probas[pattern] += 1 / num_options

        entropies[guess] = entropy(probas.values())

    return entropies
