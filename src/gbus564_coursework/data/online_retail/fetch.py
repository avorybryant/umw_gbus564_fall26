#!/usr/bin/env python3
#
# Fetch the UCI Online Retail dataset and write it into this directory as a
# tracked, static, gzip-compressed CSV.
#
#   online_retail.csv.gz  (~7.6MB compressed, ~48MB raw, 541,909 rows) —
#   COMMITTED, unlike the ISLP/MLBA reference material under
#   course_prep/references/. Those are copyrighted textbook content and are
#   gitignored/regenerated locally; this dataset is a public UCI ML
#   Repository dataset and small enough to check in (gzipped) directly, so
#   every student and every run sees a byte-identical file with no
#   dependency on an external host being available during class. Gzipped
#   rather than raw CSV (~48MB) to keep the repo lean; pandas reads
#   `.csv.gz` transparently via `pd.read_csv`.
#
# Source: UCI Machine Learning Repository, "Online Retail" —
# https://archive.ics.uci.edu/dataset/352/online+retail. Transactions for a
# UK-based online retailer, Dec 2010-Dec 2011.
#
# Requires: python3, pandas, openpyxl (for the source .xlsx).
# Re-run any time to refresh from upstream.

import io
import zipfile
from pathlib import Path

import pandas as pd
import urllib.request

URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
OUT = Path(__file__).resolve().parent / "online_retail.csv.gz"


def main() -> None:
    print(f">> Fetching {URL}")
    with urllib.request.urlopen(URL) as resp:
        zip_bytes = resp.read()

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        xlsx_name = next(n for n in zf.namelist() if n.endswith(".xlsx"))
        with zf.open(xlsx_name) as f:
            df = pd.read_excel(f)

    df.to_csv(OUT, index=False, compression="gzip")
    print(f">> Wrote {OUT} ({len(df)} rows)")


if __name__ == "__main__":
    main()
