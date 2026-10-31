import math
import pandas as pd
import streamlit as st

from src.utils.helpers import assign_recommended_action, format_euro


def render_customers_requiring_attention_page(df: pd.DataFrame):
    """
    Renders the dedicated Customers Requiring Attention page:
    - Heading & Subtitle.
    - Global filter threshold integration (Balance & Salary cutoffs).
    - Qualification logic: IsActiveMember == 0 AND (Balance >= Balance Cutoff OR EstimatedSalary >= Salary Cutoff).
    - 4 Non-overlapping Summary Cards.
    - Interactive Search, Geography filtering, Sorting, Pagination, and Status indicators.
    - Working CSV export: 'Download Prioritized Customers Report (CSV)'.
    """
    # Read active high-value thresholds from session state with standard defaults
    balance_cutoff = float(st.session_state.get("filter_balance_cutoff", int(df["Balance"].quantile(0.75))))
    salary_cutoff = float(st.session_state.get("filter_salary_cutoff", int(df["EstimatedSalary"].quantile(0.75))))

    # Page Heading
    st.markdown("""
    <div class="northstar-page-heading">
        <div>
            <div class="northstar-eyebrow">
                <span class="northstar-eyebrow-mark">✦</span> RISK PRIORITIZATION · PROACTIVE RELATIONSHIP MANAGEMENT
            </div>
            <h1 class="northstar-heading-title">Customers Requiring Attention</h1>
            <p class="northstar-heading-subtitle">
                Identify inactive, high-value customers who may require proactive relationship management.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Threshold Adjustment Expander
    with st.expander("⚙️ **Qualification Threshold Settings**", expanded=False):
        c_th1, c_th2 = st.columns(2)
        with c_th1:
            new_bal_cut = st.number_input(
                "High-Value Balance Threshold (€)",
                min_value=0,
                max_value=int(df["Balance"].max()),
                value=int(balance_cutoff),
                step=5000,
                key="cra_bal_cut",
            )
            st.session_state["filter_balance_cutoff"] = new_bal_cut
            balance_cutoff = float(new_bal_cut)

        with c_th2:
            new_sal_cut = st.number_input(
                "High-Value Salary Threshold (€)",
                min_value=0,
                max_value=int(df["EstimatedSalary"].max()),
                value=int(salary_cutoff),
                step=5000,
                key="cra_sal_cut",
            )
            st.session_state["filter_salary_cutoff"] = new_sal_cut
            salary_cutoff = float(new_sal_cut)

    # 1. Qualification Logic: Inactive (IsActiveMember == 0) and satisfies either financial condition
    inactive_mask = df["IsActiveMember"] == 0
    high_bal_mask = df["Balance"] >= balance_cutoff
    high_sal_mask = df["EstimatedSalary"] >= salary_cutoff

    priority_mask = inactive_mask & (high_bal_mask | high_sal_mask)
    priority_df = df[priority_mask].copy()

    # Metrics for Summary Cards (avoiding double-counting)
    total_priority = len(priority_df)
    high_bal_inactive = int((inactive_mask & high_bal_mask).sum())
    high_sal_inactive = int((inactive_mask & high_sal_mask).sum())
    exited_priority = int((priority_mask & (df["Exited"] == 1)).sum())
    exited_priority_rate = (exited_priority / total_priority) if total_priority > 0 else 0.0

    # 2. Four Summary Cards
    sc1, sc2, sc3, sc4 = st.columns(4)

    with sc1:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">Total Priority Customers</span>
                <span class="northstar-kpi-symbol sym-amber">⚠</span>
            </div>
            <div class="northstar-kpi-value" style="color: #d5942a;">{total_priority:,}</div>
            <div class="northstar-kpi-foot">
                <span>Inactive · Balance ≥ {format_euro(balance_cutoff)} or Salary ≥ {format_euro(salary_cutoff)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">High-Balance Inactive</span>
                <span class="northstar-kpi-symbol sym-blue">€</span>
            </div>
            <div class="northstar-kpi-value">{high_bal_inactive:,}</div>
            <div class="northstar-kpi-foot">
                <span>Inactive accounts with Balance ≥ {format_euro(balance_cutoff)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sc3:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">High-Salary Inactive</span>
                <span class="northstar-kpi-symbol sym-blue">💼</span>
            </div>
            <div class="northstar-kpi-value">{high_sal_inactive:,}</div>
            <div class="northstar-kpi-foot">
                <span>Inactive accounts with Salary ≥ {format_euro(salary_cutoff)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sc4:
        st.markdown(f"""
        <div class="northstar-kpi-card">
            <div class="northstar-kpi-top">
                <span class="northstar-kpi-label">Exited Among Priority</span>
                <span class="northstar-kpi-symbol sym-red">⌁</span>
            </div>
            <div class="northstar-kpi-value" style="color: #de5442;">{exited_priority:,} <span style="font-size:14px;font-weight:600;color:#7c8882;">({exited_priority_rate:.1%})</span></div>
            <div class="northstar-kpi-foot">
                <span>Historical attrition in this priority segment</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. Interactive Table Controls: Search, Geography filtering, Sorting & Page Size
    st.markdown('<div class="northstar-panel">', unsafe_allow_html=True)
    st.markdown('<h3 class="northstar-panel-title">Prioritized Customer Directory</h3>', unsafe_allow_html=True)

    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.5, 1.2, 1.2, 1.0])

    with ctrl_col1:
        search_query = st.text_input(
            "Search by Customer ID",
            placeholder="e.g. 15634602",
            key="cra_search",
        ).strip()

    with ctrl_col2:
        all_geos = ["All", "France", "Germany", "Spain"]
        selected_geo = st.selectbox(
            "Filter Geography",
            options=all_geos,
            index=0,
            key="cra_geo",
        )

    with ctrl_col3:
        sort_choice = st.selectbox(
            "Sort Records By",
            options=[
                "Account Balance (High → Low)",
                "Estimated Salary (High → Low)",
                "Relationship Score (Low → High)",
                "Age (High → Low)",
            ],
            index=0,
            key="cra_sort",
        )

    with ctrl_col4:
        page_size = st.selectbox(
            "Rows Per Page",
            options=[15, 25, 50, 100],
            index=1,
            key="cra_page_size",
        )

    # Filter by search and geography
    filtered_table = priority_df.copy()

    if search_query:
        filtered_table = filtered_table[filtered_table["CustomerId"].astype(str).str.contains(search_query)]

    if selected_geo != "All":
        filtered_table = filtered_table[filtered_table["Geography"] == selected_geo]

    # Apply sorting
    if sort_choice == "Account Balance (High → Low)":
        filtered_table = filtered_table.sort_values(by="Balance", ascending=False)
    elif sort_choice == "Estimated Salary (High → Low)":
        filtered_table = filtered_table.sort_values(by="EstimatedSalary", ascending=False)
    elif sort_choice == "Relationship Score (Low → High)":
        filtered_table = filtered_table.sort_values(by="Relationship Score", ascending=True)
    elif sort_choice == "Age (High → Low)":
        filtered_table = filtered_table.sort_values(by="Age", ascending=False)

    # Assign transparent recommended action
    filtered_table["Recommended Action"] = filtered_table.apply(
        lambda row: assign_recommended_action(row, balance_cutoff, salary_cutoff),
        axis=1
    )

    # Map required columns for presentation
    cols_map = {
        "CustomerId": "CustomerId",
        "Geography": "Geography",
        "Age": "Age",
        "Balance": "Balance",
        "EstimatedSalary": "EstimatedSalary",
        "NumOfProducts": "NumOfProducts",
        "Engagement": "Engagement Status",
        "Relationship Score": "Relationship Score",
        "Relationship Tier": "Relationship Tier",
        "Churn Status": "Exit Status",
        "Recommended Action": "Recommended Action",
    }

    display_df = filtered_table[[c for c in cols_map.keys() if c in filtered_table]].rename(columns=cols_map)

    # Pagination controls
    total_records = len(display_df)
    total_pages = max(1, math.ceil(total_records / page_size))
    current_page_idx = st.session_state.get("cra_current_page_idx", 1)
    if current_page_idx > total_pages:
        current_page_idx = total_pages

    st.markdown(
        f"<div style='font-size:11.5px; color:#7c8882; margin: 4px 0 10px 0;'>"
        f"Displaying <b>{total_records:,}</b> matching customer records · Page {current_page_idx} of {total_pages}"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Slice for current page
    start_idx = (current_page_idx - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    paged_df = display_df.iloc[start_idx:end_idx]

    # Render table
    st.dataframe(
        paged_df,
        hide_index=True,
        use_container_width=True,
        height=380,
        column_config={
            "CustomerId": st.column_config.TextColumn("Customer ID"),
            "Geography": st.column_config.TextColumn("Geography"),
            "Age": st.column_config.NumberColumn("Age", format="%d"),
            "Balance": st.column_config.NumberColumn("Account Balance", format="€%.2f"),
            "EstimatedSalary": st.column_config.NumberColumn("Estimated Salary", format="€%.2f"),
            "NumOfProducts": st.column_config.NumberColumn("Products", format="%d"),
            "Engagement Status": st.column_config.TextColumn("Engagement"),
            "Relationship Score": st.column_config.ProgressColumn(
                "Relationship Score", min_value=0, max_value=100, format="%d"
            ),
            "Relationship Tier": st.column_config.TextColumn("Tier"),
            "Exit Status": st.column_config.TextColumn("Exit Status"),
            "Recommended Action": st.column_config.TextColumn("Recommended Action"),
        }
    )

    # Pagination navigation buttons
    pag_col1, pag_col2, pag_col3, pag_col4 = st.columns([1, 1, 3, 2])
    with pag_col1:
        if st.button("◀ Previous", disabled=(current_page_idx <= 1), use_container_width=True):
            st.session_state["cra_current_page_idx"] = max(1, current_page_idx - 1)
            st.rerun()

    with pag_col2:
        if st.button("Next ▶", disabled=(current_page_idx >= total_pages), use_container_width=True):
            st.session_state["cra_current_page_idx"] = min(total_pages, current_page_idx + 1)
            st.rerun()

    with pag_col4:
        # Full Export button for currently filtered records
        csv_bytes = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="↧ Download Prioritized Customers Report (CSV)",
            data=csv_bytes,
            file_name="prioritized_customers_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
