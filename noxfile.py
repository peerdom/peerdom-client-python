import nox


@nox.session
def tests(session):
    session.install("pytest")
    session.install("pytest-cov")
    session.install("pytest-random-order")
    session.run("pip", "install", "-e", ".")
    session.run("pytest", "tests/")
