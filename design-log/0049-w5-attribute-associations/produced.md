---
schema: "design-log/v1"
id: DL-0049
part: produced
date: "2026-11-16"
---

# DL-0049 — produced

- **`engine/check.py`**: `associations(answer)`, called from
  `Answer.to_json()` as the new `associations` key. One entry per
  (attestation, attribute) the answer describes — the attestations about your
  file, else every verified attestation (the integrity-fail case). Each entry:
  `statement`, `file`, `signed-by`, `topic`, `subject`, `standing`.
  - `standing` is **read from `Coverage`**: a `Covered` gives the anchor plus
    `Covered.path` hops; a `ThresholdCovered` gives the threshold root; a
    `Stopped` gives `no-standing`, its §10.3 code and detail, the hops
    followed, and the broken link (`Stopped.link`). With no coverage (no
    statement about your file), `not-evaluated`. Nothing is reduced again.
  - `signed-by.principal` is taken from `Coverage.names` (the name anchors the
    reduction resolved) when one resolved to the signer.
  - `Answer` gains `described` and `definition` (defaults, so existing
    constructors still work).
- **`engine/render.py`**: `name_text` for `[7, kid, [label…]]`.
- **`screens/forms.py`**: `associations()` renders the four under every
  verdict in the Check tab, from the JSON only; a digest that is not your
  file's is shown next to yours in red.
- **README**: *Who signed, topic, digest, standing* (also shown in Learn's
  Check page) and *The verdict as JSON* (the shape W-7 reads).
- **Tests** (474 pass, was 460): `tests/test_associations.py` — the three
  slice cases end to end under both codecs against
  `fixtures/golden/associations-{green,unauthorized,tampered}.json`, and
  standing through E-2 (delegation), E-4 (broken link, `widening`), E-11
  (threshold). `tests/test_screens.py` — a pilot test that drives the Check
  tab through authorization fail, integrity fail and (after Trust) green,
  re-runs each argv as a separate `mofn` process, asserts the JSON is
  identical, and asserts each of the four is on screen.
- wallet **0.9.0** (MINOR: behaviour added), CHANGELOG entry.
