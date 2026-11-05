"""`mofn run`: the guided screen, in Textual.

It shows each step's text and every command before it runs, runs them
through `session.Session`, and prints what came back. The six lines come from
the engine's `check --format json`; this file only lays them out.
"""

from pathlib import Path

from rich.console import Group
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Input, Label, ListItem, ListView, Static

import engine
from guide.session import LINES, Outcome, Session, deciding
from guide.steps import STEPS, expected, shown

KEYS = " enter run · h hint · r reset · l list · q quit"


def bar(done: int, total: int, width: int = 14) -> str:
    filled = round(width * done / total)
    return "▓" * filled + "░" * (width - filled)


def verdict_rows(o: Outcome) -> list[Text]:
    rows = []
    v = o.verdict["verdict"]
    first = deciding(o.verdict)
    for i, name in enumerate(LINES, 1):
        result = v[name]["result"].replace("-", " ")
        mark = "▶" if name == first else " "
        style = "bold" if name == first else ""
        rows.append(
            Text(f" {mark} {i} {name:<14} {result:<14} {v[name]['sentence']}", style)
        )
    rows.append(Text(f"   answer: {o.verdict['answer']}", "bold"))
    return rows


class Run(App):
    CSS = """
    Screen { layout: vertical; }
    #top, #keys { height: 1; }
    #body { height: 1fr; }
    #steps { width: 26; border-right: solid $primary; }
    #right { padding: 0 1; }
    #field { display: none; }
    #field.shown { display: block; }
    """
    BINDINGS = [
        Binding("enter", "go", "run"),
        Binding("h", "hint", "hint"),
        Binding("r", "reset", "reset"),
        Binding("l", "list", "list"),
        Binding("q", "quit", "quit"),
    ]

    def __init__(self, folder: Path):
        super().__init__()
        self.session = Session(folder)
        self.view = 0
        self.outputs: dict[int, list] = {}
        self.answers: dict[int, int] = {}
        self.asking = ""

    def compose(self) -> ComposeResult:
        yield Static(id="top")
        with Horizontal(id="body"):
            yield ListView(
                *(ListItem(Label(id=f"step-{n}")) for n in range(len(STEPS))),
                id="steps",
            )
            with VerticalScroll(id="right"):
                yield Static(id="text")
                yield Input(id="field")
        yield Static(KEYS, id="keys")

    def on_mount(self) -> None:
        self.session.prepare()
        if self.session.done and not self.session.started:
            self.session.reset()
        self.view = min(self.session.step, len(STEPS) - 1)
        self.refresh_all()
        self.query_one("#right").focus()

    def refresh_all(self) -> None:
        current = self.session.step
        finished = min(current, len(STEPS))
        top = f" mofn {engine.__version__} ─ run ─ {finished}/{len(STEPS)} {bar(finished, len(STEPS))}"
        self.query_one("#top", Static).update(top)
        for n, step in enumerate(STEPS):
            mark = "✓" if n < current else ("▶" if n == current else " ")
            self.query_one(f"#step-{n}", Label).update(f"{mark} {n} {step.title}")
        self.query_one("#text", Static).update(self.page(self.view))

    def page(self, n: int) -> Group:
        step = STEPS[n]
        parts = [
            Text(f"{n}  {step.heading}", "bold"),
            Text(""),
            Text(step.text),
            Text(""),
        ]
        done_here = n < self.session.step
        if self.outputs.get(n):
            parts.extend(self.outputs[n])
        else:
            parts.append(Text("This will run:", "dim"))
            parts.append(Text(f"  cd {self.session.folder}"))
            for a in self.session.pending(n) or step.actions:
                parts.append(Text("  " + (f"({a.note})" if a.edit else shown(a.argv))))
            parts.append(Text(""))
        if n == self.session.step and step.question and n not in self.answers:
            parts.append(Text(step.question, "bold"))
        elif self.session.step >= len(STEPS) and n == len(STEPS) - 1:
            parts.append(Text("All eight steps done. r starts again.", "bold"))
        elif done_here:
            parts.append(Text("enter: next step", "dim"))
        else:
            parts.append(Text("enter: run these", "dim"))
        return Group(*parts)

    def ask(self, kind: str) -> None:
        field = self.query_one("#field", Input)
        field.value = ""
        self.asking = kind
        if kind == "passphrase":
            field.password = True
            field.restrict = None
            field.max_length = 0
            field.placeholder = "passphrase for your key, me"
        else:
            field.password = False
            field.restrict = r"[1-6]"
            field.max_length = 1
            field.placeholder = "1–6"
        field.add_class("shown")
        field.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value
        if not value:
            return
        field = self.query_one("#field", Input)
        field.value = ""
        field.remove_class("shown")
        self.query_one("#right").focus()
        if self.asking == "passphrase":
            self.session.passphrase = value.encode("utf-8")
        else:
            self.answers[self.view] = int(value)
        self.asking = ""
        self.action_go()

    def action_go(self) -> None:
        if self.asking:
            return
        current = self.session.step
        if current >= len(STEPS):
            self.refresh_all()
            return
        if self.view != current:
            self.view = current
            self.refresh_all()
            return
        if self.session.needs_passphrase(current):
            self.ask("passphrase")
            return
        if STEPS[current].question and current not in self.answers:
            self.ask("answer")
            return
        self.run_step(current)

    def run_step(self, n: int) -> None:
        out = self.outputs.setdefault(n, [])
        while self.session.step == n:
            o = self.session.advance()
            a = o.action
            out.append(Text("· " + a.note if a.edit else "$ " + shown(a.argv), "bold"))
            if o.verdict is not None:
                out.extend(verdict_rows(o))
            elif o.out.strip():
                out.append(Text(o.out.rstrip()))
            if o.err.strip():
                out.append(Text(o.err.rstrip(), "red"))
            if not o.ok:
                out.extend(Text(f"  not as expected: {p}", "red") for p in o.problems)
                out.append(Text("  r resets the guide and starts again", "red"))
                break
            if a.check:
                out.append(Text(f"  as expected: {expected(a)}, exit {o.code}", "green"))
            out.append(Text(""))
        if n == 0 and self.session.step > 0:
            out.append(Text("Your wallet:", "bold"))
            out.extend(Text("  " + r) for r in self.session.folders())
            out.append(Text("Your private key:", "bold"))
            out.extend(Text("  " + r) for r in self.session.key_files())
        if n in self.answers:
            self.answers_line(n, out)
        self.refresh_all()

    def answers_line(self, n: int, out: list) -> None:
        name = next(a.decides for a in STEPS[n].actions if a.check)
        first, guess = LINES.index(name) + 1, self.answers[n]
        right = guess == first
        out.append(
            Text(
                f"You said {guess}. The first line that fails is {first}, "
                f"{name}." + (" Right." if right else ""),
                "green" if right else "yellow",
            )
        )

    def action_hint(self) -> None:
        out = self.outputs.setdefault(self.view, [])
        out.append(Text("hint: " + STEPS[self.view].hint, "italic"))
        self.refresh_all()

    def action_reset(self) -> None:
        self.session.reset()
        self.session.passphrase = None
        self.outputs.clear()
        self.answers.clear()
        self.view = 0
        self.refresh_all()

    def action_list(self) -> None:
        self.query_one("#steps", ListView).focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.view = event.list_view.index or 0
        self.refresh_all()
        self.query_one("#right").focus()


def main(folder: Path) -> int:
    Run(folder).run()
    return 0
