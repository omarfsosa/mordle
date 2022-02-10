from pathlib import Path

from mordle.patterns import Pattern


def _load():
    """
    Load the full corpus from file,
    """
    pkg = Path(__name__).resolve()
    path_data = pkg.parent / "mordle" / "data" / "wordle-corpus.txt"
    with open(path_data, "r") as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


SIZE = len(_load())


class Corpus:
    def __init__(self, words=None):
        self._words = list(words or _load())

    def __getitem__(self, index):
        return self._words[index]

    def __iter__(self):
        return iter(self._words)

    def __len__(self):
        return len(self._words)

    def reduce(self, guess, pattern):
        """
        Filter out the words for which the
        `guess` does not match the `pattern`.
        """

        def condition(word):
            pat = Pattern.from_words(guess, word)
            return pat == pattern

        return Corpus(w for w in self if condition(w))
