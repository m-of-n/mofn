"""`mofn run`: the App, its tabs, first run, and Learn.

The wallet is the one the CLI would open: `--wallet`, else `$MOFN_WALLET`,
else `./wallet`. With no wallet there yet, first run asks the questions that
make one.
"""

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
    TabbedContent,
    TabPane,
)

import cli
import engine
from engine.render import fingerprint
from screens import data, example, forms, learn, runner

KEYS = " tab next field · enter choose · ctrl+s run · o open a file · ? learn · q or ctrl+q quit"
TABS = ("wallet", "keys", "trust", "sign", "check", "learn")


class WalletPane(VerticalScroll):
    def __init__(self, place):
        super().__init__(id="wallet-pane")
        self.place = place

    def compose(self) -> ComposeResult:
        yield Static(id="wallet-summary")
        with Horizontal(classes="row"):
            yield Button("Open a file… (o)", id="wallet-open")
            yield Button("Get the example vocabulary", id="wallet-example")
        yield Static(id="wallet-result")

    def reload(self, view: data.View) -> None:
        t = Text()
        t.append("Wallet  ", "bold")
        t.append(f"{cli.shown(self.place.wallet)}\n\n")
        t.append("Your keys\n", "bold")
        for p in view.owned:
            t.append(f"  {data.name(p):<24} {fingerprint(p.kid)}  {p.controller}\n")
        if not view.owned:
            t.append("  none yet: make one on Keys\n")
        t.append("\nKeys you know\n", "bold")
        for p in view.known:
            t.append(f"  {data.name(p):<24} {fingerprint(p.kid)}\n")
        if not view.known:
            t.append("  none yet: import one on Keys\n")
        t.append("\nYour anchors\n", "bold")
        lines = [(c, l) for c in view.contexts for l in view.anchor_lines(c)]
        for _, l in lines:
            t.append(f"  {l}\n")
        if not lines:
            t.append("  none yet: you trust no key about anything; see Trust\n")
        if example.installed(self.place.wallet):
            t.append(f"\nThe example vocabulary is in {example.folder(self.place.wallet)}/\n", "dim")
        self.query_one("#wallet-summary", Static).update(t)
        self.query_one("#wallet-example").display = not example.installed(self.place.wallet)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "wallet-open":
            self.app.action_open_file()
        elif event.button.id == "wallet-example":
            self.query_one("#wallet-result", Static).update(self.app.get_example())


class KeyTable(DataTable):
    def on_mount(self) -> None:
        self.add_columns("name", "fingerprint", "", "kind")
        self.cursor_type = "row"

    def reload(self, view: data.View) -> None:
        self.clear()
        for p in view.owned + view.known:
            self.add_row(
                data.name(p),
                fingerprint(p.kid),
                "yours" if p.owned else "known",
                p.controller or "",
            )


class LearnPane(Horizontal):
    def __init__(self):
        super().__init__(id="learn-pane")
        self.pages = learn.pages()

    def compose(self) -> ComposeResult:
        yield ListView(*(ListItem(Label(p.title)) for p in self.pages), id="learn-list")
        with VerticalScroll(id="learn-page"):
            yield Markdown(self.pages[0].text, id="learn-text")
            yield Button(f"Go to {self.pages[0].go.title()}", id="learn-go")

    def show(self, n: int) -> None:
        page = self.pages[n]
        self.query_one("#learn-text", Markdown).update(page.text)
        go = self.query_one("#learn-go", Button)
        go.label = f"Go to {page.go.title()}"
        go.target = page.go

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.list_view.index is not None:
            self.show(event.list_view.index)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "learn-go":
            target = getattr(event.button, "target", self.pages[0].go)
            self.app.query_one(TabbedContent).active = target


