"""Colours, the stylesheet and the icons (W-7 mockup v2/v3, approved
2026-11-17: graphite, violet accent, green pass / red fail).

One token table per scheme; the stylesheet is written once against the
tokens. Icons are inline SVG strokes (Lucide-style shapes drawn here), so
nothing is downloaded and no icon font is bundled.
"""

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPixmap

DARK = {
    "bg": "#0c0c0e", "side": "#121214", "card": "#18181b", "field": "#111113",
    "line": "#2a2a2f", "fg": "#ececef", "mut": "#8b8b94", "soft": "#c4c4cc",
    "acc": "#8b7cf6", "acc_bg": "#232029", "acc_fg": "#b9aefc", "pill_bg": "#25203d",
    "who_bg": "#1d1a2e", "who_line": "#5b4fc4", "btn_bg": "#d9d4ff", "btn_fg": "#16131f",
    "ok": "#2fbf8f", "ok_bg": "#132b25", "ok_line": "#2f7a5f", "ok_chip": "#1e5a47", "ok_chip_fg": "#7ff0c6",
    "bad": "#ef5a6f", "bad_bg": "#2b1319", "bad_line": "#8a2f3d", "bad_chip": "#5a1e2a", "bad_chip_fg": "#ffb0bb",
    "warn": "#f0a447", "warn_bg": "#231a10", "warn_line": "#6b4a1c", "root": "#ef5a6f", "signer": "#3fd0e0",
}
LIGHT = {
    "bg": "#f6f6f8", "side": "#ededf0", "card": "#ffffff", "field": "#f6f6f8",
    "line": "#dcdce2", "fg": "#18181b", "mut": "#6b6b75", "soft": "#3a3a42",
    "acc": "#6d5ce8", "acc_bg": "#e7e3fd", "acc_fg": "#4b3cc4", "pill_bg": "#ebe7fe",
    "who_bg": "#efecfe", "who_line": "#a99ff2", "btn_bg": "#4b3cc4", "btn_fg": "#ffffff",
    "ok": "#178a65", "ok_bg": "#e6f6f0", "ok_line": "#8fd3bb", "ok_chip": "#c9efe1", "ok_chip_fg": "#0f6a4d",
    "bad": "#c9324a", "bad_bg": "#fdecef", "bad_line": "#eba5b0", "bad_chip": "#f8d3da", "bad_chip_fg": "#9b1f33",
    "warn": "#9a5b0c", "warn_bg": "#fdf2e2", "warn_line": "#e8c48f", "root": "#c9324a", "signer": "#0f8fa0",
}

