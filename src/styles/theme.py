import streamlit as st

def apply_custom_theme():
    """
    Inject Northstar European Bank design system:
    - Fonts: DM Sans and Manrope
    - Clean white persistent sidebar with Northstar branding and section groups
    - Slim top navigation bar with breadcrumbs and live data indicator
    - Light grey/off-white dashboard background (#f6f7f4)
    - Card panels with crisp subtle lines (#e9ede8), soft shadows, and refined badges
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #172521;
        --muted: #7c8983;
        --line: #e9ede8;
        --bg: #f6f7f4;
        --panel: #ffffff;
        --green: #11785f;
        --mint: #70d1aa;
        --navy: #183c35;
        --blue: #526eeb;
        --amber: #e4a43d;
        --red: #de5442;
        --shadow: 0 2px 10px rgba(24, 49, 40, 0.03);
    }

    /* Core Application styling */
    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--ink);
    }

    .stApp {
        background-color: var(--bg) !important;
    }

    /* Reduce default container padding to fit the Northstar grid */
    .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1400px !important;
    }

    /* ---------------- TOPBAR COMPONENT ---------------- */
    .northstar-topbar {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 9px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(24, 49, 40, 0.02);
    }

    .northstar-breadcrumb {
        font-size: 11px;
        color: #98a19c;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .northstar-breadcrumb span {
        color: #d0d5d1;
    }

    .northstar-breadcrumb b {
        color: #3a4640;
        font-weight: 600;
    }

    .northstar-top-actions {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .northstar-live {
        font-size: 10px;
        color: #748078;
        display: inline-flex;
        align-items: center;
        font-weight: 500;
    }

    .northstar-live i {
        display: inline-block;
        width: 6px;
        height: 6px;
        background: #40b482;
        border-radius: 50%;
        margin-right: 6px;
        box-shadow: 0 0 0 3px #e4f5ed;
    }

    .northstar-avatar {
        height: 27px;
        width: 27px;
        border-radius: 50%;
        background: #ece6dd;
        color: #765e49;
        display: grid;
        place-items: center;
        font-size: 10px;
        font-weight: 700;
        font-family: 'Manrope', sans-serif;
    }

    /* ---------------- PAGE HEADING ---------------- */
    .northstar-page-heading {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 18px;
    }

    .northstar-eyebrow {
        color: #789083;
        font-size: 9px;
        letter-spacing: 1.1px;
        font-weight: 700;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 4px;
    }

    .northstar-eyebrow-mark {
        color: #20a276;
    }

    .northstar-heading-title {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        font-size: 24px;
        letter-spacing: -0.8px;
        color: var(--ink);
        margin: 0 0 4px 0;
    }

    .northstar-heading-subtitle {
        color: #8c9691;
        font-size: 11.5px;
        margin: 0;
    }

    /* ---------------- KPI CARDS ---------------- */
    .northstar-kpi-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 9px;
        box-shadow: var(--shadow);
        padding: 14px 16px 12px;
        min-height: 114px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .northstar-kpi-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(24, 49, 40, 0.05);
    }

    .northstar-kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .northstar-kpi-label {
        font-size: 10.5px;
        font-weight: 600;
        color: #7c8882;
        letter-spacing: 0.2px;
    }

    .northstar-kpi-symbol {
        width: 24px;
        height: 24px;
        border-radius: 6px;
        display: grid;
        place-items: center;
        font-size: 12px;
        font-weight: 700;
    }

    .sym-blue { background: #eef0ff; color: #596ee8; }
    .sym-green { background: #eaf6ef; color: #1a9669; }
    .sym-amber { background: #fff5e7; color: #d5942a; }
    .sym-red { background: #fef0ed; color: #de5442; }

    .northstar-kpi-value {
        font-family: 'Manrope', sans-serif;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: var(--ink);
        margin: 6px 0 2px 0;
        line-height: 1.1;
    }

    .northstar-kpi-foot {
        font-size: 9.5px;
        color: #9aa29d;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* ---------------- CHART PANELS ---------------- */
    .northstar-panel {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 9px;
        box-shadow: var(--shadow);
        padding: 18px 20px 14px;
        margin-bottom: 16px;
    }

    .northstar-panel-head {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
    }

    .northstar-panel-title {
        font-family: 'Manrope', sans-serif;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: -0.2px;
        color: var(--ink);
        margin: 0 0 2px 0;
    }

    .northstar-panel-question {
        font-size: 10.5px;
        color: #11785f;
        font-weight: 600;
        margin: 0;
    }

    .northstar-takeaway {
        background: #f6f9f7;
        border-left: 3px solid #11785f;
        border-radius: 0 6px 6px 0;
        padding: 10px 14px;
        font-size: 11px;
        color: #273b33;
        line-height: 1.45;
        margin-top: 10px;
    }

    .northstar-takeaway-alert {
        background: #fff9f0;
        border-left-color: #e4a43d;
        color: #6d4b14;
    }

    /* ---------------- PRIORITY SECTION ---------------- */
    .northstar-priority-container {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 9px;
        box-shadow: var(--shadow);
        padding: 20px;
        margin-top: 18px;
    }

    .northstar-summary-banner {
        background: #fdf5f4;
        border: 1px solid #f9deda;
        border-radius: 6px;
        padding: 11px 15px;
        color: #8c2e22;
        font-size: 11.5px;
        line-height: 1.5;
        margin: 10px 0 16px 0;
    }

    /* ---------------- SIDEBAR CUSTOMIZATION ---------------- */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e9ede8 !important;
        min-width: 320px !important;
        max-width: 345px !important;
        padding-top: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding: 16px 16px 20px 16px !important;
    }

    /* Sidebar vertical block spacing: compact 4px gap */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 4px !important;
    }

    /* Group labels close to items with clear vertical space */
    .sb-group-heading {
        display: block !important;
        font-size: 11px !important;
        letter-spacing: 1.2px !important;
        font-weight: 700 !important;
        color: #8c9691 !important;
        text-transform: uppercase !important;
        padding: 14px 6px 6px 6px !important;
        margin: 0 !important;
        line-height: 1.3 !important;
        font-family: 'Manrope', sans-serif !important;
        box-sizing: border-box !important;
    }

    .sb-manage-heading {
        padding-top: 22px !important;
    }

    /* Sidebar Navigation Buttons - Clean, standardized, non-colliding */
    [data-testid="stSidebar"] .stButton {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stSidebar"] .stButton>button {
        width: 100% !important;
        height: 42px !important;
        min-height: 42px !important;
        max-height: 42px !important;
        padding: 0 14px !important;
        border-radius: 9px !important;
        border: 1px solid transparent !important;
        background-color: transparent !important;
        color: #4b5853 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        text-align: left !important;
        transition: all 0.14s ease !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
        line-height: normal !important;
    }

    [data-testid="stSidebar"] .stButton>button p {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #4b5853 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        line-height: normal !important;
    }

    /* Subtle hover effect for inactive items */
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #f6f8f6 !important;
        color: #172521 !important;
        border-color: #e9ede8 !important;
    }

    [data-testid="stSidebar"] .stButton>button:hover p {
        color: #172521 !important;
    }

    /* Active selected item (type='primary'): full light mint-green background (#EAF4EF) & dark teal text (#087A68) */
    [data-testid="stSidebar"] button[kind="primary"],
    [data-testid="stSidebar"] [data-testid="baseButton-primary"] {
        background-color: #EAF4EF !important;
        color: #087A68 !important;
        font-weight: 600 !important;
        border: 1px solid #d3e7dd !important;
    }

    [data-testid="stSidebar"] button[kind="primary"] p,
    [data-testid="stSidebar"] [data-testid="baseButton-primary"] p {
        color: #087A68 !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] button[kind="secondary"],
    [data-testid="stSidebar"] [data-testid="baseButton-secondary"] {
        background-color: transparent !important;
        color: #4b5853 !important;
        border: 1px solid transparent !important;
    }

    .sb-health-panel {
        background: #f4f7f5 !important;
        border: 1px solid #dbe6e0 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 4px 0 6px 0 !important;
        font-size: 10.5px !important;
    }

    .sb-health-panel b {
        color: #087A68 !important;
        display: block !important;
        margin-bottom: 2px !important;
    }

    .sb-health-panel span {
        color: #576760 !important;
    }

    /* Workspace brand badge in sidebar */
    .sb-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 18px 4px 14px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 12px;
    }

    .sb-brand-mark {
        height: 26px;
        width: 26px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2.5px;
        transform: rotate(-45deg);
    }

    .sb-brand-mark span {
        background: #16765d;
        border-radius: 3px 3px 1px 3px;
    }

    .sb-brand-mark span:nth-child(2),
    .sb-brand-mark span:nth-child(3) {
        opacity: 0.57;
    }

    .sb-brand b {
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        font-size: 17px;
        letter-spacing: -0.8px;
        display: block;
        color: var(--ink);
        line-height: 1.1;
    }

    .sb-brand small {
        display: block;
        color: #94a098;
        letter-spacing: 1.15px;
        font-size: 8px;
        font-weight: 700;
        margin-top: 1px;
    }

    .sb-workspace {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 8px 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        background: #ffffff;
        margin-bottom: 12px;
    }

    .sb-workspace-icon {
        width: 26px;
        height: 26px;
        border-radius: 6px;
        background: #e7f3ed;
        color: #14785e;
        display: grid;
        place-items: center;
        font-weight: 700;
        font-size: 11px;
    }

    .sb-workspace b {
        font-size: 11px;
        color: #172521;
        display: block;
        line-height: 1.2;
    }

    .sb-workspace small {
        font-size: 8.5px;
        color: #98a19d;
        display: block;
    }

    /* Help & profile widget at bottom of sidebar */
    .sb-help-card {
        background: #f6f8f5;
        border-radius: 8px;
        padding: 11px 12px;
        margin-top: 18px;
        font-size: 10px;
    }

    .sb-help-card b {
        font-size: 10.5px;
        color: #172521;
        display: block;
        margin-bottom: 3px;
    }

    .sb-help-card p {
        font-size: 9.5px;
        color: #7d8982;
        line-height: 1.4;
        margin: 0;
    }

    /* Streamlit widgets refinements */
    div[data-testid="stPlotlyChart"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line) !important;
        border-radius: 7px !important;
        overflow: hidden !important;
    }

    /* Buttons */
    .stButton>button {
        border: 1px solid var(--line) !important;
        background: #ffffff !important;
        color: #3e4b44 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
    }

    .stButton>button:hover {
        border-color: #20a276 !important;
        color: #11785f !important;
        background: #f6f8f5 !important;
    }

    .stDownloadButton>button {
        background: #16765d !important;
        color: #ffffff !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 6px 14px !important;
    }

    .stDownloadButton>button:hover {
        background: #11624c !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)
