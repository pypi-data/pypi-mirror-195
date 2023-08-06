import argparse
from subprocess import run
from typing import Literal, Optional

import sqlmodel as sqm
from lamin_logger import logger
from packaging.version import parse as vparse
from typeguard import typechecked

description_cli = "Migrate hub."
parser = argparse.ArgumentParser(
    description=description_cli, formatter_class=argparse.RawTextHelpFormatter
)
subparsers = parser.add_subparsers(dest="command")

# migrate
migr = subparsers.add_parser("migrate")
aa = migr.add_argument
aa("action", choices=["generate", "deploy"], help="Generate migration.")
aa(
    "--breaks-lndb",
    choices=["y", "n"],
    default=None,
    help="Specify whether migration will break lndb (y/n).",
)

# parse args
args = parser.parse_args()


def generate():
    run(
        "alembic --config lnhub_rest/schema/alembic.ini --name cbwk revision"
        " --autogenerate -m 'vX.X.X.'",
        shell=True,
    )


@typechecked
def deploy(breaks_lndb: Optional[Literal["y", "n"]] = None):
    from lndb import settings

    from lnhub_rest._engine import engine
    from lnhub_rest.schema import __version__, _migration
    from lnhub_rest.schema.versions import version_cbwk

    if len(__version__.split(".")) != 3:
        raise RuntimeError("Your __version__ string is not of form X.X.X")

    if breaks_lndb is None:
        raise SystemExit("Error: Pass --breaks-lndb y or --breaks-lndb n")

    if breaks_lndb:
        response = input(
            "Have you ensured that lndb and lamindb have releases on PyPI that users"
            " can pull?"
        )
        if response == "y":
            pass
        else:
            raise SystemExit(
                "Please test thoroughly and prepare releases for lndb and lamindb.\n"
                "Pin lnhub_rest in lamindb, set a lower bound in lndb."
            )

    if settings.user.handle.startswith(("test", "static-test")):
        raise SystemExit("Error: Log in with your developer handle, e.g., falexwolf")

    # check that a release was made
    with sqm.Session(engine) as ss:
        deployed_v = ss.exec(
            sqm.select(version_cbwk.v)
            .order_by(version_cbwk.v.desc())  # type: ignore
            .limit(1)
        ).one()
    if deployed_v == __version__:
        raise SystemExit("Error: Make a new release before deploying the migration!")
    if vparse(deployed_v) > vparse(__version__):
        raise RuntimeError(
            "The new version has to be greater than the deployed version."
        )

    process = run(
        "alembic --config lnhub_rest/schema/alembic.ini --name cbwk upgrade head",
        shell=True,
    )
    if process.returncode == 0:
        with sqm.Session(engine) as ss:
            ss.add(
                version_cbwk(
                    v=__version__,
                    migration=_migration,
                    user_id=settings.user.id,
                    breaks_lndb=(breaks_lndb == "y"),
                )
            )
            ss.commit()

        logger.success("Successfully migrated hub.")


def main():
    if args.command == "migrate":
        if args.action == "generate":
            generate()
        if args.action == "deploy":
            deploy(breaks_lndb=args.breaks_lndb)
    else:
        logger.error("Invalid command. Try `lndb -h`.")
        return 1
