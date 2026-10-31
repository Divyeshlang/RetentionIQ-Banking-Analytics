import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import PALETTE


def render_engagement_chart(view: pd.DataFrame):
    """Section 3: Customer Engagement vs Churn in Northstar styling"""
    st.markdown("""
    <div class="northstar-panel-head">
        <div>
            <h3 class="northstar-panel-title">Customer Engagement vs Churn</h3>
            <p class="northstar-panel-question">Business question: Are inactive customers more likely to leave the bank?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    eng_stats = (
        view.groupby("Engagement", observed=True)
        .agg(Customers=("CustomerId", "size"), ChurnRate=("Exited", "mean"), ExitedCount=("Exited", "sum"))
        .reindex(["Active", "Inactive"])
        .dropna()
        .reset_index()
    )

    if not eng_stats.empty:
        fig = go.Figure()
        # Northstar colors: Deep Green for Active, Warm Red for Inactive
        colors_eng = ["#11785f" if e == "Active" else "#de5442" for e in eng_stats["Engagement"]]
        
        bar_text = [
            f"<b>{row['ChurnRate']:.1%}</b><br><span style='font-size:10px;color:#7c8983;'>({row['Customers']:,} cust)</span>"
            for _, row in eng_stats.iterrows()
        ]
        
        fig.add_trace(go.Bar(
            x=eng_stats["Engagement"],
            y=eng_stats["ChurnRate"] * 100,
            text=bar_text,
            textposition="outside",
            marker_color=colors_eng,
            marker_line=dict(color="#e9ede8", width=1),
            width=0.42,
            hovertemplate="<b>%{x} Customers</b><br>Observed Churn: %{y:.1f}%<extra></extra>",
        ))

        max_churn_eng = eng_stats["ChurnRate"].max() * 100
        fig.update_layout(
            height=300,
            margin=dict(l=15, r=15, t=25, b=15),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            xaxis=dict(title="", tickfont=dict(size=12, color="#172521", family="DM Sans")),
            yaxis=dict(
                title="Observed Churn Rate (%)",
                ticksuffix="%",
                gridcolor="#f2f5f2",
                range=[0, max(32, max_churn_eng * 1.35)],
                tickfont=dict(size=10, color="#7c8983"),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        active_row = eng_stats[eng_stats["Engagement"] == "Active"]
        inactive_row = eng_stats[eng_stats["Engagement"] == "Inactive"]

        if not active_row.empty and not inactive_row.empty:
            act_churn = active_row["ChurnRate"].values[0]
            inact_churn = inactive_row["ChurnRate"].values[0]
            diff = (inact_churn - act_churn) * 100
            takeaway = (
                f"<b>Key Insight:</b> Inactive customers experience an observed churn rate of <b>{inact_churn:.1%}</b> vs "
                f"<b>{act_churn:.1%}</b> for active customers (+{diff:.1f} percentage points higher). Priority should focus on dormant account activation."
            )
        elif not inactive_row.empty:
            takeaway = f"<b>Key Insight:</b> Current filtered subset contains only inactive accounts with <b>{inactive_row['ChurnRate'].values[0]:.1%}</b> observed churn."
        else:
            takeaway = f"<b>Key Insight:</b> Current filtered subset contains only active accounts with <b>{active_row['ChurnRate'].values[0]:.1%}</b> observed churn."

        st.markdown(f'<div class="northstar-takeaway">{takeaway}</div>', unsafe_allow_html=True)
    else:
        st.info("Insufficient engagement data for the current filter settings.")


def render_product_chart(view: pd.DataFrame):
    """Section 4: Product Usage vs Churn in Northstar styling"""
    st.markdown("""
    <div class="northstar-panel-head">
        <div>
            <h3 class="northstar-panel-title">Product Usage vs Churn</h3>
            <p class="northstar-panel-question">Business question: Does product adoption relate to customer retention?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    prod_stats = (
        view.groupby("NumOfProducts", observed=True)
        .agg(Customers=("CustomerId", "size"), ChurnRate=("Exited", "mean"), ExitedCount=("Exited", "sum"))
        .reset_index()
    )

    if not prod_stats.empty:
        reliable_groups = prod_stats[prod_stats["Customers"] >= 30]
        if not reliable_groups.empty:
            best_prod = reliable_groups.sort_values("ChurnRate").iloc[0]["NumOfProducts"]
        else:
            best_prod = prod_stats.sort_values("ChurnRate").iloc[0]["NumOfProducts"]

        bar_colors = [
            "#11785f" if p == best_prod else ("#de5442" if r >= 0.5 else "#8bb9ee")
            for p, r in zip(prod_stats["NumOfProducts"], prod_stats["ChurnRate"])
        ]

        prod_text = [
            f"<b>{row['ChurnRate']:.1%}</b><br><span style='font-size:10px;color:#7c8983;'>({row['Customers']:,} cust)</span>"
            for _, row in prod_stats.iterrows()
        ]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"{int(p)} Product{'s' if p>1 else ''}" for p in prod_stats["NumOfProducts"]],
            y=prod_stats["ChurnRate"] * 100,
            text=prod_text,
            textposition="outside",
            marker_color=bar_colors,
            marker_line=dict(color="#e9ede8", width=1),
            width=0.48,
            hovertemplate="<b>%{x}</b><br>Observed Churn: %{y:.1f}%<extra></extra>",
        ))

        max_churn_prod = prod_stats["ChurnRate"].max() * 100
        fig.update_layout(
            height=300,
            margin=dict(l=15, r=15, t=25, b=15),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            xaxis=dict(title="", tickfont=dict(size=11, color="#172521", family="DM Sans")),
            yaxis=dict(
                title="Observed Churn Rate (%)",
                ticksuffix="%",
                gridcolor="#f2f5f2",
                range=[0, max(32, max_churn_prod * 1.35)],
                tickfont=dict(size=10, color="#7c8983"),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        best_row = prod_stats[prod_stats["NumOfProducts"] == best_prod].iloc[0]
        has_small_sample = (prod_stats["Customers"] < 100).any()
        small_sample_prods = prod_stats[prod_stats["Customers"] < 100]["NumOfProducts"].tolist()

        takeaway = (
            f"<b>Key Insight:</b> Customers with <b>{int(best_prod)} products</b> achieve the lowest observed churn rate at "
            f"<b>{best_row['ChurnRate']:.1%}</b> (highlighted in Northstar green). "
            f"Account depth does not linearly increase retention: customers with 3 or 4 products exhibit heavy attrition."
        )

        if has_small_sample:
            small_notes = ", ".join([f"{int(p)} products (n={int(prod_stats[prod_stats['NumOfProducts']==p]['Customers'].iloc[0])})" for p in small_sample_prods])
            warning_html = f"<br>⚠️ <em>Sample size advisory: Customer counts for {small_notes} are small; their high rates should be interpreted with caution.</em>"
            st.markdown(f'<div class="northstar-takeaway northstar-takeaway-alert">{takeaway}{warning_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="northstar-takeaway">{takeaway}</div>', unsafe_allow_html=True)
    else:
        st.info("Insufficient product data for the current filter settings.")


def render_relationship_tier_section(view: pd.DataFrame):
    """Section 5: Customer Relationship Strength in Northstar horizontal layout"""
    st.markdown("""
    <div class="northstar-panel-head">
        <div>
            <h3 class="northstar-panel-title">Customer Relationship Strength</h3>
            <p class="northstar-panel-question">Business question: Which relationship groups require the most attention?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    rel_stats = (
        view.groupby("Relationship Tier", observed=True)
        .agg(
            Customers=("CustomerId", "size"),
            ChurnRate=("Exited", "mean"),
            ExitedCount=("Exited", "sum"),
            AvgScore=("Relationship Score", "mean"),
        )
        .reindex(["Fragile", "Developing", "Strong"])
        .dropna()
        .reset_index()
    )

    if not rel_stats.empty:
        rel_stats["PctShare"] = rel_stats["Customers"] / rel_stats["Customers"].sum()
        risk_order = {"Fragile": 0, "Developing": 1, "Strong": 2}
        rel_stats["Order"] = rel_stats["Relationship Tier"].map(risk_order)
        rel_stats = rel_stats.sort_values("Order").reset_index(drop=True)

        c3_chart, c3_table = st.columns([1.5, 1])

        with c3_chart:
            tier_colors = {
                "Fragile": "#de5442",
                "Developing": "#e4a43d",
                "Strong": "#11785f",
            }
            
            fig = go.Figure()
            plot_df = rel_stats.iloc[::-1]

            fig.add_trace(go.Bar(
                y=plot_df["Relationship Tier"],
                x=plot_df["Customers"],
                orientation="h",
                text=[f"<b>{c:,}</b> ({p:.1%})" for c, p in zip(plot_df["Customers"], plot_df["PctShare"])],
                textposition="outside",
                marker_color=[tier_colors.get(t, "#526eeb") for t in plot_df["Relationship Tier"]],
                marker_line=dict(color="#e9ede8", width=1),
                hovertemplate="<b>%{y} Relationship Tier</b><br>Volume: %{x:,} accounts<extra></extra>",
            ))

            fig.update_layout(
                height=250,
                margin=dict(l=10, r=40, t=10, b=15),
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff",
                xaxis=dict(
                    title="Number of Customers",
                    gridcolor="#f2f5f2",
                    tickfont=dict(size=10, color="#7c8983"),
                    range=[0, rel_stats["Customers"].max() * 1.32],
                ),
                yaxis=dict(title="", tickfont=dict(size=12, color="#172521", family="DM Sans")),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        with c3_table:
            summary_table = rel_stats[["Relationship Tier", "Customers", "PctShare", "ChurnRate", "AvgScore"]].copy()
            summary_table = summary_table.rename(columns={
                "Relationship Tier": "Relationship Tier",
                "Customers": "Customers",
                "PctShare": "Portfolio %",
                "ChurnRate": "Observed Churn",
                "AvgScore": "Score Index",
            })
            
            st.dataframe(
                summary_table,
                hide_index=True,
                use_container_width=True,
                height=250,
                column_config={
                    "Relationship Tier": st.column_config.TextColumn(help="Sorted highest risk to lowest risk"),
                    "Customers": st.column_config.NumberColumn(format="%d"),
                    "Portfolio %": st.column_config.NumberColumn(format="%.1f%%"),
                    "Observed Churn": st.column_config.NumberColumn(format="%.1%"),
                    "Score Index": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d / 100"),
                },
            )

        fragile_data = rel_stats[rel_stats["Relationship Tier"] == "Fragile"]
        strong_data = rel_stats[rel_stats["Relationship Tier"] == "Strong"]
        
        if not fragile_data.empty:
            f_share = fragile_data["PctShare"].values[0]
            f_churn = fragile_data["ChurnRate"].values[0]
            takeaway = (
                f"<b>Key Insight:</b> <b>Fragile relationships</b> account for <b>{f_share:.1%}</b> of the portfolio "
                f"({fragile_data['Customers'].values[0]:,} accounts) and show the highest observed churn at <b>{f_churn:.1%}</b>."
            )
            if not strong_data.empty:
                s_churn = strong_data["ChurnRate"].values[0]
                takeaway += f" In contrast, <b>Strong relationships</b> demonstrate stability with an observed churn rate of only <b>{s_churn:.1%}</b>."
        else:
            takeaway = "<b>Key Insight:</b> Current filter contains no Fragile accounts. Monitor developing accounts to prevent risk tier downgrades."

        st.markdown(f'<div class="northstar-takeaway">{takeaway}</div>', unsafe_allow_html=True)

        with st.expander("ℹ️ How Relationship Strength Scoring is Calculated", expanded=False):
            st.markdown("""
            **Scoring Methodology (0–100 points):**
            - **Activity Component (60 points):** Awarded if `IsActiveMember = 1` (actively engaging with banking services).
            - **Product Breadth Component (up to 40 points):** Linearly scaled from 1 product (0 points) to 4 products (40 points).
            - **Relationship Tiers:**
              - 🔴 **Fragile (0–39 points):** High-risk accounts, typically inactive with minimal product breadth.
              - 🟡 **Developing (40–69 points):** Moderate engagement or single-product active users.
              - 🟢 **Strong (70–100 points):** Active accounts holding multiple financial products.
            """)
    else:
        st.info("Insufficient relationship tier data for the current filter settings.")
