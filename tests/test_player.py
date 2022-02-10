import pytest

from mordle.corpus import Corpus
from mordle.game import Game
from mordle.player import Bot


@pytest.fixture
def bot():
    return Bot()


@pytest.mark.parametrize("answer", Corpus())
def test_bot(bot, answer):
    game = Game(bot, answer)
    score = game.run(verbose=False)
    if answer not in ["goner", "watch"]:
        assert score <= 7
    else:
        assert score == 8
