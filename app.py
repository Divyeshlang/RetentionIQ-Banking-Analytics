from pathlib import Path
import streamlit as st

from src.config import DATA_PATH
from src.data_loader import load_and_clean_data, filter_portfolio
from src.styles.theme import apply_custom_theme
from src.components.sidebar import render_sidebar
from src.components.portfolio_filters import render_portfolio_filters
from src.components.kpi_cards import render_kpis
from src.components.charts import (
    render_engagement_chart,
    render_product_chart,
    render_relationship_tier_section,
)
from src.components.priority_table import render_customers_requiring_attention_page
from src.components.recommendations import render_strategic_recommendations_page
from src.components.risk_studio import render_risk_studio_page

# Page Configuration with European Bank styling
st.set_page_config(
    page_title="European Bank | Customer Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply unified Northstar European Bank design system
apply_custom_theme()

# Load verified dataset (preserving all validation, ingestion, and preprocessing routines)
try:
    df, audit = load_and_clean_data(DATA_PATH, DATA_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.info(f"Ensure European_Bank.csv is available at {DATA_PATH}.")
    st.stop()

# Render Northstar interactive sidebar with brand and navigation
nav_state = render_sidebar(df)
active_page = nav_state["page"]

# ----------------- PAGE ROUTING -----------------
if active_page == "Risk Studio":
    render_risk_studio_page(df)

elif active_page == "Customers Requiring Attention":
    render_customers_requiring_attention_page(df)

elif active_page == "Strategic Portfolio Recommendations":
    render_strategic_recommendations_page(df)

else:
    # ========================================================
    # OVERVIEW PAGE
    # ========================================================
    # Section 1: Page Header
    st.markdown("""
    <div class="northstar-page-heading">
        <div>
            <div class="northstar-eyebrow">
                <span class="northstar-eyebrow-mark">✦</span> PORTFOLIO SNAPSHOT · 2025 EUROPEAN BANK DATASET
            </div>
            <h1 class="northstar-heading-title">Customer Loyalty & Retention Dashboard</h1>
            <p class="northstar-heading-subtitle">
                Monitor customer engagement, retention performance, product utilization, and relationship risk across the banking portfolio.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Global Portfolio Filters Panel (created in Step 2)
    filters = render_portfolio_filters(df)

    # Filter dataset dynamically using active global filters
    view = filter_portfolio(
        df,
        selected_engagement=filters["engagement"],
        selected_geos=filters["geos"],
        selected_prod_range=filters["prod_range"],
        selected_balance_min=filters["balance_min"],
        selected_salary_min=filters["salary_min"],
    )

    # Filtered segment count subtitle
    st.markdown(
        f"<div style='font-size:12px; color:#7c8882; margin:-4px 0 14px 2px;'>"
        f"Displaying <b>{len(view):,}</b> filter-matched accounts (out of <b>{len(df):,}</b> total verified accounts)."
        f"</div>",
        unsafe_allow_html=True,
    )

    if view.empty:
        st.warning("⚠️ No customers match the selected filter combination. Please expand your filters above.")
        st.stop()

    # Section 2: Four KPI Cards (Horizontal row on desktop)
    at_risk_df = render_kpis(
        view=view,
        total_portfolio_size=len(df),
        balance_cutoff=filters["balance_cutoff"],
        salary_cutoff=filters["salary_cutoff"],
    )

    # Sections 3 & 4: Customer Engagement vs Churn and Product Adoption Charts
    c_left, c_right = st.columns(2)
    with c_left:
        render_engagement_chart(view)

    with c_right:
        render_product_chart(view)
