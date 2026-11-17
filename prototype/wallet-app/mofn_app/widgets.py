"""The few pieces every page is made of: cards, labels, a file field, a
two-way toggle, the page frame, and the Standing timeline."""

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from . import theme


def label(text: str = "", name: str | None = None, wrap: bool = True) -> QLabel:
    w = QLabel(text)
    if name:
        w.setObjectName(name)
    w.setWordWrap(wrap)
    w.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return w


def caps(text: str) -> QLabel:
    return label(text.upper(), "lab", wrap=False)


def restyle(w: QWidget, **props) -> None:
    for k, v in props.items():
        w.setProperty(k, v)
    w.style().unpolish(w)
    w.style().polish(w)


class Card(QFrame):
    def __init__(self, title: str | None = None, tone: str | None = None):
        super().__init__()
        self.setObjectName("card")
        if tone:
            self.setProperty("tone", tone)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(14, 12, 14, 12)
        self.box.setSpacing(6)
        if title:
            self.box.addWidget(caps(title))

    def add(self, w: QWidget) -> QWidget:
        self.box.addWidget(w)
        return w

    def tone(self, tone: str | None) -> None:
        restyle(self, tone=tone or "")


class Rows(QGridLayout):
    """Label | value rows: the app's one layout for facts and forms."""

    def __init__(self, width: int = 120):
        super().__init__()
        self.setHorizontalSpacing(12)
        self.setVerticalSpacing(7)
        self.setColumnMinimumWidth(0, width)
        self.setColumnStretch(1, 1)

    def row(self, name: str, w: QWidget | str) -> QWidget:
        if isinstance(w, str):
            w = label(w)
        r = self.rowCount()
        left = label(name, "sub", wrap=False)
        left.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.addWidget(left, r, 0)
        self.addWidget(w, r, 1)
        return w


def holder(layout) -> QWidget:
    w = QWidget()
    w.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)
    return w


class FileField(QWidget):
    """A path with a Choose… button. `mode`: open, many, save."""

    changed = Signal(str)

    def __init__(self, placeholder: str = "", mode: str = "open", filter: str = ""):
        super().__init__()
        self.mode, self.filter = mode, filter
        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(placeholder)
        self.edit.textChanged.connect(self.changed.emit)
        b = QPushButton("Choose…")
        b.clicked.connect(self.choose)
        h.addWidget(self.edit, 1)
        h.addWidget(b)

    def choose(self) -> None:
        if self.mode == "many":
            files, _ = QFileDialog.getOpenFileNames(self, "Choose files", "", self.filter)
            if files:
                self.edit.setText("; ".join(files))
            return
        pick = QFileDialog.getSaveFileName if self.mode == "save" else QFileDialog.getOpenFileName
        f, _ = pick(self, "Choose a file", self.text(), self.filter)
        if f:
            self.edit.setText(f)

    def text(self) -> str:
        return self.edit.text().strip()

    def files(self) -> list[str]:
        return [f.strip() for f in self.text().split(";") if f.strip()]

    def set(self, text: str) -> None:
        self.edit.setText(text)


class Toggle(QWidget):
    """Two or three segments, one checked."""

    picked = Signal(str)

    def __init__(self, options: list[str], start: str | None = None):
        super().__init__()
        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        self.group = QButtonGroup(self)
        for o in options:
            b = QPushButton(o)
            b.setObjectName("seg")
            b.setCheckable(True)
            b.setChecked(o == (start or options[0]))
            b.clicked.connect(lambda _=False, o=o: self.picked.emit(o))
            self.group.addButton(b)
            h.addWidget(b)

    def value(self) -> str:
        return self.group.checkedButton().text()


