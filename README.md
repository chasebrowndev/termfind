# termfind

A lightweight CLI tool for bulk glossary lookups. Drop in a glossary, list your terms, get back definitions — fast.

Built for students doing key terms assignments but useful anywhere you need to pull definitions from a structured text glossary.

---

## Usage (Windows — no install required)

1. Download `termfind.exe` from the [Releases](../../releases) page
2. Place it in your class folder (or anywhere on your PATH)
3. Open a terminal in that folder and run:
   ```
   termfind --init
   ```
4. Edit `termfind.conf` — point `glossary_file` at your glossary
5. Fill `terms.txt` with your terms, one per line
6. Run `termfind` — results print to the terminal and save to `found.txt`

> **Tip:** Add `termfind.exe` to a folder on your PATH (e.g. `C:\Tools`) so you can run it from any directory.

---

## Usage (Linux / macOS — requires Python 3.10+)

```bash
pipx install -e .
```

Then use exactly as above.

---

## Glossary Format

One entry per line using a consistent separator:

```
Term | Definition
Term: Definition
Term - Definition
```

Supports `|`, `:`, `-`, `=`, and tab separators. Set your separator in `termfind.conf`.

---

## Config Reference

`termfind.conf` lives in your working directory. All paths are relative to the config file.

| Key | Default | Description |
|-----|---------|-------------|
| `glossary_file` | `glossary.txt` | Path to your glossary |
| `terms_file` | `terms.txt` | Path to your terms list |
| `output_file` | `found.txt` | Path to write results |
| `separator` | `colon` | Separator: `colon`, `dash`, `equals`, `tab`, or any literal character like `\|` |
| `case_insensitive` | `true` | Match terms regardless of capitalisation |
| `warn_missing` | `true` | Print a warning for terms not found |

---

## Fuzzy Matching

termfind uses fuzzy matching (via Python's `difflib`) to handle minor mismatches between your terms list and the glossary — pluralisation, missing acronyms in parentheses, etc.

---

## Building the EXE yourself

Requires Python and PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --name termfind --console __main__.py
# output: dist/termfind.exe
```

---

## Releasing a new version

Push a version tag and GitHub Actions will build and attach `termfind.exe` automatically:

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## Tips

- Paste your glossary straight from a browser console (`document.body.innerText`) into `glossary.txt`
- `found.txt` persists after each run, useful for submitting or referencing later
- Multiple class folders can each have their own `termfind.conf` pointing to different glossaries

---

## License

MIT
