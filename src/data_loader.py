from pathlib import Path
import pandas as pd
import streamlit as st

from src.config import REQUIRED_COLUMNS


@st.cache_data(show_spinner="Validating portfolio dataset…")
def load_and_clean_data(path: Path | str, modified: float) -> tuple[pd.DataFrame, dict]:
    """
    Loads, audits, and cleans the European Bank portfolio dataset:
    - Validates presence of required schema fields.
    - Excludes records missing essential identifiers or targets.
    - Deduplicates CustomerId (retaining the first record).
    - Imputes missing continuous features with the median.
    - Imputes missing categorical/binary features with mode or 'Unknown'.
    - Calculates the 0-100 Relationship Score and assigns Relationship Tiers.
    """
    raw = pd.read_csv(path)
    missing_cols = REQUIRED_COLUMNS - set(raw.columns)
    if missing_cols:
        raise ValueError("Required columns missing: " + ", ".join(sorted(missing_cols)))

    audit = {
        "source_rows": len(raw),
        "missing_target": int(raw["Exited"].isna().sum()),
        "missing_id": int(raw["CustomerId"].isna().sum()),
        "duplicate_ids": int(raw["CustomerId"].duplicated().sum()),
    }

    # Data integrity: exclude missing essential identifiers or targets, keep first deduplicated ID
    df = raw.dropna(subset=["CustomerId", "Exited"]).copy()
    df = df.drop_duplicates(subset="CustomerId", keep="first")

    numeric = ["Balance", "EstimatedSalary", "NumOfProducts", "IsActiveMember", "Exited"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Missing value imputation: median for continuous, mode for binary
    for col in ["Balance", "EstimatedSalary", "NumOfProducts"]:
        df[col] = df[col].fillna(df[col].median())
    for col in ["IsActiveMember", "Exited"]:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode().iloc[0])

    for col in ["Geography", "Gender", "Surname"]:
        if col in df:
            df[col] = df[col].fillna("Unknown").astype(str)

    df["CustomerId"] = df["CustomerId"].astype("int64").astype(str)
    df["Exited"] = df["Exited"].astype(int)
    df["IsActiveMember"] = df["IsActiveMember"].astype(int)
    df["NumOfProducts"] = df["NumOfProducts"].round().astype(int)
    df["Engagement"] = df["IsActiveMember"].map({1: "Active", 0: "Inactive"}).fillna("Unknown")

    # Transparent 0–100 relationship-strength scoring methodology:
    # 60 pts for active membership + up to 40 pts for product breadth (1 product = 0, 4+ products = 40)
    df["Relationship Score"] = (
        df["IsActiveMember"].clip(0, 1) * 60
        + df["NumOfProducts"].clip(1, 4).sub(1).div(3).clip(0, 1) * 40
    ).round().astype(int)

    df["Relationship Tier"] = pd.cut(
        df["Relationship Score"],
        [-1, 39, 69, 100],
        labels=["Fragile", "Developing", "Strong"],
    ).astype(str)

    df["Churn Status"] = df["Exited"].map({1: "Exited", 0: "Retained"})

    return df, audit


def filter_portfolio(
    df: pd.DataFrame,
    selected_engagement: list[str],
    selected_geos: list[str],
    selected_prod_range: tuple[int, int],
    selected_balance_min: float,
    selected_salary_min: float,
) -> pd.DataFrame:
    """Filter the customer DataFrame based on chosen sidebar controls."""
    return df[
        df["Engagement"].isin(selected_engagement)
        & df["Geography"].isin(selected_geos)
        & df["NumOfProducts"].between(selected_prod_range[0], selected_prod_range[1])
        & (df["Balance"] >= selected_balance_min)
        & (df["EstimatedSalary"] >= selected_salary_min)
    ].copy()
