# Customer Engagement & Product Utilization Analytics

A Streamlit dashboard for exploring customer engagement, product usage, historical churn, relationship strength, and high-value disengaged customers using the supplied European Bank dataset.

## Run locally

1. Install Python 3.10 or newer.
2. From this folder, create and activate a virtual environment if desired.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

The application loads `data/European_Bank.csv` relative to `app.py`. Put a replacement file at that path to analyze a refreshed snapshot. On load, the app checks its required fields, excludes rows without a customer ID or churn outcome, deduplicates IDs (keeping the first row), imputes missing numeric values with the median, fills missing categories with `Unknown`, and fills missing binary flags with the mode. The included file needs no imputation or row exclusion.

## Dashboard features

- KPI cards for churn, retention, active membership, average product count, and high-value disengaged customers.
- Filters for engagement, product count, minimum balance, and minimum estimated salary. All visible metrics, charts, narratives, and the customer list respond to these filters.
- Charts for engagement and product-count churn, a two-way churn heatmap, balance/salary/outcome, and relationship-strength distribution.
- High-value disengaged customer table with CSV download.
- Expandable executive readout, dataset profile, assumptions, and limitations.

## Metric definitions

- **Churn rate:** share of customers with `Exited = 1` in the current filtered view.
- **Relationship score:** 60 points for active membership plus up to 40 points for product breadth, linearly scaled from 1 product (0 points) to 4+ products (40 points). Tiers are Fragile (0–39), Developing (40–69), and Strong (70–100). This is a transparent portfolio heuristic, not a validated loyalty score.
- **High-value disengaged:** inactive customers meeting either the chosen balance or salary cutoff. The default cutoffs are each full-dataset 75th percentile: balance €127,644.24 and salary €149,388.25. Adjust these independently in the sidebar.
- **Engagement:** the dataset's single `IsActiveMember` flag. It does not capture login frequency or recency.

All comparisons describe historical associations in the provided data. They do not show causality or estimate future individual churn. The data does not include transaction history, product types, or longitudinal engagement.

## Data provenance

The included CSV is copied from the user-provided `European_Bank.csv`. The dashboard does not fabricate or precompute customer results; metrics are calculated from the loaded file at runtime.
