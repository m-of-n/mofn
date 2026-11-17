"""`mofn-wallet [--wallet DIR] [--self-test] [--version]`."""

import argparse
import sys


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="mofn-wallet", description="The m-of-n desktop wallet (prototype).")
    p.add_argument("--wallet", metavar="DIR", help="wallet folder (default: $MOFN_WALLET, else ~/Projects/wallet/mofn)")
    p.add_argument("--self-test", action="store_true", help="check the engine end to end without a window, then exit")
    p.add_argument("--version", action="store_true")
    # macOS passes -psn_… to apps opened from Finder on some versions.
    a, _ = p.parse_known_args(argv)

    from . import core

    if a.version:
        print(f"mofn-wallet {core.VERSION} (prototype: {' and '.join(core.OPEN)} are open; do not use real keys)")
        return 0
    if a.self_test:
        return core.self_test() or window_test()

    from PySide6.QtWidgets import QApplication

    from .window import Window

    app = QApplication(sys.argv[:1])
    app.setOrganizationName("m-of-n")
    app.setApplicationName("mofn-wallet")
    w = Window(core.resolve_wallet(a.wallet) if a.wallet else None)
    w.show()
    return app.exec()


def window_test() -> int:
    """The second half of --self-test: Qt's plugins load from the bundle and
    every page builds, on a throwaway wallet, with no screen needed."""
    import os
    import tempfile

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtCore import QSettings
    from PySide6.QtWidgets import QApplication

    from . import core
    from .window import PAGES, Window

    with tempfile.TemporaryDirectory() as tmp:
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, tmp)
        app = QApplication([])
        w = Window(core.Session(tmp + "/wallet").root)
        for _, items in PAGES:
            for name, _, _ in items:
                w.go(name)
        pages = w.pages["Learn"].list.count()
        w.close()
        app.quit()
    if pages < 6:
        print(f"self-test: Learn has {pages} pages; the bundle is missing screens/learn", file=sys.stderr)
        return 1
    print("mofn-wallet window self-test: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
