import pandas as pd
import streamlit as st
from src.utils.helpers import format_euro

def render_portfolio_filters(df: pd.DataFrame) -> dict:
    """
    Renders the dedicated global Portfolio Filters panel on the Overview page:
    - Positioned between page heading and KPI cards.
    - Contains 7 required filters across logical financial & profile columns.
    - Synchronized with session_state for seamless persistence.
    - Interactive 'Reset All Filters' button.
    - Displays active filter summary chips.
    """
    # Initialize session state keys with application defaults if not set
    if "filter_engagement" not in st.session_state:
        st.session_state["filter_engagement"] = ["Active", "Inactive"]
    if "filter_geo" not in st.session_state:
        st.session_state["filter_geo"] = ["France", "Germany", "Spain"]
    min_p, max_p = int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max())
    if "filter_products" not in st.session_state:
        st.session_state["filter_products"] = (min_p, max_p)
    if "filter_balance_min" not in st.session_state:
        st.session_state["filter_balance_min"] = 0
    if "filter_salary_min" not in st.session_state:
        st.session_state["filter_salary_min"] = 0
    if "filter_balance_cutoff" not in st.session_state:
        st.session_state["filter_balance_cutoff"] = int(df["Balance"].quantile(0.75))
    if "filter_salary_cutoff" not in st.session_state:
        st.session_state["filter_salary_cutoff"] = int(df["EstimatedSalary"].quantile(0.75))

    max_bal = int(df["Balance"].max())
    max_sal = int(df["EstimatedSalary"].max())

    with st.expander("🔍 **Portfolio Filters & Segment Configuration**", expanded=True):
        # Row 1: Profile & Engagement Filters
        c1, c2, c3 = st.columns([1.2, 1.3, 1.5])

        with c1:
            selected_engagement = st.multiselect(
                "Engagement Status",
                options=["Active", "Inactive"],
                default=st.session_state["filter_engagement"],
                help="Filter by active vs dormant banking status.",
                key="pf_engagement",
            )
            st.session_state["filter_engagement"] = selected_engagement

        with c2:
            all_geos = ["France", "Germany", "Spain"]
            selected_geos = st.multiselect(
                "Geography",
                options=all_geos,
                default=[g for g in st.session_state["filter_geo"] if g in all_geos] or all_geos,
                help="Filter by country market location.",
                key="pf_geo",
            )
            st.session_state["filter_geo"] = selected_geos

        with c3:
            selected_prod_range = st.slider(
                "Products Held",
                min_value=min_p,
                max_value=max_p,
                value=st.session_state["filter_products"],
                step=1,
                help="Customer range of products held (1 to 4).",
                key="pf_products",
            )
            st.session_state["filter_products"] = selected_prod_range

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        # Row 2: Financial Inclusions & High-Value Cutoffs
        f1, f2, f3, f4 = st.columns(4)

        with f1:
            selected_balance_min = st.slider(
                "Min Account Balance (€)",
                min_value=0,
                max_value=max_bal,
                value=int(st.session_state["filter_balance_min"]),
                step=5000,
                format="€%d",
                help="Portfolio inclusion floor for deposits.",
                key="pf_balance_min",
            )
            st.session_state["filter_balance_min"] = selected_balance_min

        with f2:
            selected_salary_min = st.slider(
                "Min Estimated Salary (€)",
                min_value=0,
                max_value=max_sal,
                value=int(st.session_state["filter_salary_min"]),
                step=5000,
                format="€%d",
                help="Portfolio inclusion floor for estimated salary.",
                key="pf_salary_min",
            )
            st.session_state["filter_salary_min"] = selected_salary_min

        with f3:
            balance_cutoff = st.number_input(
                "High-Value Balance (€)",
                min_value=0,
                max_value=max_bal,
                value=int(st.session_state["filter_balance_cutoff"]),
                step=5000,
                help="Qualification threshold: balance ≥ threshold constitutes high value.",
                key="pf_bal_cut",
            )
            st.session_state["filter_balance_cutoff"] = balance_cutoff

        with f4:
            salary_cutoff = st.number_input(
                "High-Value Salary (€)",
                min_value=0,
                max_value=max_sal,
                value=int(st.session_state["filter_salary_cutoff"]),
                step=5000,
                help="Qualification threshold: salary ≥ threshold constitutes high value.",
                key="pf_sal_cut",
            )
            st.session_state["filter_salary_cutoff"] = salary_cutoff

        # Active filters readout & Reset button
        st.markdown("<hr style='margin:10px 0 8px 0; border:none; border-top:1px solid #e9ede8;'>", unsafe_allow_html=True)
        bot_col1, bot_col2 = st.columns([5, 1])

        with bot_col1:
            eng_str = ", ".join(selected_engagement) if selected_engagement else "None"
            geo_str = ", ".join(selected_geos) if selected_geos else "None"
            st.markdown(
                f"<div style='font-size:11px; color:#7c8882; line-height:1.6;'>"
                f"<b>Active Filter Selections:</b> "
                f"<span style='background:#f0f4f1; color:#183c35; padding:2px 7px; border-radius:4px; font-weight:600;'>Engagement: {eng_str}</span> &nbsp;"
                f"<span style='background:#f0f4f1; color:#183c35; padding:2px 7px; border-radius:4px; font-weight:600;'>Regions: {geo_str}</span> &nbsp;"
                f"<span style='background:#f0f4f1; color:#183c35; padding:2px 7px; border-radius:4px; font-weight:600;'>Products: {selected_prod_range[0]}–{selected_prod_range[1]}</span> &nbsp;"
                f"<span style='background:#f0f4f1; color:#183c35; padding:2px 7px; border-radius:4px; font-weight:600;'>Balance ≥ {format_euro(selected_balance_min)}</span> &nbsp;"
                f"<span style='background:#f0f4f1; color:#183c35; padding:2px 7px; border-radius:4px; font-weight:600;'>Salary ≥ {format_euro(selected_salary_min)}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        with bot_col2:
            if st.button("↺ Reset All Filters", use_container_width=True):
                st.session_state["filter_engagement"] = ["Active", "Inactive"]
                st.session_state["filter_geo"] = ["France", "Germany", "Spain"]
                st.session_state["filter_products"] = (min_p, max_p)
                st.session_state["filter_balance_min"] = 0
                st.session_state["filter_salary_min"] = 0
                st.session_state["filter_balance_cutoff"] = int(df["Balance"].quantile(0.75))
                st.session_state["filter_salary_cutoff"] = int(df["EstimatedSalary"].quantile(0.75))
                st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    return {
        "engagement": selected_engagement,
        "geos": selected_geos,
        "prod_range": selected_prod_range,
        "balance_min": selected_balance_min,
        "salary_min": selected_salary_min,
        "balance_cutoff": balance_cutoff,
        "salary_cutoff": salary_cutoff,
    }
