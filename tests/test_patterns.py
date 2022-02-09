import pytest

from mordle.patterns import Pattern


@pytest.mark.parametrize("values", [(0, 0, 0, 0, 0)])
def test_new(values):
    with pytest.raises(AssertionError):
        Pattern(0, 1, 2, 1, 3)

    with pytest.raises(AssertionError):
        Pattern(0, 1, "a", 1, 1)

    with pytest.raises(AssertionError):
        Pattern(0, 0, 0, 0, 0, 0)

    pattern = Pattern(0, 0, 0, 0, 0)
    assert all(p == 0 for p in pattern)


@pytest.mark.parametrize(
    argnames=["answer", "guess", "pattern"],
    argvalues=[
        ("abbey", "abbey", (0, 0, 0, 0, 0,)),
        ("abbey", "algae", (0, 2, 2, 2, 1,)),
        ("abbey", "keeps", (2, 1, 2, 2, 2,)),
        ("abbey", "orbit", (2, 2, 0, 2, 2,)),
        ("abbey", "abate", (0, 0, 2, 2, 1,)),
        ("abbey", "bbbbb", (2, 0, 0, 2, 2,)),
        ("mouse", "ooxxx", (2, 0, 2, 2, 2,)),
        ("mouse", "xooxx", (2, 0, 2, 2, 2,)),
        ("mouse", "xxoox", (2, 2, 1, 2, 2,)),
        ("mouse", "oxoxx", (1, 2, 2, 2, 2,)),
    ]
)
def test_from_words(answer, guess, pattern):
    result = Pattern.from_words(guess, answer)
    assert result == Pattern(*pattern)
