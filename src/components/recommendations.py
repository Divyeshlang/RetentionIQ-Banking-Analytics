import html
import textwrap
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.utils.helpers import format_euro


def _render_html(raw_html: str):
    """
    Renders raw HTML safely by stripping common leading indentation (dedenting)
    and ensuring no 4-space markdown indent is interpreted as a code-block.
    """
    cleaned = textwrap.dedent(raw_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_strategic_recommendations_page(df: pd.DataFrame):
    """
    Renders the Strategic Portfolio Recommendations page:
    - Section 1: Engagement-Based Retention
    - Section 2: Product Adoption Strategy
    - Section 3: High-Value Customer Protection
    - Section 4: Regional Retention Strategy
    - Section 5: Executive Action Plan
    """
    # Dynamic calculations from verified dataset
    total_customers = len(df)
    
    # 1. Engagement metrics
    act_churn = df[df["IsActiveMember"] == 1]["Exited"].mean()
    inact_churn = df[df["IsActiveMember"] == 0]["Exited"].mean()
    inact_count = int((df["IsActiveMember"] == 0).sum())
    act_count = int((df["IsActiveMember"] == 1).sum())
    eng_delta = (inact_churn - act_churn) * 100

    # 2. Product metrics
    prod_summary = df.groupby("NumOfProducts").agg(
        n=("CustomerId", "count"),
        churn=("Exited", "mean")
    ).reset_index()

    # 3. High-Value metrics
    bal_cutoff = float(st.session_state.get("filter_balance_cutoff", int(df["Balance"].quantile(0.75))))
    sal_cutoff = float(st.session_state.get("filter_salary_cutoff", int(df["EstimatedSalary"].quantile(0.75))))
    
    inact_mask = df["IsActiveMember"] == 0
    high_bal_inact = int((inact_mask & (df["Balance"] >= bal_cutoff)).sum())
    high_sal_inact = int((inact_mask & (df["EstimatedSalary"] >= sal_cutoff)).sum())
    total_priority = int((inact_mask & ((df["Balance"] >= bal_cutoff) | (df["EstimatedSalary"] >= sal_cutoff))).sum())

    # 4. Regional metrics
    geo_summary = df.groupby("Geography").agg(
        n=("CustomerId", "count"),
        churn=("Exited", "mean"),
        avg_bal=("Balance", "mean")
    ).reset_index()

    # Header
    _render_html("""
<div class="northstar-page-heading">
<div>
<div class="northstar-eyebrow">
<span class="northstar-eyebrow-mark">✦</span> STRATEGIC ADVISORY · DATA-BACKED PLAYBOOK
</div>
<h1 class="northstar-heading-title">Strategic Portfolio Recommendations</h1>
<p class="northstar-heading-subtitle">
Data-driven strategies to improve customer engagement, strengthen relationships, and reduce customer churn.
</p>
</div>
</div>
""")

    # Context alert
    _render_html("""
<div class="northstar-takeaway" style="margin-bottom:18px; border-left-color:#526eeb; background:#f4f7fd; color:#182b49;">
<b>Executive Advisory Context:</b> All recommendations are formulated from empirical observations within the 
verified 10,000-customer European banking dataset. Observed historical correlations highlight high-leverage intervention opportunities, 
though individual customer behavior should be confirmed through controlled pilot testing.
</div>
""")

    # -------------------------------------------------------------
    # SECTION 1 & 2: ENGAGEMENT & PRODUCT ADOPTION
    # -------------------------------------------------------------
    r1_col1, r1_col2 = st.columns(2)

    with r1_col1:
        # 1. Engagement-Based Retention Card
        _render_html(f"""
<div class="northstar-panel">
<h3 class="northstar-panel-title">1. Engagement-Based Retention</h3>
<p class="northstar-panel-question">Addressing the single largest churn determinant in the portfolio</p>

<div style="display:flex; justify-content:space-between; margin:14px 0 10px 0; background:#f6f8f5; padding:12px; border-radius:6px;">
<div>
<span style="font-size:10px; color:#7c8882; font-weight:600;">ACTIVE CHURN</span>
<div style="font-size:20px; font-weight:800; color:#11785f;">{act_churn:.1%}</div>
<span style="font-size:9.5px; color:#7c8882;">{act_count:,} accounts</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:16px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">INACTIVE CHURN</span>
<div style="font-size:20px; font-weight:800; color:#de5442;">{inact_churn:.1%}</div>
<span style="font-size:9.5px; color:#7c8882;">{inact_count:,} accounts</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:16px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">OBSERVED SPREAD</span>
<div style="font-size:20px; font-weight:800; color:#172521;">+{eng_delta:.1f}%</div>
<span style="font-size:9.5px; color:#7c8882;">Elevated attrition</span>
</div>
</div>

<p style="font-size:11.5px; color:#172521; line-height:1.5; margin:0 0 10px 0;">
<b>Key Analytical Finding:</b> Inactive customers exhibit an observed churn rate nearly double that of active members ({inact_churn:.1%} vs {act_churn:.1%}). 
Dormancy strongly correlates with account closure.
</p>
</div>
""")

        # Engagement Comparison Chart
        fig_eng = go.Figure()
        fig_eng.add_trace(go.Bar(
            x=["Active", "Inactive"],
            y=[act_churn * 100, inact_churn * 100],
            text=[f"<b>{act_churn:.1%}</b>", f"<b>{inact_churn:.1%}</b>"],
            textposition="outside",
            marker_color=["#11785f", "#de5442"],
            width=0.45,
            hovertemplate="<b>%{x}</b><br>Observed Churn: %{y:.1f}%<extra></extra>"
        ))
        fig_eng.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            xaxis=dict(title="", tickfont=dict(size=12, color="#172521", family="DM Sans")),
            yaxis=dict(
                title="Observed Churn Rate (%)",
                ticksuffix="%",
                gridcolor="#f2f5f2",
                range=[0, max(35, inact_churn * 135)],
                tickfont=dict(size=10, color="#7c8983")
            ),
            showlegend=False
        )
        st.plotly_chart(fig_eng, use_container_width=True)

    with r1_col2:
        prod2_churn = prod_summary[prod_summary["NumOfProducts"] == 2]["churn"].values[0]
        prod1_churn = prod_summary[prod_summary["NumOfProducts"] == 1]["churn"].values[0]

        # 2. Product Adoption Strategy Card
        _render_html(f"""
<div class="northstar-panel">
<h3 class="northstar-panel-title">2. Product Adoption Strategy</h3>
<p class="northstar-panel-question">Promoting relationship depth without creating operational fatigue</p>

<div style="display:flex; justify-content:space-between; margin:14px 0 10px 0; background:#f6f8f5; padding:12px; border-radius:6px;">
<div>
<span style="font-size:10px; color:#7c8882; font-weight:600;">1 PRODUCT</span>
<div style="font-size:20px; font-weight:800; color:#de5442;">{prod1_churn:.1%}</div>
<span style="font-size:9.5px; color:#7c8882;">5,084 accounts</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:12px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">2 PRODUCTS</span>
<div style="font-size:20px; font-weight:800; color:#11785f;">{prod2_churn:.1%}</div>
<span style="font-size:9.5px; color:#7c8882;">4,590 accounts</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:12px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">3 PRODUCTS</span>
<div style="font-size:20px; font-weight:800; color:#de5442;">82.7%</div>
<span style="font-size:9.5px; color:#7c8882;">266 accounts</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:12px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">4 PRODUCTS</span>
<div style="font-size:20px; font-weight:800; color:#de5442;">100%</div>
<span style="font-size:9.5px; color:#7c8882;">60 accounts*</span>
</div>
</div>

<p style="font-size:11.5px; color:#172521; line-height:1.5; margin:0 0 10px 0;">
<b>Key Analytical Finding:</b> Customers with <b>2 products</b> achieve the lowest observed attrition rate (<b>{prod2_churn:.1%}</b>). 
Holding 3 or 4 products exhibits extreme attrition (>80%). Product quantity does not linearly increase loyalty.
</p>
</div>
""")

        # Product Adoption Chart
        fig_prod = go.Figure()
        prod_colors = ["#de5442" if p != 2 else "#11785f" for p in prod_summary["NumOfProducts"]]
        fig_prod.add_trace(go.Bar(
            x=[f"{int(p)} Prod" for p in prod_summary["NumOfProducts"]],
            y=prod_summary["churn"] * 100,
            text=[f"<b>{c:.1%}</b>" for c in prod_summary["churn"]],
            textposition="outside",
            marker_color=prod_colors,
            width=0.5,
            hovertemplate="<b>%{x}</b><br>Observed Churn: %{y:.1f}%<extra></extra>"
        ))
        fig_prod.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            xaxis=dict(title="", tickfont=dict(size=12, color="#172521", family="DM Sans")),
            yaxis=dict(
                title="Observed Churn Rate (%)",
                ticksuffix="%",
                gridcolor="#f2f5f2",
                range=[0, 115],
                tickfont=dict(size=10, color="#7c8983")
            ),
            showlegend=False
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    # -------------------------------------------------------------
    # SECTION 3: HIGH-VALUE PROTECTION
    # -------------------------------------------------------------
    _render_html(f"""
<div class="northstar-panel">
<h3 class="northstar-panel-title">3. High-Value Customer Protection</h3>
<p class="northstar-panel-question">Preserving wealth and capital liquidity in high-equity inactive accounts</p>

<div style="display:flex; justify-content:space-between; margin:14px 0 10px 0; background:#f6f8f5; padding:12px; border-radius:6px;">
<div>
<span style="font-size:10px; color:#7c8882; font-weight:600;">AT-RISK HIGH-VALUE</span>
<div style="font-size:20px; font-weight:800; color:#d5942a;">{total_priority:,}</div>
<span style="font-size:9.5px; color:#7c8882;">21.5% of portfolio</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:14px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">HIGH-BALANCE INACT</span>
<div style="font-size:20px; font-weight:800; color:#172521;">{high_bal_inact:,}</div>
<span style="font-size:9.5px; color:#7c8882;">≥ {format_euro(bal_cutoff)}</span>
</div>
<div style="border-left:1px solid #e9ede8; padding-left:14px;">
<span style="font-size:10px; color:#7c8882; font-weight:600;">HIGH-SALARY INACT</span>
<div style="font-size:20px; font-weight:800; color:#172521;">{high_sal_inact:,}</div>
<span style="font-size:9.5px; color:#7c8882;">≥ {format_euro(sal_cutoff)}</span>
</div>
</div>

<p style="font-size:11.5px; color:#172521; line-height:1.5; margin:0 0 10px 0;">
<b>Key Analytical Finding:</b> Exactly <b>{total_priority:,} customers</b> hold substantial liquidity or earning power but maintain zero active banking relationship, representing substantial balance sheet flight risk.
</p>
</div>
""")

    # -------------------------------------------------------------
    # SECTION 4: REGIONAL RETENTION STRATEGY
    # -------------------------------------------------------------
    ger_churn = geo_summary[geo_summary["Geography"] == "Germany"]["churn"].values[0]
    fra_churn = geo_summary[geo_summary["Geography"] == "France"]["churn"].values[0]
    spa_churn = geo_summary[geo_summary["Geography"] == "Spain"]["churn"].values[0]
    ger_bal = geo_summary[geo_summary["Geography"] == "Germany"]["avg_bal"].values[0]
    fra_bal = geo_summary[geo_summary["Geography"] == "France"]["avg_bal"].values[0]

    _render_html(f"""
<div class="northstar-panel">
<h3 class="northstar-panel-title">4. Regional Retention Strategy</h3>
<p class="northstar-panel-question">Empirical market differences across France, Germany, and Spain</p>

<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin:14px 0;">
<div style="background:#fdf5f4; border:1px solid #f9deda; border-radius:8px; padding:12px 16px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<b style="font-size:13px; color:#8c2e22;">🇩🇪 Germany</b>
<span style="font-size:10px; background:#fef0ed; color:#de5442; padding:2px 6px; border-radius:4px; font-weight:700;">HIGH ATTRITION</span>
</div>
<div style="font-size:24px; font-weight:800; color:#de5442; margin-top:4px;">{ger_churn:.1%}</div>
<p style="font-size:10.5px; color:#7c8882; margin:2px 0 6px 0;">2,509 customers · Avg balance: {format_euro(ger_bal)}</p>
<p style="font-size:11px; color:#172521; line-height:1.4; margin:0;">
<b>Strategic Directive:</b> German accounts have double the churn rate of France and Spain despite maintaining the highest average balances (€119k). Immediate competitive audit and interest yield restructuring required.
</p>
</div>

<div style="background:#f6f8f5; border:1px solid #e9ede8; border-radius:8px; padding:12px 16px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<b style="font-size:13px; color:#172521;">🇫🇷 France</b>
<span style="font-size:10px; background:#eaf6ef; color:#11785f; padding:2px 6px; border-radius:4px; font-weight:700;">STABLE MARKET</span>
</div>
<div style="font-size:24px; font-weight:800; color:#11785f; margin-top:4px;">{fra_churn:.1%}</div>
<p style="font-size:10.5px; color:#7c8882; margin:2px 0 6px 0;">5,014 customers · Avg balance: {format_euro(fra_bal)}</p>
<p style="font-size:11px; color:#172521; line-height:1.4; margin:0;">
<b>Strategic Directive:</b> Largest volume base (50% of portfolio) with low churn. Focus on selective 2-product cross-selling to deepen deposit volume while preserving baseline satisfaction.
</p>
</div>

<div style="background:#f6f8f5; border:1px solid #e9ede8; border-radius:8px; padding:12px 16px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<b style="font-size:13px; color:#172521;">🇪🇸 Spain</b>
<span style="font-size:10px; background:#eaf6ef; color:#11785f; padding:2px 6px; border-radius:4px; font-weight:700;">STABLE MARKET</span>
</div>
<div style="font-size:24px; font-weight:800; color:#11785f; margin-top:4px;">{spa_churn:.1%}</div>
<p style="font-size:10.5px; color:#7c8882; margin:2px 0 6px 0;">2,477 customers · Avg balance: €61,818</p>
<p style="font-size:11px; color:#172521; line-height:1.4; margin:0;">
<b>Strategic Directive:</b> Consistent retention baseline similar to France. Replicate successful French engagement mechanics to grow Spanish active membership beyond current levels.
</p>
</div>
</div>
</div>
""")

    # -------------------------------------------------------------
    # SECTION 5: EXECUTIVE ACTION PLAN
    # -------------------------------------------------------------
    action_plan_data = [
        {
            "Priority": "High",
            "Business Challenge": "Inactive premium customers",
            "Recommended Action": "Personalized outreach & wealth check-ins",
            "Expected Business Benefit": "Improve engagement & prevent liquidity flight",
        },
        {
            "Priority": "High",
            "Business Challenge": "High German market churn (32.4%)",
            "Recommended Action": "Targeted competitive rate audit & regional outreach",
            "Expected Business Benefit": "Improve retention across high-balance German accounts",
        },
        {
            "Priority": "Medium",
            "Business Challenge": "Low product adoption (Single-product accounts)",
            "Recommended Action": "Relevant dual-product bundling (Checking + Savings)",
            "Expected Business Benefit": "Increase relationship depth to optimal 7.6% churn",
        },
    ]

    action_df = pd.DataFrame(action_plan_data)

    def render_priority_badge(val):
        color = "#de5442" if val == "High" else "#d5942a"
        bg = "#fef0ed" if val == "High" else "#fff8ec"
        safe_val = html.escape(str(val))
        return f'<span style="background:{bg}; color:{color}; font-weight:700; font-size:10px; padding:3px 8px; border-radius:4px; display:inline-block;">{safe_val}</span>'

    table_rows = "".join([
        f"""
<tr style="border-bottom:1px solid #eef2ed; font-size:11.5px;">
<td style="padding:10px 14px; white-space:nowrap;">{render_priority_badge(r['Priority'])}</td>
<td style="padding:10px 14px; font-weight:600; color:#172521;">{html.escape(str(r['Business Challenge']))}</td>
<td style="padding:10px 14px; color:#3a4640;">{html.escape(str(r['Recommended Action']))}</td>
<td style="padding:10px 14px; color:#11785f; font-weight:600;">{html.escape(str(r['Expected Business Benefit']))}</td>
</tr>
"""
        for _, r in action_df.iterrows()
    ])

    _render_html(f"""
<div class="northstar-panel">
<h3 class="northstar-panel-title">5. Executive Action Plan</h3>
<p class="northstar-panel-question" style="margin-bottom:14px;">Structured operational roadmap for retail banking management</p>

<div style="overflow-x:auto; border:1px solid #e9ede8; border-radius:8px; background:#ffffff;">
<table style="width:100%; border-collapse:collapse; text-align:left; font-family:'DM Sans', sans-serif;">
<thead>
<tr style="background:#f6f8f5; border-bottom:1px solid #e9ede8; font-size:10.5px; color:#7c8882; text-transform:uppercase; letter-spacing:0.4px;">
<th style="padding:10px 14px; font-weight:700;">Priority</th>
<th style="padding:10px 14px; font-weight:700;">Business Challenge</th>
<th style="padding:10px 14px; font-weight:700;">Recommended Action</th>
<th style="padding:10px 14px; font-weight:700;">Expected Business Benefit</th>
</tr>
</thead>
<tbody>
{table_rows}
</tbody>
</table>
</div>
</div>
""")
