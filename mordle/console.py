import click
import random

from mordle.corpus import Corpus
from mordle.player import Bot, Human
from mordle.game import Game


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
@click.option("--auto", is_flag=True, default=False, help="Let a bot play the game")
@click.option("--answer", type=str, default="", help="Force the answer")
def new_game(auto, answer):
    if not answer:
        answer = random.choice(Corpus())
    else:
        answer = answer.lower()

    if auto:
        player = Bot()
    else:
        player = Human()

    game = Game(player, answer)
    game.run()
