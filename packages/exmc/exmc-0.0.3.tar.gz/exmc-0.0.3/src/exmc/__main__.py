"""Command-line interface."""
import argparse

from exmc.convert import run


def main() -> None:
    """Excel Markdown Converter."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="print origin text from excel or markdown",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        help="convert markdown table str to excel str",
        action="store_true",
    )
    args = parser.parse_args()
    run(args)
