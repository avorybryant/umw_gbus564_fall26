#!/usr/bin/env python3
#
# Fetch the Australian retail trade turnover dataset and write it into this
# directory as a tracked, static CSV.
#
#   aus_retail.csv  (~64,500 rows, ~3MB) — COMMITTED, unlike the ISLP/MLBA/
#   fpppy reference material under course_prep/references/. Those are
#   copyrighted textbook content and are gitignored/regenerated locally;
#   this dataset's underlying source (Australian Bureau of Statistics,
#   catalogue 8501.0, table 11) is published under CC BY 4.0 — free to
#   reuse, adapt, and redistribute with attribution, for any purpose
#   including commercial. Small enough to check in directly, so every
#   student and every run sees a byte-identical file with no dependency on
#   an external host being available during class.
#
# Source: fpppy (Hyndman, Athanasopoulos, et al., "Forecasting: Principles
# and Practice, the Pythonic Way") hosts this as a flat CSV for readers —
# https://otexts.com/fpppy/data/aus_retail.csv — the same data bundled in
# the tsibbledata R package (github.com/tidyverts/tsibbledata, GPL-3),
# originally from the Australian Bureau of Statistics under CC BY 4.0
# (https://www.abs.gov.au/website-privacy-copyright-and-disclaimer).
#
# NOTE: otexts.com blocks requests whose User-Agent matches known
# library/browser signatures (Python-urllib, python-requests, Chrome) but
# allows a plain "curl"-style UA — confirmed empirically, not documented
# anywhere. Keep the UA override below even though it looks unnecessary.
#
# Requires: python3 (stdlib only).
# Re-run any time to refresh from upstream.

import urllib.request
from pathlib import Path

URL = "https://otexts.com/fpppy/data/aus_retail.csv"
OUT = Path(__file__).resolve().parent / "aus_retail.csv"


def main() -> None:
    print(f">> Fetching {URL}")
    req = urllib.request.Request(URL, headers={"User-Agent": "curl/8.5.0"})
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode("utf-8")

    OUT.write_text(text)
    n_rows = text.count("\n") - 1
    print(f">> Wrote {OUT} ({n_rows} rows)")


if __name__ == "__main__":
    main()
