import pandas as pd
import streamlit as st

from src.utils.helpers import format_euro

def render_kpis(view: pd.DataFrame, total_portfolio_size: int, balance_cutoff: float, salary_cutoff: float) -> pd.DataFrame:
    """
    Renders the 4 Northstar KPI cards in a 4-column horizontal desktop row:
    1. Churn Rate (Percentage and exited count)
    2. Retention Rate (Percentage and retained count)
    3. Active Customers (Count and filtered portfolio percentage)
    4. At-Risk High-Value Customers (Count and short qualification explanation)
    """
    total_count = len(view)
    churn_count = int(view["Exited"].sum())
    churn_rate = view["Exited"].mean() if total_count > 0 else 0.0
    retained_rate = 1.0 - churn_rate
    retained_count = total_count - churn_count
    active_count = int(view["IsActiveMember"].sum())
    active_share = view["IsActiveMember"].mean() if total_count > 0 else 0.0

    at_risk_df = view[
        (view["IsActiveMember"] == 0)
        & ((view["Balance"] >= balance_cutoff) | (view["EstimatedSalary"] >= salary_cutoff))
    ].copy()
    at_risk_count = len(at_risk_df)
    at_risk_share = at_risk_count / total_count if total_count > 0 else 0.0

    c1, c2, c3, c4 = st.columns(4)

    # 1. Churn Rate
    with c1:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">Churn Rate</span>
                <span class="northstar-kpi-symbol sym-red">⌁</span>
            </div>
            <div class="northstar-kpi-value" style="color: #de5442;">{churn_rate:.1%}</div>
            <div class="northstar-kpi-foot">
                <span><b>{churn_count:,}</b> of {total_count:,} customers exited</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Retention Rate
    with c2:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">Retention Rate</span>
                <span class="northstar-kpi-symbol sym-green">↗</span>
            </div>
            <div class="northstar-kpi-value" style="color: #11785f;">{retained_rate:.1%}</div>
            <div class="northstar-kpi-foot">
                <span><b>{retained_count:,}</b> of {total_count:,} customers retained</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Active Customers
    with c3:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">Active Customers</span>
                <span class="northstar-kpi-symbol sym-blue">♧</span>
            </div>
            <div class="northstar-kpi-value">{active_count:,} <span style="font-size:15px;font-weight:600;color:#7c8882;">({active_share:.1%})</span></div>
            <div class="northstar-kpi-foot">
                <span>Active banking operations</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. At-Risk High-Value Customers
    with c4:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">At-Risk High-Value</span>
                <span class="northstar-kpi-symbol sym-amber">⚠</span>
            </div>
            <div class="northstar-kpi-value" style="color: #d5942a;">{at_risk_count:,} <span style="font-size:15px;font-weight:600;color:#7c8882;">({at_risk_share:.1%})</span></div>
            <div class="northstar-kpi-foot">
                <span>Inactive · Balance ≥ {format_euro(balance_cutoff)} or Salary ≥ {format_euro(salary_cutoff)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    return at_risk_df
