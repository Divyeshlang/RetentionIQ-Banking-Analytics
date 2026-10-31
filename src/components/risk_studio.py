import html
import textwrap
import streamlit as st
import pandas as pd
from src.models.predictor import load_model_pipeline, predict_churn


def _render_html(raw_html: str):
    """Renders raw HTML safely by stripping leading indents to prevent markdown code block formatting."""
    cleaned = textwrap.dedent(raw_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def get_risk_classification(prob: float) -> tuple[str, str, str, str]:
    """
    Returns (category, color_hex, badge_bg, badge_border):
    - Low: < 25%
    - Medium: 25% - 50%
    - High: >= 50%
    """
    if prob >= 0.50:
        return "High Risk", "#de5442", "#fef0ed", "#f9deda"
    elif prob >= 0.25:
        return "Medium Risk", "#d5942a", "#fff5e7", "#fbe8cd"
    else:
        return "Low Risk", "#11785f", "#eaf6ef", "#c8ebd9"


def get_recommended_action(prob: float, is_active: bool, balance: float, products: int) -> str:
    """Provides a tailored retention action based on risk score and customer parameters."""
    if prob >= 0.50:
        if not is_active and balance > 100000:
            return "Immediate proactive outreach by senior relationship manager; arrange personalized retention incentives."
        elif products >= 3:
            return "Product consolidation review; assess service friction across complex multiple product accounts."
        else:
            return "High-priority re-engagement intervention; offer specialized fee waivers or relationship bonus."
    elif prob >= 0.25:
        if not is_active:
            return "Automated digital re-engagement sequence; highlight digital banking features and alerts."
        elif products == 1:
            return "Cross-sell advisory; introduce secondary deposit or credit product to deepen relationship."
        else:
            return "Periodic satisfaction survey and routine relationship health check."
    else:
        return "Standard relationship nurturing; account is in good standing with high retention likelihood."


def render_risk_studio_page(df: pd.DataFrame):
    """Renders the Risk Studio Page."""
    model_data, is_online = load_model_pipeline()

    # Top Status indicator
    status_badge = (
        '<span style="background:#eaf6ef; color:#11785f; padding:4px 10px; border-radius:14px; font-size:11px; font-weight:600; display:inline-flex; align-items:center; gap:5px;"><i style="width:6px;height:6px;border-radius:50%;background:#11785f;display:inline-block;"></i> Model Online (Logistic Regression AUC: 0.77)</span>'
        if is_online else
        '<span style="background:#fef0ed; color:#de5442; padding:4px 10px; border-radius:14px; font-size:11px; font-weight:600; display:inline-flex; align-items:center; gap:5px;"><i style="width:6px;height:6px;border-radius:50%;background:#de5442;display:inline-block;"></i> Rule-Based Engine (Model Offline)</span>'
    )

    _render_html(f"""
<div class="northstar-page-heading">
<div>
<div class="northstar-eyebrow">
<span class="northstar-eyebrow-mark">✦</span> PREDICTIVE INTELLIGENCE · INDIVIDUAL PROFILE SCORING
</div>
<h1 class="northstar-heading-title">Risk Studio</h1>
<p class="northstar-heading-subtitle">
Estimate customer churn likelihood using financial, demographic, and engagement characteristics.
</p>
</div>
<div>
{status_badge}
</div>
</div>
""")

    # Initialize default values in session state
    if "rs_credit_score" not in st.session_state:
        st.session_state["rs_credit_score"] = 650
        st.session_state["rs_balance"] = 76000.0
        st.session_state["rs_salary"] = 100000.0
        st.session_state["rs_products"] = 2
        st.session_state["rs_age"] = 38
        st.session_state["rs_tenure"] = 5
        st.session_state["rs_country"] = "France"
        st.session_state["rs_gender"] = "Female"
        st.session_state["rs_has_card"] = "Yes"
        st.session_state["rs_active"] = "Yes"

    # Form card
    st.markdown('<div class="northstar-panel">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-family:Manrope,sans-serif;font-size:15px;font-weight:700;margin:0 0 16px 0;color:#172521;">Customer Profile Parameters</h3>', unsafe_allow_html=True)

    with st.form("risk_studio_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<p style="font-size:11px;font-weight:700;color:#7c8882;text-transform:uppercase;margin-bottom:8px;letter-spacing:0.5px;">Customer Financial Information</p>', unsafe_allow_html=True)
            credit_score = st.number_input(
                "Credit Score",
                min_value=300,
                max_value=850,
                value=int(st.session_state["rs_credit_score"]),
                step=1,
                help="Customer credit rating between 300 and 850."
            )
            balance = st.number_input(
                "Account Balance (€)",
                min_value=0.0,
                max_value=300000.0,
                value=float(st.session_state["rs_balance"]),
                step=1000.0,
                format="%.2f",
                help="Current total deposits held in Euros."
            )
            salary = st.number_input(
                "Estimated Salary (€)",
                min_value=0.0,
                max_value=300000.0,
                value=float(st.session_state["rs_salary"]),
                step=1000.0,
                format="%.2f",
                help="Estimated annual income in Euros."
            )
            products = st.number_input(
                "Number of Products",
                min_value=1,
                max_value=4,
                value=int(st.session_state["rs_products"]),
                step=1,
                help="Total banking products held (1 to 4)."
            )

        with col2:
            st.markdown('<p style="font-size:11px;font-weight:700;color:#7c8882;text-transform:uppercase;margin-bottom:8px;letter-spacing:0.5px;">Customer Profile</p>', unsafe_allow_html=True)
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=int(st.session_state["rs_age"]),
                step=1,
                help="Customer age in years (18-100)."
            )
            tenure = st.number_input(
                "Tenure (Years)",
                min_value=0,
                max_value=10,
                value=int(st.session_state["rs_tenure"]),
                step=1,
                help="Number of years customer has banked with the institution."
            )
            country = st.selectbox(
                "Country",
                options=["France", "Germany", "Spain"],
                index=["France", "Germany", "Spain"].index(st.session_state["rs_country"]),
                help="Regional banking branch location."
            )
            gender = st.selectbox(
                "Gender",
                options=["Female", "Male"],
                index=["Female", "Male"].index(st.session_state["rs_gender"]),
                help="Customer gender."
            )

        with col3:
            st.markdown('<p style="font-size:11px;font-weight:700;color:#7c8882;text-transform:uppercase;margin-bottom:8px;letter-spacing:0.5px;">Banking Relationship</p>', unsafe_allow_html=True)
            has_card = st.selectbox(
                "Has Credit Card",
                options=["Yes", "No"],
                index=0 if st.session_state["rs_has_card"] == "Yes" else 1,
                help="Whether customer holds an active credit card."
            )
            active_member = st.selectbox(
                "Active Member",
                options=["Yes", "No"],
                index=0 if st.session_state["rs_active"] == "Yes" else 1,
                help="Whether customer actively transacts with the bank."
            )

            st.markdown('<div style="height:32px;"></div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("⚡ Calculate Risk", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Secondary action bar for Reset
    reset_col1, reset_col2 = st.columns([1, 5])
    with reset_col1:
        if st.button("↺ Reset Inputs", use_container_width=True):
            st.session_state["rs_credit_score"] = 650
            st.session_state["rs_balance"] = 76000.0
            st.session_state["rs_salary"] = 100000.0
            st.session_state["rs_products"] = 2
            st.session_state["rs_age"] = 38
            st.session_state["rs_tenure"] = 5
            st.session_state["rs_country"] = "France"
            st.session_state["rs_gender"] = "Female"
            st.session_state["rs_has_card"] = "Yes"
            st.session_state["rs_active"] = "Yes"
            if "rs_last_result" in st.session_state:
                del st.session_state["rs_last_result"]
            st.rerun()

    # Calculation Execution
    if submitted:
        input_data = {
            "CreditScore": float(credit_score),
            "Age": float(age),
            "Tenure": float(tenure),
            "Balance": float(balance),
            "NumOfProducts": float(products),
            "HasCrCard": 1.0 if has_card == "Yes" else 0.0,
            "IsActiveMember": 1.0 if active_member == "Yes" else 0.0,
            "EstimatedSalary": float(salary),
            "Geography": country,
            "Gender": gender,
        }

        if is_online:
            prob, factors = predict_churn(input_data, model_data)
            engine_note = "Estimated by validated L2-regularized logistic regression model (AUC: 0.77)."
        else:
            # Rule-based calculation fallback if model is unavailable
            base = 0.20
            if age >= 50:
                base += 0.25
            elif age >= 40:
                base += 0.12
            if active_member == "No":
                base += 0.15
            if country == "Germany":
                base += 0.12
            if products == 1:
                base += 0.08
            elif products >= 3:
                base += 0.35
            prob = max(0.01, min(0.99, base))
            factors = []
            engine_note = "Estimated by transparent portfolio rule-based benchmark (Model Offline)."

        st.session_state["rs_last_result"] = {
            "prob": prob,
            "factors": factors,
            "engine_note": engine_note,
            "is_active": active_member == "Yes",
            "balance": balance,
            "products": products,
            "is_online": is_online,
        }

    # Display Result Presentation
    if "rs_last_result" in st.session_state:
        res = st.session_state["rs_last_result"]
        prob = res["prob"]
        category, color_hex, bg_hex, border_hex = get_risk_classification(prob)
        action = get_recommended_action(prob, res["is_active"], res["balance"], res["products"])

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        _render_html(f"""
<div class="northstar-panel" style="border: 1px solid {border_hex}; background: #ffffff;">
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;">
<div>
<span style="font-size:10px; font-weight:700; color:#7c8882; text-transform:uppercase; letter-spacing:0.8px;">Prediction Assessment</span>
<h2 style="font-family:Manrope,sans-serif; font-size:22px; font-weight:800; color:#172521; margin:4px 0 2px 0;">Risk Evaluation Result</h2>
<p style="font-size:11.5px; color:#7c8983; margin:0;">{html.escape(str(res['engine_note']))}</p>
</div>
<div style="background:{bg_hex}; border:1px solid {border_hex}; border-radius:8px; padding:8px 16px; text-align:right;">
<span style="font-size:10px; font-weight:700; color:{color_hex}; text-transform:uppercase; letter-spacing:0.5px;">Classification</span>
<div style="font-family:Manrope,sans-serif; font-size:18px; font-weight:800; color:{color_hex};">{html.escape(str(category))}</div>
</div>
</div>

<div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px; align-items:center; background:#f6f8f5; border-radius:8px; padding:16px 20px; margin-bottom:16px;">
<div>
<span style="font-size:11px; color:#7c8882; font-weight:600;">Estimated Churn Likelihood</span>
<div style="font-family:Manrope,sans-serif; font-size:36px; font-weight:800; color:{color_hex}; line-height:1.1; margin-top:4px;">
{prob:.1%}
</div>
</div>
<div style="border-left: 1px solid #e9ede8; padding-left: 20px;">
<span style="font-size:11px; color:#7c8882; font-weight:600;">Recommended Retention Action</span>
<p style="font-size:13px; font-weight:600; color:#172521; margin:4px 0 0 0; line-height:1.4;">
{html.escape(str(action))}
</p>
</div>
</div>
""")

        # Factor contributions if model is online
        if res["is_online"] and res["factors"]:
            st.markdown('<p style="font-size:11.5px; font-weight:700; color:#172521; margin:16px 0 8px 0;">Key Profile Risk Influencers (Model Weights)</p>', unsafe_allow_html=True)
            top_factors = res["factors"][:4]
            f_cols = st.columns(4)
            for col, item in zip(f_cols, top_factors):
                with col:
                    impact_color = "#de5442" if item["contribution"] > 0 else "#11785f"
                    impact_arrow = "▲" if item["contribution"] > 0 else "▼"
                    _render_html(f"""
<div style="background:#ffffff; border:1px solid #e9ede8; border-radius:6px; padding:10px 12px;">
<span style="font-size:10px; color:#7c8983; display:block;">{html.escape(str(item['label']))}</span>
<b style="font-size:12px; color:{impact_color};">{impact_arrow} {html.escape(str(item['impact']))}</b>
</div>
""")

        st.markdown('</div>', unsafe_allow_html=True)