class FirstRun(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "app.quit", "quit")]
    DEFAULT_CSS = """
    FirstRun { align: center middle; }
    #first { width: 90%; height: auto; max-height: 95%; border: thick $primary; background: $surface; padding: 1 2; }
    #first .row { height: auto; }
    #first .row { margin: 0 0 1 0; }
    #first .label { width: 26; padding: 0 1 0 0; }
    #first Input { width: 1fr; background: $background; }
    #first-err { color: $error; height: auto; }
    #first-runs { color: $text-muted; height: auto; padding: 1 0; }
    #first-go { dock: bottom; }
    """

    def __init__(self, place: runner.Place):
        super().__init__()
        self.place = place

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="first"):
            yield Label(Text("There is no wallet here yet. A few questions make one.", "bold"))
            for label, fid, widget in (
                ("Where to keep it", "first-where", Input(str(self.place.wallet), id="first-where", compact=True)),
                ("A name for your key", "first-name", Input("me", id="first-name", compact=True)),
                ("Passphrase", "first-pass", Input(password=True, id="first-pass", compact=True)),
                ("The same again", "first-again", Input(password=True, id="first-again", compact=True)),
            ):
                with Horizontal(classes="row"):
                    yield Label(label, classes="label")
                    yield widget
            yield Checkbox(
                "Get the example vocabulary (DV-1, by Alice), and know Alice's key",
                True,
                id="first-example",
            )
            yield Static(id="first-runs")
            yield Static(id="first-err")
            yield Button("Create my wallet", variant="primary", id="first-go")

    def on_mount(self) -> None:
        self.refresh_runs()
        self.query_one("#first-name", Input).focus()

    def plan(self) -> list[list[str]]:
        where = self.query_one("#first-where", Input).value.strip()
        name = self.query_one("#first-name", Input).value.strip()
        place = runner.Place(self.place.wallet, self.place.flag, self.place.codec)
        if where:
            place.move(where)
        out = [place.argv("init"), place.argv("key", "gen", name, "-o", self.pub(place, name))]
        if self.query_one("#first-example", Checkbox).value:
            alice = example.path(place.wallet, f"alice.pub{place.suffix}")
            out.append(place.argv("key", "import", str(alice), "--label", example.ALICE))
        self.planned = place
        return out

    def pub(self, place, name: str) -> str:
        return str(place.wallet.parent / f"{name}.pub{place.suffix}")

    def refresh_runs(self) -> None:
        lines = ["Runs"] + ["  " + runner.shown(a) for a in self.plan()]
        if self.query_one("#first-example", Checkbox).value:
            lines.insert(3, f"  (copy the example vocabulary into {example.folder(self.planned.wallet)}/)")
        self.query_one("#first-runs", Static).update("\n".join(lines))

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id in ("first-where", "first-name"):
            self.refresh_runs()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        self.refresh_runs()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.create()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "first-go":
            self.create()

    def create(self) -> None:
        err = self.query_one("#first-err", Static)
        name = self.query_one("#first-name", Input).value.strip()
        first = self.query_one("#first-pass", Input).value
        if not name:
            err.update("give your key a name")
            return
        if not first:
            err.update("the passphrase is empty")
            return
        if self.query_one("#first-again", Input).value != first:
            err.update("the passphrases differ")
            return
        commands = self.plan()
        place = self.planned
        for i, argv in enumerate(commands):
            if i == 2:
                example.install(place.wallet, place.suffix)
            r = runner.run(argv, first.encode("utf-8") if i == 1 else None)
            self.app.last = r
            if r.code:
                err.update(f"{runner.shown(argv)}\n{r.error}")
                return
        self.place.wallet, self.place.flag = place.wallet, place.flag
        self.dismiss(True)


class ShowScreen(ModalScreen[None]):
    BINDINGS = [("escape", "close", "close")]
    DEFAULT_CSS = """
    ShowScreen { align: center middle; }
    #show-box { width: 90%; height: 90%; border: thick $primary; background: $surface; }
    #show-close { dock: bottom; }
    """

    def __init__(self, place):
        super().__init__()
        self.place = place

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="show-box"):
            yield forms.Show(self.place)
            yield Button("Close (esc)", id="show-close")

    def on_mount(self) -> None:
        self.query_one(forms.Show).reload(data.View.of(self.place))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "show-close":
            self.dismiss(None)

    def action_close(self) -> None:
        self.dismiss(None)


