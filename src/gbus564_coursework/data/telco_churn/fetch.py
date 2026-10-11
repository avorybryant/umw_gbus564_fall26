#!/usr/bin/env python3
#
# Fetch the Telco Customer Churn sample dataset and write it into this
# directory as a tracked, static CSV.
#
#   telco_customer_churn.csv  (~950 KB, 7,043 customers) — COMMITTED, unlike
#   the ISLP/MLBA reference material under course_prep/references/. Those are
#   copyrighted textbook content and are gitignored/regenerated locally; this
#   dataset is Apache-2.0 licensed and small enough to check in directly, so
#   every student and every run sees a byte-identical file with no dependency
#   on an external host (or Kaggle auth) being available during class.
#
# Source: https://github.com/IBM/telco-customer-churn-on-icp4d (Apache-2.0),
# IBM's official mirror of the well-known "Telco Customer Churn" sample —
# the same data distributed via the Kaggle listing, without Kaggle's auth
# requirement.
#
# Requires: python3 (stdlib only).
# Re-run any time to refresh from upstream.

import urllib.request
from pathlib import Path

URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)
OUT = Path(__file__).resolve().parent / "telco_customer_churn.csv"


def main() -> None:
    print(f">> Fetching {URL}")
    urllib.request.urlretrieve(URL, OUT)
    print(f">> Wrote {OUT}")


if __name__ == "__main__":
    main()
