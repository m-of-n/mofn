"""The forms. Each one builds the argv of one mofn command from its fields,
shows it on its Runs line as the fields change, and runs exactly that argv
through `runner.run`. Choices come from `data.View`, so a form never offers
a key or a value the wallet or the vocabulary does not have.
"""

import json
from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label, Select, SelectionList, Static

from engine import render
from engine.errors import WalletError
from engine.store import CONTROLLERS
from screens import data, example, runner
from screens.picker import Passphrase, Picker

LINES = ("integrity", "authenticity", "names", "authorization", "acceptance", "semantics")


def value(w) -> str | list[str]:
    if isinstance(w, Input):
        return w.value.strip()
    if isinstance(w, Select):
        return w.value if isinstance(w.value, str) else ""
    if isinstance(w, SelectionList):
        return [str(v) for v in w.selected]
    return ""


def offer(
    select: Select, options: list[tuple[str, str]], prefer: str = "", only: bool = False
) -> None:
    keep = value(select)
    if [o[1] for o in options] != [o[1] for o in getattr(select, "_offered", [])]:
        select._offered = options
        select.set_options(options)
    ids = [o[1] for o in options]
    sole = ids[0] if only and len(ids) == 1 else ""
    pick = keep if keep in ids else (prefer if prefer in ids else sole)
    if pick and value(select) != pick:
        select.value = pick


