from pathlib import Path

SEPARATORS = {
    "colon":  ":",
    "dash":   " - ",
    "equals": "=",
    "tab":    "\t",
}


def parse_glossary(file_path: Path, separator: str, case_insensitive: bool) -> dict[str, tuple[str, str]]:
    """
    Parse a glossary file into {lookup_key: (original_term, definition)}.
    Lines starting with # or blank lines are ignored.
    """
    sep = SEPARATORS.get(separator, separator)
    glossary: dict[str, tuple[str, str]] = {}

    for lineno, raw in enumerate(file_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if sep not in line:
            continue  # silently skip malformed lines
        sep_padded = f" {sep} "
        term, _, definition = line.partition(sep_padded) if sep_padded in line else line.partition(sep)
        term = term.strip()
        definition = definition.strip()
        if not term or not definition:
            continue
        key = term.lower() if case_insensitive else term
        glossary[key] = (term, definition)

    return glossary


def lookup_terms(
    terms: list[str],
    glossary: dict[str, tuple[str, str]],
    case_insensitive: bool,
) -> list[tuple[str, str | None]]:
    """Return [(term, definition_or_None), ...] for each requested term."""
    from difflib import get_close_matches
    results = []
    keys = list(glossary.keys())
    for term in terms:
        key = term.strip().lower() if case_insensitive else term.strip()
        if key in glossary:
            _, definition = glossary[key]
            results.append((term.strip(), definition))
        else:
            matches = get_close_matches(key, keys, n=1, cutoff=0.8)
            if matches:
                _, definition = glossary[matches[0]]
                results.append((term.strip(), definition))
            else:
                results.append((term.strip(), None))
    return results
