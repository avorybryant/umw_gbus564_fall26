"""Shared loaders for the course's notebook-portfolio datasets (see course_prep/course_data.md)."""

from importlib.resources import files

import pandas as pd

_DATA_DIR = files("gbus564_coursework.data")


def load_churn() -> pd.DataFrame:
    """Telco Customer Churn — one row per customer, binary Churn label (1 = churned)."""
    df = pd.read_csv(_DATA_DIR / "telco_churn" / "telco_customer_churn.csv")
    df = df.drop(columns="customerID")
    # 11 customers with tenure == 0 have a blank TotalCharges (no bill yet) — treat as 0.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df


def load_housing() -> pd.DataFrame:
    """Ames Housing — one row per home sale, numeric target SalePrice ($)."""
    df = pd.read_csv(_DATA_DIR / "housing" / "ames_housing.csv")
    df = df.drop(columns=["Order", "PID"])
    df.columns = df.columns.str.replace(" ", "", regex=False)
    # A handful of homes have no basement/garage: the corresponding numeric
    # measurements are blank rather than 0 in the source file.
    no_feature_cols = ["TotalBsmtSF", "BsmtFinSF1", "BsmtFinSF2", "BsmtUnfSF",
                        "BsmtFullBath", "BsmtHalfBath", "GarageCars", "GarageArea"]
    df[no_feature_cols] = df[no_feature_cols].fillna(0)
    return df


def load_online_retail() -> pd.DataFrame:
    """Online Retail — one row per invoice line, UK online retailer, Dec 2010-Dec 2011.

    Used across Week 4 (recommender, customer segmentation) and Week 6
    (autoencoder anomaly detection); this loader only fixes the data-quality
    issues true for every use, leaving matrix-building/aggregation to each
    notebook.
    """
    df = pd.read_csv(_DATA_DIR / "online_retail" / "online_retail.csv.gz")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    # ~25% of rows have no CustomerID (guest/unattributed orders) — no basis
    # for a per-customer row or column, so they can't support CF or segmentation.
    df = df.dropna(subset=["CustomerID"])
    df["CustomerID"] = df["CustomerID"].astype(int)
    # Cancelled orders are flagged with a "C"-prefixed InvoiceNo and carry
    # negative Quantity; a handful of other rows have non-positive Quantity/
    # UnitPrice (adjustments, testing SKUs) — neither reflects a real purchase.
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    return df.reset_index(drop=True)


def load_aus_retail() -> pd.DataFrame:
    """Australian retail trade turnover — one row per (State, Industry, Month),
    monthly Turnover ($M AUD). Source: Australian Bureau of Statistics,
    catalogue 8501.0 table 11, via fpppy's data appendix (CC BY 4.0).

    152 parallel State x Industry series, 1982 onward — used for Week 7
    (forecasting); each notebook filters/aggregates to the series it needs
    (e.g. summing across states for a national industry total), same
    aggregate-per-notebook pattern as load_online_retail().
    """
    df = pd.read_csv(_DATA_DIR / "aus_retail" / "aus_retail.csv")
    df["Month"] = pd.to_datetime(df["Month"])
    return df