class FileField(Horizontal):
    DEFAULT_CSS = """
    FileField { height: auto; width: 1fr; }
    FileField Input { width: 1fr; }
    FileField Button { width: 10; margin: 0 0 0 1; }
    """

    def __init__(self, fid: str, placeholder: str = "", start: str = ""):
        super().__init__(id=f"{fid}-box")
        self.fid, self.placeholder, self.start = fid, placeholder, start

    def compose(self) -> ComposeResult:
        yield Input(self.start, placeholder=self.placeholder, id=self.fid, compact=True)
        yield Button("Browse", id=f"{self.fid}-browse", compact=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == f"{self.fid}-browse":
            event.stop()
            field = self.query_one(Input)
            self.app.push_screen(
                Picker(f"Choose a file for {self.fid.split('-', 1)[-1]}"),
                lambda chosen: chosen and setattr(field, "value", chosen),
            )


class Form(Vertical):
    DEFAULT_CSS = """
    Form { height: auto; border: round $primary; padding: 0 1; margin: 0 0 1 0; }
    Form .row { height: auto; margin: 0 0 0 0; }
    Form .label { width: 18; padding: 0 1 0 0; }
    Form .field { width: 1fr; }
    Form .err, Form .form-err { color: $error; height: auto; padding: 0 0 0 18; }
    Form .form-err { padding: 0; }
    Form .runs { color: $text-muted; height: auto; padding: 1 0; }
    Form .result { height: auto; }
    Form #check-list { height: auto; padding: 0 0 0 18; }
    """
    NAME = "form"
    TITLE = ""
    GO = "Run"
    SECRET = ""
    CONFIRM = False
    OK = (0,)
    MAIN = ""

    def __init__(self, place: runner.Place):
        super().__init__(id=self.NAME)
        self.place = place
        self.view = data.View(None)
        self.inputs: dict[str, object] = {}
        self.busy = False

    def compose(self) -> ComposeResult:
        yield Label(Text(self.TITLE, "bold"))
        yield from self.fields()
        yield Static(classes="runs", id=f"{self.NAME}-runs")
        yield Static(classes="form-err", id=f"{self.NAME}-err")
        yield Button(self.GO, variant="primary", id=f"{self.NAME}-go")
        yield Static(classes="result", id=f"{self.NAME}-result")

    def row(self, label: str, key: str, widget) -> ComposeResult:
        fid = f"{self.NAME}-{key}"
        self.inputs[key] = fid
        if not isinstance(widget, FileField):
            widget.id = fid
        with Horizontal(classes="row"):
            yield Label(label, classes="label")
            yield widget
        yield Static(classes="err", id=f"{fid}-err")

    def w(self, key: str):
        return self.query_one(f"#{self.inputs[key]}")

    def v(self, key: str):
        return value(self.w(key))

    def fields(self) -> ComposeResult:
        return iter(())

    def argv(self) -> list[str] | None:
        return None

    def full(self) -> list[str] | None:
        a = self.argv()
        return self.place.argv(*a) if a else None

    def refresh_runs(self) -> None:
        a = self.full()
        text = "Runs   " + runner.shown(a) if a else "Runs   (fill in the fields above)"
        self.query_one(f"#{self.NAME}-runs", Static).update(text)

    def reload(self, view: data.View) -> None:
        self.view = view
        self.refresh_runs()

    def depend(self, key: str) -> None:
        pass

    def key_of(self, widget_id: str | None) -> str:
        return next((k for k, f in self.inputs.items() if f == widget_id), "")

    def on_mount(self) -> None:
        self.refresh_runs()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.depend(self.key_of(event.input.id))
        self.refresh_runs()

    def on_select_changed(self, event: Select.Changed) -> None:
        self.depend(self.key_of(event.select.id))
        self.refresh_runs()

    def on_selection_list_selected_changed(self, event) -> None:
        self.refresh_runs()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == f"{self.NAME}-go":
            event.stop()
            self.submit()

    def clear_errors(self) -> None:
        for s in self.query(".err"):
            s.update("")
        self.query_one(f"#{self.NAME}-err", Static).update("")

    def show_error(self, message: str) -> None:
        for key, fid in self.inputs.items():
            v = self.v(key)
            for item in v if isinstance(v, list) else [v]:
                if len(item) >= 2 and item in message:
                    self.query_one(f"#{fid}-err", Static).update(message)
                    return
        where = f"#{self.inputs[self.MAIN]}-err" if self.MAIN else f"#{self.NAME}-err"
        self.query_one(where, Static).update(message)

    def submit(self) -> None:
        self.clear_errors()
        argv = self.full()
        if not argv:
            self.query_one(f"#{self.NAME}-err", Static).update(
                "fill in every field the command needs"
            )
            return
        if self.SECRET:
            self.app.push_screen(
                Passphrase(self.SECRET, self.CONFIRM),
                lambda p: p is not None and self.execute(argv, p),
            )
        else:
            self.execute(argv, None)

    def execute(self, argv: list[str], passphrase: bytes | None) -> None:
        r = runner.run(argv, passphrase)
        self.app.last = r
        if r.code not in self.OK:
            self.show_error(r.error)
            return
        self.query_one(f"#{self.NAME}-result", Static).update(self.result(r))
        self.app.reload()

    def result(self, r: runner.Result):
        return Text(r.out.rstrip())


class KeyGen(Form):
    NAME = "keygen"
    TITLE = "Make a key of your own"
    GO = "Make key…"
    SECRET = "A passphrase for the new key. You will need it to sign."
    CONFIRM = True

    def fields(self) -> ComposeResult:
        yield from self.row("Name", "name", Input(placeholder="me", classes="field", compact=True))
        yield from self.row(
            "Kind",
            "kind",
            Select([(c, c) for c in CONTROLLERS], value="person", allow_blank=False, classes="field", compact=True),
        )
        yield from self.row(
            "Save public key", "save", Input(placeholder="NAME.pub.stmt", classes="field", compact=True)
        )

    def argv(self):
        name, kind, save = self.v("name"), self.v("kind"), self.v("save")
        if not name:
            return None
        out = ["key", "gen", name]
        if kind and kind != "person":
            out += ["--controller", kind]
        return out + (["-o", save] if save else [])


class KeyImport(Form):
    NAME = "keyimport"
    TITLE = "Know a key you were sent"
    GO = "Import"
    MAIN = "file"

    def fields(self) -> ComposeResult:
        yield from self.row("File", "file", FileField("keyimport-file", "someone.pub.stmt"))
        yield from self.row(
            "Your name for it", "label", Input(placeholder="Chip", classes="field", compact=True)
        )

    def argv(self):
        f, label = self.v("file"), self.v("label")
        if not f:
            return None
        return ["key", "import", f] + (["--label", label] if label else [])


class KeyExport(Form):
    NAME = "keyexport"
    TITLE = "Send your key again"
    GO = "Export"
    MAIN = "as"

    def fields(self) -> ComposeResult:
        yield from self.row("Your key", "as", Select([], prompt="one of your keys", classes="field", compact=True))
        yield from self.row("Save as", "save", Input(placeholder="LABEL.pub.stmt", classes="field", compact=True))

    def reload(self, view):
        offer(self.w("as"), data.choices(view.owned), only=True)
        self.depend("as")
        super().reload(view)

    def depend(self, key):
        if key == "as" and self.v("as"):
            save = self.w("save")
            if not save.value or getattr(self, "auto_save", "") == save.value:
                self.auto_save = f"{self.v('as')}.pub{self.place.suffix}"
                save.value = self.auto_save

    def argv(self):
        if not self.v("as"):
            return None
        return ["key", "export", self.v("as")] + (["-o", self.v("save")] if self.v("save") else [])


SHOWN = (".stmt", ".stmt.yaml", ".def")


class Vocabulary(Form):
    def vocab_field(self) -> ComposeResult:
        start = ""
        if example.installed(self.place.wallet):
            start = str(example.path(self.place.wallet, "dv-1.def"))
        yield from self.row(
            "Vocabulary", "vocab", FileField(f"{self.NAME}-vocab", "dv-1.def", start)
        )

    def default_vocab(self) -> None:
        field = self.w("vocab")
        if not field.value and example.installed(self.place.wallet):
            field.value = str(example.path(self.place.wallet, "dv-1.def"))

    def definition(self):
        return data.vocabulary(self.v("vocab")) if self.v("vocab") else None

    def offer_claims(self, prefer: str = "") -> None:
        d = self.definition()
        offer(self.w("claim"), [(c, c) for c in data.claims(d)], prefer)


class Trust(Vocabulary):
    NAME = "trust"
    TITLE = "Trust a key about one kind of claim"
    GO = "Trust"

    def fields(self) -> ComposeResult:
        yield from self.row("Whose key", "whose", Select([], prompt="a key you know", classes="field", compact=True))
        yield from self.row("As which of yours", "as", Select([], prompt="you", classes="field", compact=True))
        yield from self.vocab_field()
        yield from self.row("Claim", "claim", Select([], prompt="a type in the vocabulary", classes="field", compact=True))
        yield from self.row("Values you accept", "values", SelectionList(classes="field", compact=True))
        yield from self.row("Context", "context", Input("default", classes="field", compact=True))
        yield from self.row("Note", "note", Input(placeholder="optional", classes="field", compact=True))
        yield Static(id="trust-anchors")

    def reload(self, view):
        self.default_vocab()
        offer(self.w("whose"), data.choices(view.known))
        offer(self.w("as"), data.choices(view.acceptors), only=True)
        self.offer_claims("build-provenance")
        self.show_anchors()
        super().reload(view)

    def show_anchors(self) -> None:
        ctx = self.v("context") or "default"
        try:
            lines = self.view.anchor_lines(ctx)
        except WalletError:
            lines = []
        body = "\n".join(lines) or f"no anchors in context {ctx}: you trust no key about anything here"
        self.query_one("#trust-anchors", Static).update(Text("Your anchors\n", "bold") + Text(body))

    def depend(self, key):
        if key == "vocab":
            self.offer_claims()
        if key in ("vocab", "claim"):
            vals = data.values(self.definition(), self.v("claim"))
            sl = self.w("values")
            have = [str(sl.get_option_at_index(i).value) for i in range(sl.option_count)]
            if have != vals:
                sl.clear_options()
                sl.add_options([(v, v, False) for v in vals])
        if key == "context":
            self.show_anchors()

    def argv(self):
        whose, as_, vocab, claim = self.v("whose"), self.v("as"), self.v("vocab"), self.v("claim")
        if not (whose and as_ and vocab and claim):
            return None
        out = ["root", "add", whose, "--as", as_, "--def", vocab, "--type", claim]
        if self.v("values"):
            out += ["--values", ",".join(self.v("values"))]
        ctx = self.v("context") or "default"
        if ctx != "default":
            out += ["--context", ctx]
        return out + (["--note", self.v("note")] if self.v("note") else [])

    def result(self, r):
        self.show_anchors()
        return Text(r.out.rstrip())


class Sign(Vocabulary):
    NAME = "sign"
    TITLE = "Sign one statement about a file"
    GO = "Sign…"
    SECRET = "Your passphrase, to sign with your key."

    def fields(self) -> ComposeResult:
        yield from self.row("Sign as", "as", Select([], prompt="one of your keys", classes="field", compact=True))
        yield from self.row("File", "file", FileField("sign-file", "the file you vouch for"))
        yield from self.vocab_field()
        yield from self.row("Claim", "claim", Select([], prompt="a type in the vocabulary", classes="field", compact=True))
        yield from self.row("Value", "value", Select([], prompt="a value of that type", classes="field", compact=True))
        yield from self.row("Valid for (days)", "days", Input("30", type="integer", classes="field", compact=True))
        yield from self.row("Save as", "save", Input(placeholder="FILE.stmt", classes="field", compact=True))

    def reload(self, view):
        self.default_vocab()
        offer(self.w("as"), data.choices(view.owned), only=True)
        self.offer_claims()
        super().reload(view)

    def depend(self, key):
        if key == "vocab":
            self.offer_claims()
        if key in ("vocab", "claim"):
            vals = data.values(self.definition(), self.v("claim"))
            offer(self.w("value"), [(v, v) for v in vals])
        if key == "file":
            save = self.w("save")
            f = self.v("file")
            if f and (not save.value or getattr(self, "auto_save", "") == save.value):
                self.auto_save = f"{Path(f).name}{self.place.suffix}"
                save.value = self.auto_save

    def argv(self):
        as_, f, vocab, claim, val = (self.v(k) for k in ("as", "file", "vocab", "claim", "value"))
        if not (as_ and f and vocab and claim and val):
            return None
        out = ["make", "--as", as_, "--subject", f, "--def", vocab, "--type", claim, "--value", val]
        days = self.v("days")
        if days and days != "30":
            out += ["--valid-days", days]
        return out + (["-o", self.v("save")] if self.v("save") else [])


class Check(Vocabulary):
    NAME = "check"
    TITLE = "Check the statements you were handed"
    GO = "Check"
    OK = (0, 1, 3)

    def __init__(self, place):
        super().__init__(place)
        self.statements: list[str] = []

    def fields(self) -> ComposeResult:
        yield from self.row("Add a statement", "add", FileField("check-add", "a .stmt you were handed"))
        with Horizontal(classes="row"):
            yield Label("", classes="label")
            yield Button("Add", id="check-add-go", compact=True)
            yield Button(" Clear", id="check-clear", compact=True)
        yield Static(id="check-list")
        yield from self.row("File", "file", FileField("check-file", "the file they are about"))
        yield from self.vocab_field()
        yield from self.row("Context", "context", Select([("default", "default")], value="default", allow_blank=False, classes="field", compact=True))
        yield from self.row("At", "at", Input(placeholder="now, or YYYY-MM-DDTHH:MM:SSZ", classes="field", compact=True))

    def reload(self, view):
        self.default_vocab()
        offer(self.w("context"), [(c, c) for c in view.contexts], "default")
        self.show_list()
        super().reload(view)

    def handed(self) -> list[str]:
        out = list(self.statements)
        vocab = self.v("vocab")
        if vocab and example.is_example(self.place.wallet, vocab):
            define = str(example.path(self.place.wallet, f"alice-define{self.place.suffix}"))
            if define not in out:
                out.append(define)
        return out

    def show_list(self) -> None:
        lines = [f"  {s}" for s in self.statements]
        extra = self.handed()[len(self.statements) :]
        lines += [f"  {s}   (added: who published the vocabulary)" for s in extra]
        body = "\n".join(lines) if lines else "  (none yet)"
        self.query_one("#check-list", Static).update("Handed over\n" + body)

    def depend(self, key):
        if key == "vocab":
            self.show_list()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "check-add-go":
            event.stop()
            s = self.v("add")
            if s and s not in self.statements:
                self.statements.append(s)
            self.w("add").value = ""
            self.show_list()
            self.refresh_runs()
        elif event.button.id == "check-clear":
            event.stop()
            self.statements.clear()
            self.show_list()
            self.refresh_runs()
        else:
            super().on_button_pressed(event)

    def argv(self):
        stmts, f, vocab = self.handed(), self.v("file"), self.v("vocab")
        if not (self.statements and f and vocab):
            return None
        out = ["check", *stmts, "--artifact", f, "--def", vocab]
        ctx = self.v("context")
        if ctx and ctx != "default":
            out += ["--context", ctx]
        if self.v("at"):
            out += ["--at", self.v("at")]
        return out + ["--format", "json"]

    def show_error(self, message):
        if any(s in message for s in self.statements):
            self.query_one(f"#{self.NAME}-add-err", Static).update(message)
        else:
            super().show_error(message)

    def result(self, r):
        try:
            j = json.loads(r.out)
        except ValueError:
            return Text(r.out or r.err)
        v = j["verdict"]
        deciding = next((n for n in LINES if v[n]["result"] == "fail"), None)
        out = Text()
        for i, n in enumerate(LINES, 1):
            mark = "▶" if n == deciding else " "
            res = v[n]["result"].replace("-", " ")
            style = "bold" if n == deciding else ("green" if res == "pass" else "")
            out.append(f"{mark} {i} {n:<14} {res:<14} {v[n]['sentence']}\n", style)
        out.append(f"\nanswer: {j['answer']}\n", "bold green" if j["answer"] == "yes" else "bold red")
        if j.get("sentences") and not j.get("sentences_about_your_file", True):
            out.append(f"\n{render.OTHER_FILE}")
        for s in j.get("sentences", []):
            out.append(f"\n{s}\n")
        out.append(f"\n{j['limit']}\n", "dim")
        return out


class Show(Form):
    NAME = "show"
    TITLE = "Open a statement, a .def file, or any file to hash"
    GO = "Open"
    MAIN = "file"

    def fields(self) -> ComposeResult:
        yield from self.row("File", "file", FileField("show-file", "a .stmt, a .def, or any file"))

    def argv(self):
        f = self.v("file")
        if not f:
            return None
        return ["show", f] if f.endswith(SHOWN) else ["hash", f, "--format", "json"]

    def execute(self, argv, passphrase):
        r = runner.run(argv, passphrase)
        self.app.last = r
        if r.code:
            self.show_error(r.error)
            return
        self.query_one(f"#{self.NAME}-result", Static).update(self.result(r))

    def result(self, r):
        if r.argv[-2:] != ["--format", "json"]:
            return Text(r.out.rstrip())
        d = json.loads(r.out)["this"]["digest"]
        out = Text()
        out.append(f"{d['alg']}:{d['value'][2:]}\n", "bold")
        out.append(
            "\nThis is the file's SHA-256. A statement about this file carries it as "
            "its this; verdict sentences print its first 16 digits.\n",
            "dim",
        )
        return out
