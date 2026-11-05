"""Two small dialogs: choose a file, and type a passphrase."""

import os
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Input, Label, Static


def nearby(path: Path) -> str:
    try:
        rel = os.path.relpath(path)
    except ValueError:
        return str(path)
    return str(path) if rel.startswith("..") else rel


class Picker(ModalScreen[str | None]):
    BINDINGS = [("escape", "cancel", "cancel")]
    DEFAULT_CSS = """
    Picker { align: center middle; }
    #picker { width: 80%; height: 80%; border: thick $primary; background: $surface; padding: 0 1; }
    #picker DirectoryTree { height: 1fr; }
    """

    def __init__(self, title: str):
        super().__init__()
        self.title_text = title

    def compose(self) -> ComposeResult:
        with Vertical(id="picker"):
            yield Label(self.title_text)
            yield DirectoryTree(Path.cwd())
            with Horizontal():
                yield Button("Cancel", id="picker-cancel")

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.dismiss(nearby(Path(event.path)))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "picker-cancel":
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class Passphrase(ModalScreen[bytes | None]):
    """A masked field. What is typed goes back to the form that asked, and
    from there to `cli.main` in this process; it is never shown or stored."""

    BINDINGS = [("escape", "cancel", "cancel")]
    DEFAULT_CSS = """
    Passphrase { align: center middle; }
    #ask { width: 60; height: auto; border: thick $primary; background: $surface; padding: 1 2; }
    #ask-error { color: $error; }
    """

    def __init__(self, purpose: str, confirm: bool = False):
        super().__init__()
        self.purpose, self.confirm = purpose, confirm

    def compose(self) -> ComposeResult:
        with Vertical(id="ask"):
            yield Label(self.purpose)
            yield Input(password=True, placeholder="passphrase", id="ask-1")
            if self.confirm:
                yield Input(password=True, placeholder="the same again", id="ask-2")
            yield Static(id="ask-error")
            with Horizontal():
                yield Button("OK", variant="primary", id="ask-ok")
                yield Button("Cancel", id="ask-cancel")

    def on_mount(self) -> None:
        self.query_one("#ask-1", Input).focus()

    def finish(self) -> None:
        first = self.query_one("#ask-1", Input).value
        if not first:
            self.query_one("#ask-error", Static).update("the passphrase is empty")
            return
        if self.confirm and self.query_one("#ask-2", Input).value != first:
            self.query_one("#ask-error", Static).update("the passphrases differ")
            return
        self.dismiss(first.encode("utf-8"))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.confirm and event.input.id == "ask-1":
            self.query_one("#ask-2", Input).focus()
        else:
            self.finish()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ask-ok":
            self.finish()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)
