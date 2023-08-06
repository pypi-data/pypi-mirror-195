from argparse import ArgumentParser
from typing import Any

from linkedincv.cli.command import build
from linkedincv.constants import Routes


def main() -> None:

    parser = ArgumentParser(description="CLI for the linkedin-cv package.")

    parser.set_defaults(method=dispatch)

    parser.add_argument(
        "--config",
        "-c",
        dest="config_file",
        help="The profile json file",
    )

    args = parser.parse_args()
    args.method(**vars(args))


def dispatch(
    config_file: str = "",
    **kwargs: Any,  # type: ignore
) -> None:

    build(Routes.TEX_ENTRY_POINT, Routes.OUT_FOLDER)
