# Download

!!! warning "Prototype pre-releases"
    These builds exist to demonstrate the design. The architecture is a draft
    with open decisions; **do not use real keys** and do not rely on a verdict.

## The macOS app

**[Releases of the wallet](https://github.com/m-of-n/mofn/releases?q=wallet-v&expanded=true)**
— open the newest one and download:

| file | what it is |
|---|---|
| `mofn-wallet-X.Y.Z-macos-arm64.dmg` | **the desktop app**: a disk image, for macOS 13 or later on Apple silicon |
| `mofn-wallet-X.Y.Z-macos-arm64.zip` | the same app, zipped |
| `SHA256SUMS` | the checksums of every file in the release |

(`/releases/latest` skips pre-releases, which is all these are, so the link
above lists them instead.)

1. **Check it** before you open it, in the folder you downloaded to:

    ```sh
    shasum -a 256 --ignore-missing -c SHA256SUMS
    gh attestation verify mofn-wallet-X.Y.Z-macos-arm64.dmg -R m-of-n/mofn
    ```

    The checksum shows the file is the one in the release; the attestation
    (Sigstore) shows this repository's release workflow built it, from the
    tagged commit.

2. **Install:** double-click the DMG and drag **m-of-n Wallet** onto the
   **Applications** shortcut.

3. **Open it.** Each release's notes say whether the app is signed and
   notarized by Apple.

    - **Notarized:** it opens normally.
    - **Not notarized:** macOS blocks the first launch. Open
      **System Settings → Privacy & Security** and choose **Open Anyway**, or
      run `xattr -dr com.apple.quarantine "/Applications/m-of-n Wallet.app"`
      once.

## The command line, and the details

The same releases have `mofn` for macOS (Apple silicon) and Linux (x86-64),
each with the same checks. The steps, the checks and what each proves are on
[Install the wallet](project/APP-0005-install-wallet.md).
