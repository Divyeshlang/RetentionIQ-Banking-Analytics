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
    Renders the European Bank sidebar navigation:
    - Clean desktop width, full viewport height, white background, subtle border
    - Standardized reusable _render_nav_item component across all cards
    - Strict Flexbox alignment and left-aligned text with outline icons
    - WORKSPACE:
        - Overview
        - Customers (with 10k badge)
        - Insights
        - Risk Studio
    """
    total_cust = len(df)
    badge_label = f"{total_cust // 1000}k" if total_cust >= 1000 else f"{total_cust}"

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Overview"

    with st.sidebar:
        # 1. Branding Header (European Bank)
        _render_sidebar_html("""
<div class="sb-brand">
    <div class="sb-brand-mark">
        <span></span><span></span><span></span><span></span>
    </div>
    <div>
        <b>European Bank</b>
        <small>PORTFOLIO INTELLIGENCE</small>
    </div>
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

        # 3. Enterprise Footer Card
        _render_sidebar_html(f"""
<div class="sb-help-card">
    <b>✳ European Bank Workspace</b>
    <p>Database active with <b>{len(df):,}</b> verified customer accounts.</p>
</div>
""")

    return {
        "page": st.session_state["current_page"],
    }
