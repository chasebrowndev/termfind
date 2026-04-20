from pathlib import Path

DEFAULTS = {
    "glossary_file": "glossary.txt",
    "separator": "colon",
    "case_insensitive": True,
    "terms_file": "terms.txt",
    "output_file": "found.txt",
}


def load_config(config_path: Path) -> dict:
    cfg = dict(DEFAULTS)
    if not config_path.exists():
        return cfg

    for raw in config_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
        if key in DEFAULTS:
            cfg[key] = val

    return cfg