class Page(QScrollArea):
    """Pill, title, subtitle, then cards, top to bottom."""

    title = ""
    pill = ""
    sub = ""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget()
        inner.setObjectName("page")
        self.body = QVBoxLayout(inner)
        self.body.setContentsMargins(22, 16, 22, 22)
        self.body.setSpacing(10)
        self.setWidget(inner)
        pill = label(self.pill.upper(), "pill", wrap=False)
        pill.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.body.addWidget(pill)
        self.head = QHBoxLayout()
        text = QVBoxLayout()
        text.setSpacing(2)
        self.h2 = label(self.title, "h2")
        self.subline = label(self.sub, "sub")
        text.addWidget(self.h2)
        text.addWidget(self.subline)
        self.head.addLayout(text, 1)
        self.body.addLayout(self.head)
        self.build()
        self.body.addStretch(1)

    def build(self) -> None:  # pages add their cards here
        pass

    def reload(self) -> None:  # called when the wallet or identity changes
        pass

    def add(self, w: QWidget) -> QWidget:
        self.body.addWidget(w)
        return w

    def error(self, card: Card, text: str) -> None:
        card.tone("bad")
        self.app.status(text, ok=False)


# ----------------------------------------------------------- standing: chain


class Rail(QWidget):
    """The left column of one timeline row: an icon square, and the line
    down to the next row (dashed red when that link is broken)."""

    def __init__(self, kind: str, colour: str, line: str, fill: str, last: bool, dashed: bool):
        super().__init__()
        self.kind, self.colour, self.line, self.fill = kind, colour, line, fill
        self.last, self.dashed = last, dashed
        self.setFixedWidth(30)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(30, 44)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.last:
            pen = QPen(QColor(self.line), 2)
            if self.dashed:
                pen.setStyle(Qt.PenStyle.DashLine)
            p.setPen(pen)
            p.drawLine(15, 30, 15, self.height())
        p.setPen(QPen(QColor(self.colour), 2))
        p.setBrush(QColor(self.fill))
        p.drawRoundedRect(2, 2, 26, 26, 7, 7)
        p.drawPixmap(8, 8, theme.pixmap(self.kind, self.colour, 14))


class Chain(QWidget):
    """Standing as timeline rows (mockup option A): root, each delegation,
    and the signer, top to bottom, each with what the engine said of it."""

    def __init__(self, standing: dict, signer: str, tokens: dict):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 4, 0, 0)
        v.setSpacing(0)
        chain = list(standing.get("chain") or [])
        broken = standing.get("broken")
        good = standing.get("result") == "standing"
        rows = []
        for i, c in enumerate(chain):
            if c["role"] == "root":
                t = c.get("threshold")
                what = (
                    f"any {t['k']} of {t['n']} keys together · accepted by {c['accepted-by']}"
                    if t
                    else f"trusted by you · accepted by {c['accepted-by']} ({c['anchor']})"
                )
                rows.append(("trust", tokens["root"], c["key"], "root", what, ""))
            else:
                rows.append(("person", tokens["acc"], c["key"], "delegate", "given standing by the key above", ""))
        last_key = chain[-1]["key"] if chain else None
        if good and rows and last_key == signer:
            kind, colour, name, _, what, _ = rows[-1]
            rows[-1] = (kind, colour, name, "root · signer" if len(rows) == 1 else "signer", what, "✓ in scope")
        else:
            reason = standing.get("detail") or standing.get("text", "")
            rows.append(("keys", tokens["signer"], signer, "signer", reason if not good else "", "✓" if good else "✕"))
        for i, (kind, colour, name, role, what, mark) in enumerate(rows):
            last = i == len(rows) - 1
            nxt_broken = (not good) and (i == len(rows) - 2)
            line = tokens["bad"] if nxt_broken else tokens["acc"]
            h = QHBoxLayout()
            h.setSpacing(10)
            h.addWidget(Rail(kind, colour, line, tokens["field"], last, nxt_broken))
            text = QVBoxLayout()
            text.setSpacing(1)
            top = QHBoxLayout()
            top.addWidget(label(f"<b>{name}</b> &nbsp;<span style='color:{tokens['mut']}'>{role}</span>", wrap=False))
            top.addStretch(1)
            if mark:
                top.addWidget(label(mark, "ok" if mark.startswith("✓") else "bad", wrap=False))
            text.addLayout(top)
            if what:
                text.addWidget(label(what, "bad" if (last and not good) else "cap"))
            text.addSpacing(10)
            h.addLayout(text, 1)
            v.addLayout(h)
        if broken:
            v.addWidget(label(f"Broken link: {broken['from']} → {broken['to']}", "bad"))
