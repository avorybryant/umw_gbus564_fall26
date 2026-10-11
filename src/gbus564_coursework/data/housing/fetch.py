#!/usr/bin/env python3
#
# Fetch the Ames Housing dataset and write it into this directory as a
# tracked, static CSV.
#
#   ames_housing.csv  (~2,930 rows, ~1MB) — COMMITTED, unlike the ISLP/MLBA
#   reference material under course_prep/references/. Those are copyrighted
#   textbook content and are gitignored/regenerated locally; this dataset is
#   public-domain assessor records compiled explicitly for teaching reuse, and
#   small enough to check in directly, so every student and every run sees a
#   byte-identical file with no dependency on an external host being
#   available during class.
#
# Source: Dean De Cock, "Ames, Iowa: Alternative to the Boston Housing Data
# as an End of Semester Regression Project," Journal of Statistics Education
# 19:3 (2011) — http://jse.amstat.org/v19n3/decock/AmesHousing.txt. Compiled
# from Ames City Assessor's Office public records; this is the original,
# canonical source for the dataset widely mirrored elsewhere (e.g. Kaggle's
# "House Prices" competition).
#
# Requires: python3 (stdlib only).
# Re-run any time to refresh from upstream.

import csv
import urllib.request
from pathlib import Path

URL = "http://jse.amstat.org/v19n3/decock/AmesHousing.txt"
OUT = Path(__file__).resolve().parent / "ames_housing.csv"


def main() -> None:
    print(f">> Fetching {URL}")
    with urllib.request.urlopen(URL) as resp:
        text = resp.read().decode("utf-8")

    rows = list(csv.reader(text.splitlines(), delimiter="\t"))
    with open(OUT, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f">> Wrote {OUT} ({len(rows) - 1} rows)")


if __name__ == "__main__":
    main()
