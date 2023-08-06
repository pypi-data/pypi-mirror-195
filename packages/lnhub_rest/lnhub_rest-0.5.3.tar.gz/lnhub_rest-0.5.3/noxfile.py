import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    session.install(".[dev,test]")
    session.run(
        "pytest",
        "-s",
        "--cov=lnhub_rest",
        "--cov-append",
        "--cov-report=term-missing",
        env={"LN_SERVER_DEPLOY": "1", "LN_LOCAL_SUPABASE": "1"},
    )
    # session.run("coverage", "xml")


@nox.session
def supabase_stop(session: nox.Session) -> None:
    session.run("supabase", "db", "reset", external=True)
    session.run("supabase", "stop", external=True)
