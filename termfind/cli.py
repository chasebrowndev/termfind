"""
termfind — bulk glossary term lookup
-------------------------------------
Run from any directory that contains a termfind.conf (or pass --config).

Quick start:
  1. Edit termfind.conf  →  point glossary_file at your glossary
  2. Put your terms in   terms.txt  (one per line)
  3. Run:  termfind
  4. Results appear in   found.txt  and are printed to the terminal

Usage:
  termfind                        # use termfind.conf in current directory
  termfind --config path/to.conf  # use a specific config
  termfind --init                 # create starter config + empty terms.txt here
"""

import argparse
import sys
from pathlib import Path

from .config import load_config, DEFAULTS
from .glossary import parse_glossary, lookup_terms

INIT_CONF = """\
# termfind configuration
# Paths are relative to this config file's directory, or absolute.

glossary_file = glossary.txt
terms_file    = terms.txt
output_file   = found.txt

# Separator used between term and definition in the glossary file.
# Options: colon (:)  dash ( - )  equals (=)  tab
separator = colon

# Match terms regardless of capitalisation
case_insensitive = true
"""

INIT_TERMS = """\
# Add the terms you want to look up, one per line.
# Lines starting with # are ignored.

"""


def init_project(directory: Path) -> None:
    conf = directory / "termfind.conf"
    terms = directory / "terms.txt"
    if conf.exists():
        print(f"  termfind.conf already exists, skipping.")
    else:
        conf.write_text(INIT_CONF, encoding="utf-8")
        print(f"  Created {conf}")
    if terms.exists():
        print(f"  terms.txt already exists, skipping.")
    else:
        terms.write_text(INIT_TERMS, encoding="utf-8")
        print(f"  Created {terms}")
    print("\nDone. Edit termfind.conf to point at your glossary, then run: termfind")


def format_results(results: list[tuple[str, str | None]]) -> str:
    found = [(t, d) for t, d in results if d is not None]
    missing = [t for t, d in results if d is None]

    lines = []

    if found:
        max_term = max(len(t) for t, _ in found)
        for term, definition in found:
            lines.append(f"{term:<{max_term}}  {definition}")

    if missing:
        lines.append("")
        lines.append("NOT FOUND:")
        for term in missing:
            lines.append(f"  {term}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="termfind",
        description="Look up key term definitions from a glossary.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--config", "-c",
        default="termfind.conf",
        metavar="FILE",
        help="Config file to use (default: termfind.conf in current directory)",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create a starter termfind.conf and terms.txt in the current directory",
    )
    args = parser.parse_args()

    if args.init:
        init_project(Path.cwd())
        return

    config_path = Path(args.config).resolve()
    cfg = load_config(config_path)
    base = config_path.parent  # all relative paths resolve from config location

    # Resolve paths
    glossary_path = Path(cfg["glossary_file"])
    if not glossary_path.is_absolute():
        glossary_path = base / glossary_path

    terms_path = Path(cfg["terms_file"])
    if not terms_path.is_absolute():
        terms_path = base / terms_path

    output_path = Path(cfg["output_file"])
    if not output_path.is_absolute():
        output_path = base / output_path

    # Validate inputs
    if not glossary_path.exists():
        sys.exit(f"Error: glossary file not found: {glossary_path}")
    if not terms_path.exists():
        sys.exit(f"Error: terms file not found: {terms_path}")

    # Load terms (skip blank lines and comments)
    raw_terms = [
        line.strip()
        for line in terms_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not raw_terms:
        sys.exit("Error: terms.txt is empty — nothing to look up.")

    # Parse glossary and look up
    case_insensitive = bool(cfg["case_insensitive"])
    glossary = parse_glossary(glossary_path, cfg["separator"], case_insensitive)
    results = lookup_terms(raw_terms, glossary, case_insensitive)

    # Format and write output
    output = format_results(results)
    output_path.write_text(output + "\n", encoding="utf-8")

    # Print summary, then cat found.txt
    found_count = sum(1 for _, d in results if d is not None)
    missing_count = len(results) - found_count
    print(f"termfind: {found_count} found, {missing_count} not found → {output_path}\n")
    print(output)


if __name__ == "__main__":
    main()
