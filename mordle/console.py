import click
import random

from mordle.corpus import Corpus
from mordle.game import Game
from mordle import player


@click.group()
@click.version_option()
def wordle():
    """
    Wordle in Python!\n
    -----------------\n
    You have 7 chances to find the hidden word.
    The hidden word has 5 letters and it's an
    English word.
    Progress is displayed in UPPER-CASE letters but
    the game is not case sensitive.
    """


@wordle.command("play")
@click.option("--auto", "plyr", flag_value="Bot", help="Let a bot play the game")
@click.option("--human", "plyr", flag_value="Human", help="Let a human play the game")
@click.option("--semi", "plyr", flag_value="SemiHuman", help="Let a semi-human play the game")
@click.option("--answer", type=str, default="", help="Force the answer")
def new_game(plyr, answer):
    if not answer:
        answer = random.choice(Corpus())
    else:
        answer = answer.lower()

    game = Game(getattr(player, plyr)(), answer)
    game.run()
