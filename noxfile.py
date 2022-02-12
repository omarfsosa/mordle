import nox

locations = "mordle", "tests", "noxfile.py"
nox.options.sessions = "lint", "test"


@nox.session
def lint(session):
    """Lint python source"""
    args = session.posargs or locations
    session.install("black", "flake8", "isort")
    session.run("black", "--check", *args)
    session.run("flake8", *args)
    session.run("isort", "--check", *args)


@nox.session(name="format")
def format_(session):
    args = session.posargs or locations
    session.install("black", "isort")
    session.run("black", *args)
    session.run("isort", *args)


@nox.session
def test(session):
    """Run the tests"""
    session.install("pytest", ".")
    session.run("pytest")