SHEET = """
QWidget {{ color: {fg}; font-size: 13px; }}
QMainWindow, #content, #page, QScrollArea, QScrollArea > QWidget > QWidget {{ background: {bg}; }}
#sidebar {{ background: {side}; border-right: 1px solid {line}; }}
#topbar {{ border-bottom: 1px solid {line}; }}
#statusbar {{ border-top: 1px solid {line}; }}
#statusbar QLabel {{ color: {mut}; font-size: 11px; }}
#cmd {{ font-family: Menlo, monospace; color: {soft}; }}
#section {{ color: {mut}; font-size: 9px; font-weight: 700; letter-spacing: 2px; }}
#title {{ font-size: 16px; font-weight: 600; }}
#h2 {{ font-size: 19px; font-weight: 700; }}
#sub, #cap {{ color: {mut}; }}
#cap {{ font-size: 11px; }}
#mono {{ font-family: Menlo, monospace; font-size: 11px; color: {soft}; }}
#pill {{ background: {pill_bg}; color: {acc_fg}; font-size: 9px; font-weight: 700;
        letter-spacing: 2px; padding: 3px 9px; border-radius: 9px; }}
#lab {{ color: {mut}; font-size: 9px; font-weight: 700; letter-spacing: 2px; }}
#card {{ background: {card}; border: 1px solid {line}; border-radius: 12px; }}
#card[tone="ok"] {{ background: {ok_bg}; border-color: {ok_line}; }}
#card[tone="bad"] {{ background: {bad_bg}; border-color: {bad_line}; }}
#chip[tone="ok"] {{ background: {ok_chip}; color: {ok_chip_fg}; }}
#chip[tone="bad"] {{ background: {bad_chip}; color: {bad_chip_fg}; }}
#chip {{ font-weight: 800; letter-spacing: 2px; padding: 3px 12px; border-radius: 10px; }}
#big {{ font-size: 26px; font-weight: 700; }}
#ok {{ color: {ok}; font-weight: 600; }}
#bad {{ color: {bad}; font-weight: 600; }}
#badge {{ background: {warn_bg}; border: 1px solid {warn_line}; color: {warn}; font-size: 9px;
         font-weight: 700; letter-spacing: 1px; border-radius: 8px; padding: 6px; }}
#who {{ background: {who_bg}; border: 1px solid {who_line}; border-radius: 9px; padding: 6px; text-align: left; }}
#nav {{ background: transparent; border: none; border-radius: 7px; padding: 6px 8px; text-align: left; color: {soft}; }}
#nav:hover {{ background: {acc_bg}; }}
#nav:checked {{ background: {acc_bg}; color: {fg}; border-left: 2px solid {acc}; }}
#dashed {{ background: transparent; border: 1px dashed {line}; border-radius: 8px; color: {mut}; padding: 5px; }}
#wallet {{ background: transparent; border: none; border-top: 1px solid {line}; color: {mut};
          text-align: left; padding: 6px 4px; font-size: 11px; }}
QPushButton {{ background: transparent; border: 1px solid {line}; border-radius: 7px; padding: 5px 12px; color: {soft}; }}
QPushButton:hover {{ border-color: {acc}; }}
QPushButton#primary {{ background: {btn_bg}; color: {btn_fg}; border: none; font-weight: 700; padding: 6px 16px; }}
QPushButton#primary:disabled {{ background: {line}; color: {mut}; }}
QPushButton#seg {{ border-radius: 0; padding: 3px 10px; color: {mut}; font-size: 11px; }}
QPushButton#seg:checked {{ background: {line}; color: {fg}; }}
QPushButton#icon {{ border: none; padding: 4px; }}
QLineEdit, QComboBox, QSpinBox, QPlainTextEdit, QTextBrowser, QListWidget {{
    background: {field}; border: 1px solid {line}; border-radius: 7px; padding: 4px 8px; color: {fg};
    selection-background-color: {acc}; }}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{ border-color: {acc}; }}
QComboBox QAbstractItemView {{ background: {card}; border: 1px solid {line}; selection-background-color: {acc_bg}; }}
QCheckBox {{ spacing: 6px; }}
QTableWidget {{ background: transparent; border: none; gridline-color: transparent; }}
QTableWidget::item {{ border-bottom: 1px solid {line}; padding: 4px; }}
QHeaderView, QTableCornerButton::section {{ background: transparent; border: none; }}
QHeaderView::section {{ background: transparent; color: {mut}; border: none; border-bottom: 1px solid {line};
    font-size: 9px; font-weight: 700; letter-spacing: 2px; padding: 4px; }}
QMenu {{ background: {card}; border: 1px solid {line}; padding: 4px; }}
QMenu::item {{ padding: 5px 16px; border-radius: 5px; }}
QMenu::item:selected {{ background: {acc_bg}; }}
QScrollBar:vertical {{ background: transparent; width: 8px; }}
QScrollBar::handle:vertical {{ background: {line}; border-radius: 4px; min-height: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
QToolTip {{ background: {card}; color: {fg}; border: 1px solid {line}; }}
"""


def sheet(tokens: dict) -> str:
    return SHEET.format(**tokens)


# --------------------------------------------------------------------- icons

PATHS = {
    "overview": '<path d="M3 11l9-8 9 8v10H3z"/>',
    "keys": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
    "trust": '<path d="M12 3l8 4v5c0 5-4 8-8 9-4-1-8-4-8-9V7z"/>',
    "sign": '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
    "verify": '<path d="M5 12l5 5L20 7"/>',
    "show": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "learn": '<path d="M4 5h7v14H4zM13 5h7v14h-7z"/>',
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 15-5 16 0"/>',
    "sidebar": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5"/>',
    "moon": '<path d="M20 14A8 8 0 1 1 10 4a6 6 0 0 0 10 10z"/>',
    "system": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
}


def icon(name: str, colour: str, size: int = 32) -> QIcon:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}" '
        f'fill="none" stroke="{colour}" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round">{PATHS[name]}</svg>'
    )
    pm = QPixmap()
    pm.loadFromData(QByteArray(svg.encode()), "SVG")
    return QIcon(pm)


def pixmap(name: str, colour: str, size: int = 16) -> QPixmap:
    return icon(name, colour, size * 2).pixmap(size, size)


ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
