import textwrap
import pandas as pd
import streamlit as st


def _render_sidebar_html(raw_html: str):
    st.markdown(textwrap.dedent(raw_html).strip(), unsafe_allow_html=True)


def _render_nav_item(label: str, page_key: str, icon: str, badge: str = None) -> bool:
    """
    Reusable navigation card component:
    - Native Streamlit button with type='primary' for active, 'secondary' for inactive
    - 41px height, vertically centered, left-aligned
    - Inline badge for Customers
    - Returns True if clicked
    """
    is_active = st.session_state.get("current_page") == page_key
    badge_suffix = f"   ·   {badge}" if badge else ""
    btn_text = f"{icon}  {label}{badge_suffix}"
    btn_type = "primary" if is_active else "secondary"

    clicked = st.button(
        btn_text,
        key=f"sb_nav_btn_{page_key.replace(' ', '_')}",
        type=btn_type,
        use_container_width=True,
    )

    if clicked:
        st.session_state["current_page"] = page_key
        st.rerun()

    return clicked


def render_sidebar(df: pd.DataFrame) -> dict:
    """
    Renders the Northstar Enterprise Bank sidebar navigation:
    - Fixed 320-345px desktop width, full viewport height, white background, subtle border
    - Standardized reusable _render_nav_item component across all cards
    - Strict Flexbox alignment without absolute offsets, negative margins, or manual translate
    - WORKSPACE:
        - Overview
        - Customers (with independently positioned top-right badge)
        - Insights
        - Risk Studio
    - MANAGE:
        - Model Health
        - Settings
    """
    total_cust = len(df)
    badge_label = f"{total_cust // 1000}k" if total_cust >= 1000 else f"{total_cust}"

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Overview"

    with st.sidebar:
        # 1. Branding Header & Workspace Selector
        _render_sidebar_html("""
<div class="sb-brand">
    <div class="sb-brand-mark">
        <span></span><span></span><span></span><span></span>
    </div>
    <div>
        <b>northstar</b>
        <small>EUROPEAN BANK</small>
    </div>
</div>
<div class="sb-workspace">
    <span class="sb-workspace-icon">N</span>
    <div style="flex:1;">
        <b>Northstar Europe</b>
        <small>Enterprise workspace</small>
    </div>
    <span style="color:#909a95; font-size:11px;">⌄</span>
</div>
""")

        # 2. WORKSPACE Group
        st.markdown('<div class="sb-group-heading">WORKSPACE</div>', unsafe_allow_html=True)
        
        _render_nav_item(
            label="Overview",
            page_key="Overview",
            icon="⊞",
        )
        _render_nav_item(
            label="Customers",
            page_key="Customers Requiring Attention",
            icon="👥",
            badge=badge_label,
        )
        _render_nav_item(
            label="Insights",
            page_key="Strategic Portfolio Recommendations",
            icon="◔",
        )
        _render_nav_item(
            label="Risk Studio",
            page_key="Risk Studio",
            icon="🛡",
        )

        # 3. MANAGE Group
        st.markdown('<div class="sb-group-heading sb-manage-heading">MANAGE</div>', unsafe_allow_html=True)

        is_health = st.session_state.get("show_model_health", False)
        health_type = "primary" if is_health else "secondary"
        if st.button("◈  Model Health", key="sb_btn_model_health_card", type=health_type, use_container_width=True):
            st.session_state["show_model_health"] = not is_health
            st.rerun()

        if st.session_state.get("show_model_health", False):
            _render_sidebar_html("""
<div class="sb-health-panel">
    <b>● Model Online</b>
    <span>L2 Logistic Pipeline AUC: 0.772. Calibration healthy.</span>
</div>
""")

        if st.button("⚙  Settings", key="sb_btn_settings_card", type="secondary", use_container_width=True):
            st.session_state["filter_engagement"] = ["Active", "Inactive"]
            st.session_state["filter_geo"] = ["France", "Germany", "Spain"]
            st.session_state["filter_products"] = (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max()))
            st.session_state["filter_balance_min"] = 0
            st.session_state["filter_salary_min"] = 0
            st.session_state["filter_balance_cutoff"] = int(df["Balance"].quantile(0.75))
            st.session_state["filter_salary_cutoff"] = int(df["EstimatedSalary"].quantile(0.75))
            st.toast("Settings restored to defaults", icon="⚙️")
            st.rerun()

        # 4. Enterprise Footer Card
        _render_sidebar_html(f"""
<div class="sb-help-card">
    <b>✳ Enterprise Bank Workspace</b>
    <p>Database active with <b>{len(df):,}</b> verified customer accounts.</p>
</div>
""")

    return {
        "page": st.session_state["current_page"],
    }