class WalletApp(App):
    TITLE = "mofn"
    CSS = """
    Screen { overflow: hidden; }
    #top, #help { height: 1; }
    #top { dock: top; background: $primary; color: $text; }
    #help { dock: bottom; }
    TabbedContent { height: 1fr; }
    TabbedContent ContentSwitcher { height: 1fr; }
    TabPane { height: 1fr; padding: 0; }
    TabPane > VerticalScroll, #wallet-pane, #learn-pane { height: 1fr; }
    #learn-list { width: 26; height: 1fr; }
    #learn-page { height: 1fr; padding: 0 1; }
    .row { height: auto; }
    """
    BINDINGS = [
        Binding("question_mark", "learn", "learn"),
        Binding("o", "open_file", "open a file"),
        Binding("ctrl+s", "submit", "run"),
        Binding("q", "quit", "quit"),
        Binding("ctrl+q", "quit", "quit", priority=True),
    ]

    def __init__(self, flag: str | None = None, codec: str | None = None):
        super().__init__()
        self.place = runner.Place.resolve(flag, codec)
        self.last: runner.Result | None = None

    def compose(self) -> ComposeResult:
        yield Static(id="top")
        with TabbedContent(initial="wallet"):
            with TabPane("Wallet", id="wallet"):
                yield WalletPane(self.place)
            with TabPane("Keys", id="keys"):
                with VerticalScroll():
                    yield KeyTable(id="key-table")
                    yield forms.KeyGen(self.place)
                    yield forms.KeyImport(self.place)
            with TabPane("Trust", id="trust"):
                with VerticalScroll():
                    yield forms.Trust(self.place)
            with TabPane("Sign", id="sign"):
                with VerticalScroll():
                    yield forms.Sign(self.place)
            with TabPane("Check", id="check"):
                with VerticalScroll():
                    yield forms.Check(self.place)
            with TabPane("Learn", id="learn"):
                yield LearnPane()
        yield Static(KEYS, id="help")

    def on_mount(self) -> None:
        self.reload()
        if not self.place.exists:
            self.push_screen(FirstRun(self.place), self.after_first_run)

    def after_first_run(self, made: bool | None) -> None:
        self.reload()
        if made:
            view = data.View.of(self.place)
            mine = view.owned[0] if view.owned else None
            if mine:
                self.query_one("#wallet-result", Static).update(
                    Text(
                        f"Made your wallet at {cli.shown(self.place.wallet)}, and your key "
                        f"{data.name(mine)}, {fingerprint(mine.kid)}. Send "
                        f"{mine.label}.pub{self.place.suffix} to anyone who should "
                        "check what you sign.",
                        "green",
                    )
                )

    def reload(self) -> None:
        view = data.View.of(self.place)
        self.query_one("#top", Static).update(
            f" mofn {engine.__version__} ── wallet {cli.shown(self.place.wallet)}"
        )
        self.query_one(WalletPane).reload(view)
        self.query_one(KeyTable).reload(view)
        for f in self.query(forms.Form):
            f.reload(view)

    def get_example(self) -> Text:
        example.install(self.place.wallet, self.place.suffix)
        view = data.View.of(self.place)
        if any(p.label == example.ALICE for p in view.personas):
            self.reload()
            return Text(f"copied the example vocabulary into {example.folder(self.place.wallet)}")
        argv = self.place.argv(
            "key",
            "import",
            str(example.path(self.place.wallet, f"alice.pub{self.place.suffix}")),
            "--label",
            example.ALICE,
        )
        r = runner.run(argv)
        self.last = r
        self.reload()
        return Text(f"$ {runner.shown(argv)}\n{r.out.rstrip() or r.error}")

    def action_learn(self) -> None:
        self.query_one(TabbedContent).active = "learn"

    def action_open_file(self) -> None:
        self.push_screen(ShowScreen(self.place))

    def action_submit(self) -> None:
        pane = self.query_one(TabbedContent).active_pane
        if pane is None:
            return
        found = list(pane.query(forms.Form))
        focused = self.focused
        for f in found:
            if focused is not None and f in focused.ancestors_with_self:
                f.submit()
                return
        if found:
            found[0].submit()


def main(flag: str | None, codec: str | None) -> int:
    WalletApp(flag, codec).run()
    return 0
