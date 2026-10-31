import pandas as pd
import streamlit as st

def render_disclosures(df: pd.DataFrame, audit: dict, data_file_name: str):
    """Renders research insights, methodology disclosures, and data profiling expanders in Northstar style."""
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    with st.expander("📋 Executive Readout & Strategic Action Plan", expanded=False):
        st.markdown("""
        ### Strategic Portfolio Recommendations
        1. **Prioritize High-Balance Inactive Outreaches:** Contact inactive customers with balances exceeding the threshold through dedicated relationship managers rather than generic marketing blasts.
        2. **Focus Cross-Sell on 2-Product Bundling:** Data demonstrates customers with 2 products achieve the lowest observed attrition rate (7.6%). Aim to transition single-product depositors into dual-product accounts.
        3. **Avoid Over-Saturation Without Usage:** Churn is elevated for accounts holding 3 or 4 products. Do not push product quantity onto customers without active ongoing transaction engagement.
        4. **Regional Optimization:** Tailor re-engagement workflows according to local branch characteristics.
        """)

    with st.expander("🔬 Data Provenance, Governance & Methodological Disclosures"):
        st.markdown(f"""
        - **Dataset Source:** `{data_file_name}` containing **{audit['source_rows']:,}** records (**{len(df):,}** validated unique customers).
        - **Data Cleaning & Auditing:** Deduplicated by unique `CustomerId`. Records missing outcome or ID were verified; missing continuous features use median imputation; binary flags use the mode.
        - **Scope of Data:** Historical European retail banking snapshot. Does not contain time-series transactions, web logs, or explicit customer service interactions.
        - **Descriptive Analytics Notice:** All metrics reflect observed historical patterns in this snapshot and do not claim to forecast individual customer actions without a validated statistical predictive model.
        """)
