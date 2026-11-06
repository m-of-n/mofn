"""The Learn pages: reading, not doing. Nothing here runs a command or opens
a wallet, and this module imports neither `cli` nor `runner`.

A page is Markdown with three directives, expanded when it is loaded:

    <!-- readme: HEADING -->   that section of prototype/wallet/README.md
    <!-- golden: NAME -->      fixtures/golden/NAME.txt, as printed by check
    <!-- go: TAB -->           the tab its "Go to" button opens

so the explanation and the example output each have one source.
"""

import re
from dataclasses import dataclass
from pathlib import Path

WALLET = Path(__file__).resolve().parents[1]
README = WALLET / "README.md"
GOLDEN = WALLET / "fixtures" / "golden"
PAGES = Path(__file__).resolve().parent / "learn"
DIRECTIVE = re.compile(r"<!-- (readme|golden|go): (.+?) -->\n?")
HEADING = re.compile(r"^(#+) (.+)$")


@dataclass(frozen=True)
class Page:
    title: str
    go: str
    text: str


def section(heading: str, readme: str | None = None) -> str:
    lines = (readme if readme is not None else README.read_text(encoding="utf-8")).splitlines()
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m and m.group(2).strip() == heading:
            level, body = len(m.group(1)), []
            for rest in lines[i + 1 :]:
                n = HEADING.match(rest)
                if n and len(n.group(1)) <= level:
                    break
                body.append(rest)
            return "\n".join(body).strip("\n")
    raise KeyError(f"README.md has no section {heading!r}")


def golden(name: str) -> str:
    return (GOLDEN / f"{name}.txt").read_text(encoding="utf-8")


def expand(text: str) -> tuple[str, str]:
    go = ""

    def one(m: re.Match) -> str:
        nonlocal go
        kind, arg = m.group(1), m.group(2).strip()
        if kind == "readme":
            return section(arg) + "\n"
        if kind == "golden":
            return "```text\n" + golden(arg) + "```\n"
        go = arg
        return ""

    return DIRECTIVE.sub(one, text), go


def pages() -> list[Page]:
    out = []
    for f in sorted(PAGES.glob("*.md")):
        text, go = expand(f.read_text(encoding="utf-8"))
        title = text.splitlines()[0].removeprefix("# ").strip()
        out.append(Page(title, go, text))
    return out
