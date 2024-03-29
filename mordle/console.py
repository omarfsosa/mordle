import random

import click

from mordle import player
from mordle.corpus import Corpus
from mordle.game import Game, Result
from mordle.patterns import Pattern


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


@wordle.command("local")
@click.option("--auto", "plyr", flag_value="Bot", help="Let a bot play the game")
@click.option("--human", "plyr", flag_value="Human", help="Let a human play the game")
@click.option(
    "--semi", "plyr", flag_value="SemiHuman", help="Let a semi-human play the game"
)
@click.option("--answer", type=str, default="", help="Force the answer")
def local(plyr, answer):
    if not answer:
        answer = random.choice(Corpus())
    else:
        answer = answer.lower()

    game = Game(getattr(player, plyr)(), answer)
    game.run()


@wordle.command("online")
def online():
    bot = player.Bot()
    while True:
        click.echo(f"Best guess is {bot.best_guess}")
        click.echo("Top answers are:")
        top = bot.top_guesses(5)
        for n, word in enumerate(top):
            click.echo(f"{n}: {word} {bot.entropies.get(word):4.2f}")

        guess = click.prompt("guess: ").lower()[:5]
        values = click.prompt("pattern: ")
        values = [int(x) for x in values]
        result = Result(guess, Pattern(*values))
        if result.is_correct():
            break

        bot.update(result)
