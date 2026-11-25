from __future__ import annotations

import base64
import math
import os
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Airtel | Network Usage Intelligence",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COLOR PALETTE: INDIGO, VIOLET & CORAL TELECOM THEME
# ============================================================

NAV_DARK = "#111827"
NAV_CONTROL = "#1F2937"
INDIGO = "#4338CA"
INDIGO_LIGHT = "#EEF2FF"
CORAL = "#E11D48"
CORAL_LIGHT = "#FFF1F2"
CORAL_BORDER = "#FECDD3"
EMERALD = "#059669"
EMERALD_LIGHT = "#ECFDF5"
VIOLET = "#7C3AED"
CANVAS_BG = "#F3F4F6"
SURFACE = "#FFFFFF"
TEXT_DARK = "#111827"
TEXT_MED = "#374151"
TEXT_MUTED = "#6B7280"
BORDER = "#E5E7EB"


# ============================================================
# COMPACT CUSTOM CSS + STANDARD ANIMATIONS
# ============================================================

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --nav-dark: {NAV_DARK};
    --indigo: {INDIGO};
    --coral: {CORAL};
    --emerald: {EMERALD};
    --canvas-bg: {CANVAS_BG};
    --surface: {SURFACE};
    --border: {BORDER};
}}

/* KEYFRAME ANIMATIONS */
@keyframes fadeSlideUp {{
    0% {{
        opacity: 0;
        transform: translateY(8px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes pulseDot {{
    0% {{
        box-shadow: 0 0 0 0 rgba(129, 140, 248, 0.7);
    }}
    70% {{
        box-shadow: 0 0 0 6px rgba(129, 140, 248, 0);
    }}
    100% {{
        box-shadow: 0 0 0 0 rgba(129, 140, 248, 0);
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }}
}}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background-color: {CANVAS_BG} !important;
    color: {TEXT_DARK} !important;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
    height: 2.6rem !important;
}}

/* SIDEBAR EXPAND / COLLAPSE ARROW VISIBILITY */
[data-testid="stExpandSidebarButton"],
[data-testid="collapsedControl"],
button[kind="headerNoPadding"] {{
    background-color: {SURFACE} !important;
    color: {TEXT_DARK} !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 6px rgba(17, 24, 39, 0.12) !important;
    opacity: 1 !important;
    visibility: visible !important;
    transition: background-color 0.18s ease, border-color 0.18s ease, transform 0.18s ease !important;
}}

[data-testid="stExpandSidebarButton"] svg,
[data-testid="collapsedControl"] svg,
button[kind="headerNoPadding"] svg {{
    fill: {TEXT_DARK} !important;
    color: {TEXT_DARK} !important;
    width: 18px !important;
    height: 18px !important;
}}

[data-testid="stExpandSidebarButton"]:hover,
[data-testid="collapsedControl"]:hover {{
    background-color: {INDIGO_LIGHT} !important;
    border-color: {INDIGO} !important;
    transform: translateX(1px);
}}

[data-testid="stSidebarCollapseButton"] button {{
    background-color: rgba(255, 255, 255, 0.12) !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 7px !important;
    color: #FFFFFF !important;
    transition: background-color 0.18s ease !important;
}}

[data-testid="stSidebarCollapseButton"] svg {{
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}}

[data-testid="stMainBlockContainer"] {{
    max-width: 1520px;
    padding-top: 0.5rem !important;
    padding-bottom: 1.5rem !important;
}}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background: {NAV_DARK} !important;
    border-right: 1px solid {NAV_CONTROL};
}}

[data-testid="stSidebar"] * {{
    color: #F9FAFB !important;
}}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap: 0.45rem !important;
    padding-top: 0.75rem !important;
}}

.sb-brand-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 8px;
}}

.sb-brand-name {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #FFFFFF !important;
}}

.sb-live-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(67, 56, 202, 0.3);
    border: 1px solid rgba(129, 140, 248, 0.4);
    color: #C7D2FE !important;
    font-size: 10.5px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 999px;
}}

.sb-live-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #818CF8;
    animation: pulseDot 2s infinite;
}}

.sb-label {{
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9CA3AF !important;
    margin-bottom: 4px;
}}

[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background: {NAV_CONTROL} !important;
    border: 1px solid #374151 !important;
    border-radius: 7px !important;
    min-height: 36px !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}}

[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover {{
    border-color: #6366F1 !important;
}}

[data-testid="stSidebar"] [data-testid="stSelectbox"] span,
[data-testid="stSidebar"] [data-testid="stSelectbox"] div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg {{
    color: #F9FAFB !important;
    fill: #F9FAFB !important;
    -webkit-text-fill-color: #F9FAFB !important;
    font-size: 12.5px !important;
}}

[data-baseweb="popover"],
[data-baseweb="menu"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 7px !important;
    animation: fadeSlideUp 0.15s ease-out !important;
}}

[data-baseweb="menu"] li,
[data-baseweb="popover"] [role="option"] {{
    background: {SURFACE} !important;
    color: {TEXT_DARK} !important;
    font-size: 12.5px !important;
    transition: background-color 0.14s ease, color 0.14s ease !important;
}}

[data-baseweb="menu"] li:hover,
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {{
    background: {INDIGO_LIGHT} !important;
    color: {INDIGO} !important;
    font-weight: 600 !important;
}}

.sb-box {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 7px;
    padding: 10px 12px;
    font-size: 11.5px;
    line-height: 1.4;
    color: #D1D5DB !important;
    margin-top: 8px;
}}

/* COMPACT TOP HEADER + BRIEFING */
.top-banner {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
    animation: fadeSlideUp 0.24s ease-out both;
}}

.top-banner-left {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.logo-frame {{
    width: 44px;
    min-width: 44px;
    height: 44px;
    border-radius: 8px;
    background: {CANVAS_BG};
    border: 1px solid {BORDER};
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
}}

.logo-frame img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}}

.logo-text-fallback {{
    color: {CORAL};
    font-size: 15px;
    font-weight: 800;
    letter-spacing: -0.04em;
}}

.banner-title {{
    font-size: 19px;
    font-weight: 800;
    color: {TEXT_DARK};
    letter-spacing: -0.02em;
    line-height: 1.15;
}}

.banner-sub {{
    font-size: 12px;
    color: {TEXT_MUTED};
    margin-top: 2px;
}}

.banner-tag {{
    background: {CORAL_LIGHT};
    color: {CORAL};
    border: 1px solid {CORAL_BORDER};
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    white-space: nowrap;
}}

.brief-strip {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 3px solid {INDIGO};
    border-radius: 7px;
    padding: 7px 14px;
    font-size: 12px;
    color: {TEXT_MED};
    margin-bottom: 10px;
    animation: fadeSlideUp 0.28s ease-out both;
}}

.brief-strip strong {{
    color: {TEXT_DARK};
}}

/* COMPACT KPI CARDS WITH ENTRANCE & HOVER MOTION */
.metric-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 9px;
    padding: 11px 15px;
    min-height: 86px;
    animation: fadeSlideUp 0.32s cubic-bezier(0.22, 1, 0.36, 1) both;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}}

.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 18px -6px rgba(17, 24, 39, 0.10);
    border-color: #C7D2FE;
}}

.metric-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
}}

.metric-title {{
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {TEXT_MUTED};
}}

.metric-pill {{
    font-size: 10px;
    font-weight: 700;
    padding: 1px 7px;
    border-radius: 999px;
}}

.metric-num {{
    font-size: 22px;
    font-weight: 800;
    color: {TEXT_DARK};
    letter-spacing: -0.02em;
    margin: 4px 0 2px;
    line-height: 1.15;
}}

.metric-sub {{
    font-size: 11px;
    color: {TEXT_MED};
}}

/* COMPACT SECTION HEADERS */
.sec-head {{
    margin: 6px 0 4px;
    animation: fadeSlideUp 0.3s ease-out both;
}}

.sec-title {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT_DARK};
    letter-spacing: -0.01em;
    line-height: 1.25;
}}

.sec-desc {{
    font-size: 11.5px;
    color: {TEXT_MUTED};
}}

/* COMPACT CHART & TABLE CONTAINERS WITH HOVER & ENTRANCE */
div[data-testid="stPlotlyChart"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 9px;
    padding: 4px 6px 2px;
    animation: fadeSlideUp 0.36s cubic-bezier(0.22, 1, 0.36, 1) both;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}}

div[data-testid="stPlotlyChart"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 18px -6px rgba(17, 24, 39, 0.09);
    border-color: #CBD5E1;
}}

div[data-testid="stDataFrame"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 9px;
    padding: 4px;
    animation: fadeSlideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
}}

/* HIGH-CONTRAST TABS: ALWAYS VISIBLE EVEN WHEN UNSELECTED */
[data-testid="stTabs"] [role="tablist"] {{
    gap: 10px;
    border-bottom: 2px solid {BORDER};
    margin-bottom: 10px;
}}

[data-testid="stTabs"] [role="tab"] {{
    background-color: {SURFACE} !important;
    border: 1px solid #CBD5E1 !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 7px 16px !important;
    opacity: 1 !important;
    visibility: visible !important;
    transition: background-color 0.16s ease, border-color 0.16s ease, transform 0.16s ease !important;
}}

[data-testid="stTabs"] [role="tab"] p,
[data-testid="stTabs"] [role="tab"] span,
[data-testid="stTabs"] [role="tab"] div {{
    color: {TEXT_DARK} !important;
    -webkit-text-fill-color: {TEXT_DARK} !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    opacity: 1 !important;
    visibility: visible !important;
}}

[data-testid="stTabs"] [role="tab"]:hover {{
    background-color: {INDIGO_LIGHT} !important;
    border-color: {INDIGO} !important;
    transform: translateY(-1px);
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background-color: {INDIGO_LIGHT} !important;
    border-color: {INDIGO} !important;
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] p,
[data-testid="stTabs"] [role="tab"][aria-selected="true"] span,
[data-testid="stTabs"] [role="tab"][aria-selected="true"] div {{
    color: {INDIGO} !important;
    -webkit-text-fill-color: {INDIGO} !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background-color: {INDIGO} !important;
    height: 3px !important;
    transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), width 0.22s cubic-bezier(0.22, 1, 0.36, 1) !important;
}}

/* MAIN SELECTBOX (MONTH PICKER) */
[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] label {{
    color: {TEXT_DARK} !important;
    -webkit-text-fill-color: {TEXT_DARK} !important;
    font-weight: 600 !important;
}}

[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background-color: {SURFACE} !important;
    background: {SURFACE} !important;
    border: 1px solid #94A3B8 !important;
    border-radius: 7px !important;
    min-height: 38px !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}}

[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover {{
    border-color: {INDIGO} !important;
}}

[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"] div {{
    color: {TEXT_DARK} !important;
    -webkit-text-fill-color: {TEXT_DARK} !important;
    background-color: transparent !important;
    opacity: 1 !important;
}}

[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {{
    fill: {TEXT_DARK} !important;
    color: {TEXT_DARK} !important;
}}

/* COMPACT FOOTER */
.footer-bar {{
    color: {TEXT_MUTED};
    font-size: 11px;
    border-top: 1px solid {BORDER};
    padding-top: 8px;
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def find_database():
    configured = os.getenv("AIRTEL_DB")
    here = Path(__file__).resolve().parent

    candidates = []
    if configured:
        candidates.append(Path(configured).expanduser())

    candidates.extend([
        here / "airtel.db",
        here / "data" / "airtel.db",
        here / "data" / "raw" / "airtel.db",
        here.parent / "airtel.db",
        Path(r"C:\project\Project 2 AIRTEL TELECOM ANALYTICS\data\raw\airtel.db"),
    ])

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    raise FileNotFoundError(
        "airtel.db not found. Put it beside app.py or inside data/raw."
    )


@st.cache_resource
def get_connection(db_path):
    uri = Path(db_path).as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True, check_same_thread=False)
    connection.execute("PRAGMA query_only = ON")
    return connection


@st.cache_data(show_spinner=False, ttl=600)
def run_sql(db_path, sql, params=()):
    connection = get_connection(db_path)
    return pd.read_sql_query(sql, connection, params=params)


try:
    DB_PATH = str(find_database())
    tables_df = run_sql(
        DB_PATH,
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name IN ('customer_features', 'usage_daily', 'plans')
        """,
    )
    found_tables = set(tables_df["name"].tolist())
    missing = {"customer_features", "usage_daily", "plans"} - found_tables
    if missing:
        raise RuntimeError(f"Missing required tables: {', '.join(sorted(missing))}")

except Exception as exc:
    st.error(f"Database connection error: {exc}")
    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

connection_values = run_sql(
    DB_PATH,
    """
    SELECT DISTINCT connection_type
    FROM customer_features
    WHERE connection_type IS NOT NULL
    ORDER BY connection_type
    """,
)["connection_type"].tolist()

group_values = run_sql(
    DB_PATH,
    """
    SELECT DISTINCT ab_group
    FROM customer_features
    WHERE ab_group IS NOT NULL
    ORDER BY ab_group
    """,
)["ab_group"].tolist()

with st.sidebar:
    st.markdown(
        """
<div class="sb-brand-row">
    <div class="sb-brand-name">airtel</div>
    <div class="sb-live-pill"><span class="sb-live-dot"></span>H1 2025</div>
</div>
<div class="sb-label">Cohort Filters</div>
""",
        unsafe_allow_html=True,
    )

    connection_filter = st.selectbox(
        "Connection Type",
        ["All"] + connection_values,
        key="connection_filter",
    )

    group_filter = st.selectbox(
        "Experiment Group",
        ["All"] + group_values,
        key="group_filter",
    )

    st.markdown(
        """
<div class="sb-box">
    <strong>Filter Scope</strong><br>
    Filters apply to all KPIs, charts, and tables across both tabs.
</div>
""",
        unsafe_allow_html=True,
    )

    st.caption(f"Source: {Path(DB_PATH).name}")


# ============================================================
# SHARED HELPERS & CHART STYLING
# ============================================================

def sql_filters(alias="cf"):
    clauses = []
    values = []

    if connection_filter != "All":
        clauses.append(f"{alias}.connection_type = ?")
        values.append(connection_filter)

    if group_filter != "All":
        clauses.append(f"{alias}.ab_group = ?")
        values.append(group_filter)

    return (
        " AND ".join(clauses) if clauses else "1=1",
        tuple(values),
    )


def section(title, subtitle=""):
    desc_html = f'<span class="sec-desc"> · {subtitle}</span>' if subtitle else ""
    st.markdown(
        f'<div class="sec-head"><span class="sec-title">{title}</span>{desc_html}</div>',
        unsafe_allow_html=True,
    )


def kpi(label, value, note="", badge_text="", badge_bg=INDIGO_LIGHT, badge_fg=INDIGO, delay_s=0.0):
    pill_html = (
        f'<span class="metric-pill" style="background:{badge_bg};color:{badge_fg};">{badge_text}</span>'
        if badge_text else ""
    )
    st.markdown(
        f"""
<div class="metric-card" style="animation-delay: {delay_s:.2f}s;">
    <div class="metric-top">
        <span class="metric-title">{label}</span>
        {pill_html}
    </div>
    <div class="metric-num">{value}</div>
    <div class="metric-sub">{note}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def apply_chart_theme(
    fig,
    height=265,
    show_legend=True,
    horizontal=False,
    hovermode="x unified",
    x_title="",
    y_title="",
):
    fig.update_layout(
        height=height,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        transition=dict(duration=350, easing="cubic-in-out"),
        font=dict(
            family="Inter, -apple-system, sans-serif",
            color=TEXT_DARK,
            size=11,
        ),
        margin=dict(l=46, r=28, t=36 if show_legend else 20, b=36),
        showlegend=show_legend,
        legend=dict(
            title=dict(text="", font=dict(size=10)),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(color=TEXT_MED, size=11),
            bgcolor="rgba(255,255,255,0)",
        ),
        hovermode=hovermode,
        hoverlabel=dict(
            bgcolor=NAV_DARK,
            font_size=11.5,
            font_family="Inter, sans-serif",
            font_color="#FFFFFF",
            bordercolor=NAV_DARK,
        ),
    )

    fig.update_xaxes(
        title_text=x_title,
        showgrid=horizontal,
        gridcolor="#F3F4F6",
        linecolor=BORDER,
        linewidth=1,
        tickfont=dict(color=TEXT_MUTED, size=10.5),
        title_font=dict(color=TEXT_MED, size=11, weight=600),
    )

    fig.update_yaxes(
        title_text=y_title,
        showgrid=not horizontal,
        gridcolor="#F3F4F6",
        zeroline=False,
        linecolor=BORDER if horizontal else None,
        tickfont=dict(color=TEXT_MUTED, size=10.5),
        title_font=dict(color=TEXT_MED, size=11, weight=600),
    )

    return fig


def provenance():
    st.markdown(
        """
<div class="footer-bar">
    <span><strong>Provenance:</strong> Synthetic subscriber records queried directly from the read-only SQLite analytics store.</span>
    <span>Domain C · Network Usage Intelligence</span>
</div>
""",
        unsafe_allow_html=True,
    )


def month_label(month):
    return pd.to_datetime(month + "-01").strftime("%B %Y")


# ============================================================
# HEADER & BRIEFING STRIP
# ============================================================

logo_path = Path(__file__).resolve().parent / "assets" / "airtel-logo.jpg"

if logo_path.exists():
    logo_base64 = base64.b64encode(logo_path.read_bytes()).decode()
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Airtel logo">'
else:
    logo_html = '<span class="logo-text-fallback">airtel</span>'

st.markdown(
    f"""
<div class="top-banner">
    <div class="top-banner-left">
        <div class="logo-frame">
            {logo_html}
        </div>
        <div>
            <div class="banner-title">Network Usage Intelligence</div>
            <div class="banner-sub">Airtel Telecom Analytics · Demand, Experimentation &amp; Quota Utilisation</div>
        </div>
    </div>
    <div class="banner-tag">Domain C · Jan–Jun 2025</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="brief-strip">
    <strong>Planner Briefing:</strong> Track network load, double-data offer lift (Group B vs. Group A), and plan quota headroom across cohorts.
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DASHBOARD TABS
# ============================================================

overview_tab, detail_tab = st.tabs([
    "📊 Overview",
    "🗓️ Month Detail",
])


# ============================================================
# TAB 1: OVERVIEW
# ============================================================

with overview_tab:
    where, params = sql_filters("cf")

    fixed_days = run_sql(
        DB_PATH,
        """
        SELECT SUM(usage_days) AS total_usage_days
        FROM customer_features
        """,
    ).iloc[0]["total_usage_days"]

    step4 = run_sql(
        DB_PATH,
        """
        WITH subscriber_offer AS (
            SELECT
                c.ab_group,
                u.customer_id,
                AVG(u.data_mb) AS customer_mean_mb
            FROM usage_daily u
            JOIN customer_features c
                ON c.customer_id = u.customer_id
            WHERE u.usage_date >= '2025-05-01'
              AND u.usage_date < '2025-07-01'
            GROUP BY c.ab_group, u.customer_id
        )
        SELECT
            ab_group,
            COUNT(*) AS n_subscribers,
            AVG(customer_mean_mb) AS mean_mb,
            SUM(customer_mean_mb) AS sum_mb,
            SUM(customer_mean_mb * customer_mean_mb) AS sum_sq_mb
        FROM subscriber_offer
        GROUP BY ab_group
        """,
    )

    step4_map = {row["ab_group"]: row for _, row in step4.iterrows()}
    step4_lift = None
    step4_pct = None
    step4_p = None

    if "A" in step4_map and "B" in step4_map:
        a = step4_map["A"]
        b = step4_map["B"]
        na = int(a["n_subscribers"])
        nb = int(b["n_subscribers"])

        if na > 1 and nb > 1:
            mean_a = float(a["mean_mb"])
            mean_b = float(b["mean_mb"])

            var_a = (float(a["sum_sq_mb"]) - float(a["sum_mb"]) ** 2 / na) / (na - 1)
            var_b = (float(b["sum_sq_mb"]) - float(b["sum_mb"]) ** 2 / nb) / (nb - 1)
            standard_error = math.sqrt(max(var_a / na + var_b / nb, 0))

            if standard_error > 0 and mean_a != 0:
                step4_z = (mean_b - mean_a) / standard_error
                step4_p = 0.5 * math.erfc(step4_z / math.sqrt(2))
                step4_lift = mean_b - mean_a
                step4_pct = ((mean_b / mean_a) - 1) * 100

    overview_summary = run_sql(
        DB_PATH,
        f"""
        SELECT
            AVG(mb_per_active_day) AS avg_active,
            AVG(mb_per_observed_day) AS avg_calendar
        FROM customer_features cf
        WHERE {where}
        """,
        params,
    ).iloc[0]

    # KPI ROW
    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        kpi(
            "Total Usage Days Recorded",
            f"{float(fixed_days):,.0f}" if pd.notna(fixed_days) else "N/A",
            "Jan–Jun 2025 · Fixed baseline",
            badge_text="Baseline",
            badge_bg="#F3F4F6",
            badge_fg=TEXT_MED,
            delay_s=0.04,
        )

    with c2:
        if step4_lift is not None:
            p_text = f"{step4_p:.2e}" if step4_p < 0.001 else f"{step4_p:.4f}"
            kpi(
                "Double-Data Offer Lift",
                f"{step4_lift:+,.1f} MB",
                f"B vs A: {step4_pct:+.2f}% · p = {p_text}",
                badge_text="May–Jun Promo",
                badge_bg=CORAL_LIGHT,
                badge_fg=CORAL,
                delay_s=0.10,
            )
        else:
            kpi(
                "Double-Data Offer Lift",
                "Unavailable",
                "Requires records in both Groups A & B",
                badge_text="May–Jun Promo",
                badge_bg=CORAL_LIGHT,
                badge_fg=CORAL,
                delay_s=0.10,
            )

    with c3:
        active = overview_summary["avg_active"]
        calendar = overview_summary["avg_calendar"]
        kpi(
            "Data per Active Day",
            f"{active:,.1f} MB" if pd.notna(active) else "N/A",
            f"Calendar day: {calendar:,.1f} MB/day" if pd.notna(calendar) else "Calendar-day unavailable",
            badge_text="Daily Avg",
            badge_bg=INDIGO_LIGHT,
            badge_fg=INDIGO,
            delay_s=0.16,
        )

    # ROW 1 OF CHARTS: MONTHLY USAGE & LIFT (LEFT) + CALENDAR-DAY USAGE (RIGHT)
    r1_left, r1_right = st.columns([1.3, 1.0], gap="small")

    monthly_usage = run_sql(
        DB_PATH,
        f"""
        WITH subscriber_month AS (
            SELECT
                substr(u.usage_date,1,7) AS month,
                cf.ab_group,
                u.customer_id,
                AVG(u.data_mb) AS subscriber_mb
            FROM usage_daily u
            JOIN customer_features cf
                ON cf.customer_id = u.customer_id
            WHERE {where}
            GROUP BY month, cf.ab_group, u.customer_id
        )
        SELECT
            month,
            ab_group,
            AVG(subscriber_mb) AS data_mb_per_active_day,
            COUNT(*) AS subscriber_count
        FROM subscriber_month
        GROUP BY month, ab_group
        ORDER BY month
        """,
        params,
    )

    with r1_left:
        section("Monthly Usage & Lift", "Group A vs B daily MB & % lift")
        if not monthly_usage.empty:
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            for grp, color in [("A", INDIGO), ("B", CORAL)]:
                sub = monthly_usage[monthly_usage["ab_group"] == grp]
                if not sub.empty:
                    fig.add_trace(
                        go.Bar(
                            x=sub["month"],
                            y=sub["data_mb_per_active_day"],
                            name=f"Group {grp} (MB)",
                            text=[f"{v:,.0f}" for v in sub["data_mb_per_active_day"]],
                            textposition="inside",
                            textfont=dict(color="#FFFFFF", size=10, weight=700),
                            marker=dict(color=color, cornerradius=4),
                            customdata=sub[["subscriber_count"]],
                            hovertemplate=(
                                f"<b>Group {grp}</b>: %{{y:,.1f}} MB/day "
                                "(%{customdata[0]:,} subs)<extra></extra>"
                            ),
                        ),
                        secondary_y=False,
                    )

            piv = monthly_usage.pivot(index="month", columns="ab_group", values="data_mb_per_active_day").dropna()
            max_lift = 46.0
            min_lift = -8.0
            if {"A", "B"}.issubset(piv.columns) and not piv.empty:
                lift_pct = ((piv["B"] / piv["A"]) - 1.0) * 100.0
                max_lift = max(float(lift_pct.max()) * 1.28, 12.0)
                min_lift = min(float(lift_pct.min()) - 6.0, -5.0)
                fig.add_trace(
                    go.Scatter(
                        x=list(piv.index),
                        y=list(lift_pct),
                        name="Lift (%)",
                        mode="lines+markers+text",
                        text=[f"{v:+.1f}%" for v in lift_pct],
                        textposition="top center",
                        textfont=dict(color=VIOLET, size=10, weight=700),
                        line=dict(color=VIOLET, width=2.5, dash="dot"),
                        marker=dict(size=7, color=VIOLET, symbol="diamond", line=dict(width=1.5, color=SURFACE)),
                        hovertemplate="<b>Lift</b>: %{y:+.2f}%<extra></extra>",
                    ),
                    secondary_y=True,
                )

            max_mb = float(monthly_usage["data_mb_per_active_day"].max()) * 1.15
            fig.update_layout(barmode="group", bargap=0.25)
            apply_chart_theme(
                fig,
                height=265,
                show_legend=True,
                x_title="Month (2025)",
                y_title="MB / Active Day",
            )
            fig.update_yaxes(range=[0, max_mb], secondary_y=False)
            fig.update_yaxes(
                title_text="Lift (%)",
                range=[min_lift, max_lift],
                secondary_y=True,
                showgrid=False,
                zeroline=True,
                zerolinecolor=BORDER,
                tickfont=dict(color=VIOLET, size=10),
                title_font=dict(color=VIOLET, size=10.5, weight=600),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No monthly usage data available.")

    with r1_right:
        calendar_usage = run_sql(
            DB_PATH,
            f"""
            WITH subscriber_month AS (
                SELECT
                    substr(u.usage_date,1,7) AS month,
                    cf.ab_group,
                    u.customer_id,
                    SUM(u.data_mb) / CAST(strftime(
                        '%d',
                        date(substr(u.usage_date,1,7) || '-01', '+1 month', '-1 day')
                    ) AS REAL) AS calendar_mb
                FROM usage_daily u
                JOIN customer_features cf
                    ON cf.customer_id = u.customer_id
                WHERE {where}
                GROUP BY month, cf.ab_group, u.customer_id
            )
            SELECT
                month,
                ab_group,
                AVG(calendar_mb) AS data_mb_per_calendar_day
            FROM subscriber_month
            GROUP BY month, ab_group
            ORDER BY month
            """,
            params,
        )

        section("Calendar-Day Usage", "Amortized daily MB by group")
        if not calendar_usage.empty:
            fig = go.Figure()
            fill_map = {"A": "rgba(67, 56, 202, 0.12)", "B": "rgba(225, 29, 72, 0.12)"}
            for grp, color, pos in [("A", INDIGO, "bottom center"), ("B", CORAL, "top center")]:
                sub = calendar_usage[calendar_usage["ab_group"] == grp]
                if not sub.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=sub["month"],
                            y=sub["data_mb_per_calendar_day"],
                            mode="lines+markers+text",
                            name=f"Group {grp}",
                            text=[f"{v:,.0f}" for v in sub["data_mb_per_calendar_day"]],
                            textposition=pos,
                            textfont=dict(color=color, size=10, weight=600),
                            fill="tozeroy",
                            fillcolor=fill_map[grp],
                            line=dict(color=color, width=2.5),
                            marker=dict(size=6, color=color, line=dict(width=1.5, color=SURFACE)),
                            hovertemplate=f"<b>Group {grp}</b>: %{{y:,.1f}} MB/day<extra></extra>",
                        )
                    )

            max_cal = float(calendar_usage["data_mb_per_calendar_day"].max()) * 1.24
            apply_chart_theme(
                fig,
                height=265,
                show_legend=True,
                x_title="Month (2025)",
                y_title="MB / Cal Day",
            )
            fig.update_yaxes(range=[0, max_cal])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No calendar usage data available.")

    # ROW 2 OF CHARTS: ACTIVE SUBSCRIBERS (LEFT) + PLAN ALLOWANCE UTILISATION (RIGHT)
    r2_left, r2_right = st.columns([1.0, 1.3], gap="small")

    with r2_left:
        subscriber_counts = run_sql(
            DB_PATH,
            f"""
            SELECT
                substr(u.usage_date,1,7) AS month,
                COUNT(DISTINCT u.customer_id) AS active_subscribers
            FROM usage_daily u
            JOIN customer_features cf
                ON cf.customer_id = u.customer_id
            WHERE {where}
            GROUP BY month
            ORDER BY month DESC
            """,
            params,
        )

        section("Active Subscribers", "Distinct active users per month")
        if not subscriber_counts.empty:
            fig = go.Figure()
            for _, row in subscriber_counts.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=[0, row["active_subscribers"]],
                        y=[row["month"], row["month"]],
                        mode="lines",
                        line=dict(color="#C7D2FE", width=3.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

            fig.add_trace(
                go.Scatter(
                    x=subscriber_counts["active_subscribers"],
                    y=subscriber_counts["month"],
                    mode="markers+text",
                    name="Subscribers",
                    text=[f"{v:,}" for v in subscriber_counts["active_subscribers"]],
                    textposition="middle right",
                    textfont=dict(color=TEXT_DARK, size=10.5, weight=700),
                    marker=dict(size=10, color=INDIGO, line=dict(width=1.5, color=SURFACE)),
                    hovertemplate="<b>%{y}</b>: %{x:,} subscribers<extra></extra>",
                    showlegend=False,
                )
            )

            max_subs = float(subscriber_counts["active_subscribers"].max()) * 1.25
            apply_chart_theme(
                fig,
                height=265,
                show_legend=False,
                horizontal=True,
                hovermode="closest",
                x_title="Active Subscribers",
                y_title="Month",
            )
            fig.update_xaxes(range=[0, max_subs])
            fig.update_yaxes(type="category")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No subscriber records available.")

    allowance = run_sql(
        DB_PATH,
        f"""
        SELECT
            plan_name,
            quota_basis,
            monthly_gb,
            COUNT(*) AS subscribers,
            AVG(
                total_data_mb * 100.0 /
                NULLIF(monthly_gb * 1024.0 * 6.0, 0)
            ) AS allowance_used_pct
        FROM customer_features cf
        WHERE {where}
        GROUP BY plan_name, quota_basis, monthly_gb
        ORDER BY allowance_used_pct ASC
        """,
        params,
    )

    with r2_right:
        section("Plan Allowance Utilisation", "6-month usage vs. 100% plan quota")
        if not allowance.empty:
            max_val = max(float(allowance["allowance_used_pct"].max()) * 1.24, 120.0)
            bar_colors = [
                CORAL if v >= 85 else (VIOLET if v >= 60 else EMERALD)
                for v in allowance["allowance_used_pct"]
            ]

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=[100.0] * len(allowance),
                    y=allowance["plan_name"],
                    orientation="h",
                    name="100% Quota",
                    marker=dict(color="#F3F4F6", line=dict(color=BORDER, width=1), cornerradius=4),
                    hoverinfo="skip",
                )
            )
            fig.add_trace(
                go.Bar(
                    x=allowance["allowance_used_pct"],
                    y=allowance["plan_name"],
                    orientation="h",
                    name="Used (%)",
                    text=[f"{v:.1f}%" for v in allowance["allowance_used_pct"]],
                    textposition="outside",
                    textfont=dict(color=TEXT_DARK, size=10.5, weight=700),
                    marker=dict(color=bar_colors, cornerradius=4),
                    customdata=allowance[["subscribers", "quota_basis"]],
                    hovertemplate=(
                        "<b>%{y}</b>: %{x:.1f}% used "
                        "(%{customdata[0]:,} subs · %{customdata[1]})<extra></extra>"
                    ),
                )
            )
            fig.add_vline(
                x=100.0,
                line_dash="dash",
                line_color=CORAL,
                line_width=1.5,
                annotation_text="100% Cap",
                annotation_position="top left",
                annotation_font=dict(color=CORAL, size=10, weight=700),
            )

            fig.update_layout(barmode="overlay")
            apply_chart_theme(
                fig,
                height=265,
                show_legend=True,
                horizontal=True,
                hovermode="closest",
                x_title="Allowance Used (%)",
                y_title="Plan",
            )
            fig.update_xaxes(range=[0, max_val])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No plan allowance records available.")

    # OVERVIEW TABLE: MONTHLY COHORT & LIFT BREAKDOWN
    section(
        "Monthly Experiment & Subscriber Summary Table",
        "Month-by-month comparison of Group A vs. Group B daily usage, lift, and active subscribers",
    )
    if not monthly_usage.empty:
        piv_mb = monthly_usage.pivot(index="month", columns="ab_group", values="data_mb_per_active_day")
        piv_subs = monthly_usage.pivot(index="month", columns="ab_group", values="subscriber_count").fillna(0)

        rows = []
        for m in sorted(piv_mb.index):
            val_a = piv_mb.loc[m, "A"] if "A" in piv_mb.columns and pd.notna(piv_mb.loc[m, "A"]) else None
            val_b = piv_mb.loc[m, "B"] if "B" in piv_mb.columns and pd.notna(piv_mb.loc[m, "B"]) else None
            subs_total = int(
                (piv_subs.loc[m, "A"] if "A" in piv_subs.columns else 0)
                + (piv_subs.loc[m, "B"] if "B" in piv_subs.columns else 0)
            )
            if val_a is not None and val_b is not None and val_a != 0:
                lift_str = f"{((val_b / val_a) - 1.0) * 100.0:+.2f}%"
            else:
                lift_str = "N/A"

            rows.append({
                "Month": month_label(m),
                "Group A Avg (MB/Day)": f"{val_a:,.1f}" if val_a is not None else "N/A",
                "Group B Avg (MB/Day)": f"{val_b:,.1f}" if val_b is not None else "N/A",
                "B vs A Lift (%)": lift_str,
                "Cohort Subscribers": f"{subs_total:,}",
            })

        cohort_table_df = pd.DataFrame(rows)
        st.dataframe(cohort_table_df, use_container_width=True, hide_index=True, height=230)
    else:
        st.info("No monthly cohort table rows available.")

    provenance()


# ============================================================
# TAB 2: MONTH DETAIL
# ============================================================

with detail_tab:
    months_df = run_sql(
        DB_PATH,
        """
        SELECT DISTINCT substr(usage_date,1,7) AS month
        FROM usage_daily
        WHERE usage_date >= '2025-01-01'
          AND usage_date < '2025-07-01'
        ORDER BY month
        """,
    )

    month_values = months_df["month"].tolist()
    if not month_values:
        st.warning("No usage months found.")
        st.stop()

    month_names = [month_label(month) for month in month_values]
    where_detail, params_detail = sql_filters("cf")

    sel_col, k1, k2, k3 = st.columns([1.0, 1.0, 1.0, 1.0], gap="small")

    with sel_col:
        selected_label = st.selectbox(
            "Select Month",
            month_names,
            index=0,
            key="detail_month",
        )

    selected_month = month_values[month_names.index(selected_label)]

    monthly_summary = run_sql(
        DB_PATH,
        f"""
        SELECT
            COUNT(DISTINCT u.customer_id) AS active_subscribers,
            SUM(u.data_mb) AS total_data_mb,
            COUNT(*) AS usage_day_records,
            SUM(u.data_mb) / NULLIF(COUNT(*),0) AS mb_per_usage_day
        FROM usage_daily u
        JOIN customer_features cf
            ON cf.customer_id = u.customer_id
        WHERE substr(u.usage_date,1,7) = ?
          AND {where_detail}
        """,
        (selected_month,) + params_detail,
    ).iloc[0]

    with k1:
        kpi(
            "Active Subscribers",
            f"{monthly_summary['active_subscribers']:,.0f}",
            selected_label,
            badge_text="Users",
            badge_bg="#F3F4F6",
            badge_fg=TEXT_MED,
            delay_s=0.04,
        )

    with k2:
        total_tb = (
            monthly_summary["total_data_mb"] / 1_000_000
            if pd.notna(monthly_summary["total_data_mb"]) else 0
        )
        kpi(
            "Total Data Carried",
            f"{total_tb:,.2f} TB",
            "Decimal TB",
            badge_text="Volume",
            badge_bg=INDIGO_LIGHT,
            badge_fg=INDIGO,
            delay_s=0.10,
        )

    with k3:
        per_day = monthly_summary["mb_per_usage_day"]
        kpi(
            "Data per Usage Day",
            f"{per_day:,.1f} MB" if pd.notna(per_day) else "N/A",
            f"{monthly_summary['usage_day_records']:,.0f} records",
            badge_text="Daily Avg",
            badge_bg=EMERALD_LIGHT,
            badge_fg=EMERALD,
            delay_s=0.16,
        )

    # ROW 1: DAILY DEMAND + 7D ROLLING LINE (LEFT) & WEEKLY RHYTHM (RIGHT)
    d1_left, d1_right = st.columns([1.25, 1.0], gap="small")

    daily = run_sql(
        DB_PATH,
        f"""
        SELECT
            u.usage_date,
            SUM(u.data_mb) / 1000000.0 AS data_tb,
            COUNT(*) AS usage_day_records,
            COUNT(DISTINCT u.customer_id) AS active_subscribers
        FROM usage_daily u
        JOIN customer_features cf
            ON cf.customer_id = u.customer_id
        WHERE substr(u.usage_date,1,7) = ?
          AND {where_detail}
        GROUP BY u.usage_date
        ORDER BY u.usage_date
        """,
        (selected_month,) + params_detail,
    )

    with d1_left:
        section(f"Daily Demand – {selected_label}", "Daily TB & 7-day average")
        if not daily.empty:
            daily["rolling_7d"] = daily["data_tb"].rolling(window=7, min_periods=1).mean()
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=daily["usage_date"],
                    y=daily["data_tb"],
                    name="Daily TB",
                    marker=dict(color="rgba(67, 56, 202, 0.28)", cornerradius=3),
                    customdata=daily[["usage_day_records", "active_subscribers"]],
                    hovertemplate=(
                        "<b>%{x}</b>: %{y:.3f} TB "
                        "(%{customdata[0]:,} recs · %{customdata[1]:,} subs)<extra></extra>"
                    ),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=daily["usage_date"],
                    y=daily["rolling_7d"],
                    mode="lines+markers",
                    name="7-Day Avg",
                    line=dict(color=CORAL, width=2.5),
                    marker=dict(size=5, color=CORAL),
                    hovertemplate="<b>7-Day Avg</b>: %{y:.3f} TB<extra></extra>",
                )
            )
            apply_chart_theme(
                fig,
                height=260,
                show_legend=True,
                x_title="Date",
                y_title="Traffic (TB)",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No daily usage available.")

    weekday = run_sql(
        DB_PATH,
        f"""
        WITH subscriber_day AS (
            SELECT
                CAST(strftime('%w',u.usage_date) AS INTEGER) AS dow,
                u.customer_id,
                u.usage_date,
                AVG(u.data_mb) AS customer_day_mb
            FROM usage_daily u
            JOIN customer_features cf
                ON cf.customer_id = u.customer_id
            WHERE substr(u.usage_date,1,7) = ?
              AND {where_detail}
            GROUP BY dow, u.customer_id, u.usage_date
        )
        SELECT
            dow,
            CASE dow
                WHEN 0 THEN 'Sun'
                WHEN 1 THEN 'Mon'
                WHEN 2 THEN 'Tue'
                WHEN 3 THEN 'Wed'
                WHEN 4 THEN 'Thu'
                WHEN 5 THEN 'Fri'
                ELSE 'Sat'
            END AS weekday,
            AVG(customer_day_mb) AS avg_mb_per_usage_day,
            COUNT(*) AS usage_day_records
        FROM subscriber_day
        GROUP BY dow
        ORDER BY dow
        """,
        (selected_month,) + params_detail,
    )

    with d1_right:
        section("Weekly Rhythm", "Avg MB/day across weekdays")
        if not weekday.empty:
            wk_mean = float(weekday["avg_mb_per_usage_day"].mean())
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=weekday["weekday"],
                    y=weekday["avg_mb_per_usage_day"],
                    mode="lines+markers+text",
                    name="Daily Avg",
                    text=[f"{v:,.0f}" for v in weekday["avg_mb_per_usage_day"]],
                    textposition="top center",
                    textfont=dict(color=TEXT_DARK, size=10, weight=700),
                    fill="tozeroy",
                    fillcolor="rgba(124, 58, 237, 0.10)",
                    line=dict(color=VIOLET, width=2.5, shape="spline", smoothing=0.8),
                    marker=dict(size=7, color=VIOLET, line=dict(width=1.5, color=SURFACE)),
                    customdata=weekday[["usage_day_records"]],
                    hovertemplate=(
                        "<b>%{x}</b>: %{y:,.1f} MB/day "
                        "(%{customdata[0]:,.0f} recs)<extra></extra>"
                    ),
                    showlegend=False,
                )
            )
            fig.add_hline(
                y=wk_mean,
                line_dash="dot",
                line_color=EMERALD,
                line_width=1.5,
                annotation_text=f"Avg: {wk_mean:,.0f}",
                annotation_position="bottom right",
                annotation_font=dict(color=EMERALD, size=10, weight=700),
            )
            min_y = float(weekday["avg_mb_per_usage_day"].min()) * 0.85
            max_y = float(weekday["avg_mb_per_usage_day"].max()) * 1.18
            apply_chart_theme(
                fig,
                height=260,
                show_legend=False,
                x_title="Day of Week",
                y_title="Avg MB / Day",
            )
            fig.update_xaxes(range=[-0.6, len(weekday) - 0.4])
            fig.update_yaxes(range=[min_y, max_y])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No weekday data available.")

    # ROW 2: EXPERIMENT GROUP (LEFT) & DEVICE TYPE DONUT (RIGHT)
    d2_left, d2_right = st.columns(2, gap="small")

    group_month = run_sql(
        DB_PATH,
        f"""
        WITH subscriber_month AS (
            SELECT
                cf.ab_group,
                u.customer_id,
                AVG(u.data_mb) AS customer_mb
            FROM usage_daily u
            JOIN customer_features cf
                ON cf.customer_id = u.customer_id
            WHERE substr(u.usage_date,1,7) = ?
              AND {where_detail}
            GROUP BY cf.ab_group, u.customer_id
        )
        SELECT
            ab_group,
            AVG(customer_mb) AS mb_per_active_day,
            COUNT(*) AS subscribers
        FROM subscriber_month
        GROUP BY ab_group
        ORDER BY ab_group
        """,
        (selected_month,) + params_detail,
    )

    with d2_left:
        section("Experiment Group Comparison", "Group A vs B mean MB/active day")
        if not group_month.empty:
            colors_grp = [INDIGO if g == "A" else CORAL for g in group_month["ab_group"]]
            fig = go.Figure(
                go.Bar(
                    x=group_month["mb_per_active_day"],
                    y=[f"Group {g}" for g in group_month["ab_group"]],
                    orientation="h",
                    name="MB/Day",
                    text=[f"{v:,.1f} MB" for v in group_month["mb_per_active_day"]],
                    textposition="outside",
                    textfont=dict(color=TEXT_DARK, size=10.5, weight=700),
                    marker=dict(color=colors_grp, cornerradius=4),
                    width=0.45,
                    customdata=group_month[["subscribers"]],
                    hovertemplate=(
                        "<b>%{y}</b>: %{x:,.1f} MB/day "
                        "(%{customdata[0]:,} subs)<extra></extra>"
                    ),
                )
            )
            max_grp = float(group_month["mb_per_active_day"].max()) * 1.25
            apply_chart_theme(
                fig,
                height=245,
                show_legend=False,
                horizontal=True,
                hovermode="closest",
                x_title="MB / Active Day",
                y_title="Group",
            )
            fig.update_xaxes(range=[0, max_grp])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No experiment data available.")

    device_month = run_sql(
        DB_PATH,
        f"""
        WITH subscriber_month AS (
            SELECT
                cf.device_type,
                u.customer_id,
                AVG(u.data_mb) AS customer_mb
            FROM usage_daily u
            JOIN customer_features cf
                ON cf.customer_id = u.customer_id
            WHERE substr(u.usage_date,1,7) = ?
              AND {where_detail}
            GROUP BY cf.device_type, u.customer_id
        )
        SELECT
            device_type,
            AVG(customer_mb) AS mb_per_active_day,
            COUNT(*) AS subscribers
        FROM subscriber_month
        GROUP BY device_type
        ORDER BY mb_per_active_day DESC
        """,
        (selected_month,) + params_detail,
    )

    with d2_right:
        section("Usage by Device Type", "Mean daily MB by handset tier")
        if not device_month.empty:
            donut_palette = [INDIGO, VIOLET, CORAL, EMERALD, "#0284C7"]
            fig = go.Figure(
                go.Pie(
                    labels=device_month["device_type"],
                    values=device_month["mb_per_active_day"],
                    hole=0.52,
                    domain=dict(x=[0.12, 0.88], y=[0.10, 0.90]),
                    marker=dict(colors=donut_palette[:len(device_month)], line=dict(color=SURFACE, width=2)),
                    textinfo="label+value",
                    texttemplate="<b>%{label}</b>: %{value:,.0f} MB",
                    textfont=dict(size=10, color=TEXT_DARK),
                    customdata=device_month[["subscribers"]],
                    hovertemplate=(
                        "<b>%{label}</b>: %{value:,.1f} MB/day "
                        "(%{customdata[0]:,} subs)<extra></extra>"
                    ),
                )
            )
            fig.update_layout(
                annotations=[
                    dict(
                        text="<b>Device<br>MB/Day</b>",
                        x=0.5,
                        y=0.5,
                        font=dict(size=11, color=TEXT_MED),
                        showarrow=False,
                    )
                ]
            )
            apply_chart_theme(fig, height=245, show_legend=False, hovermode="closest")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No device data available.")

    # DAILY BREAKDOWN TABLE FOR SELECTED MONTH
    section(f"Daily Traffic Log – {selected_label}", "Day-by-day carried volume, active users, and record counts")
    if not daily.empty:
        day_table = daily[["usage_date", "data_tb", "active_subscribers", "usage_day_records"]].copy()
        day_table = day_table.rename(
            columns={
                "usage_date": "Date",
                "data_tb": "Traffic (TB)",
                "active_subscribers": "Active Subscribers",
                "usage_day_records": "Usage Records",
            }
        )
        day_table["Traffic (TB)"] = day_table["Traffic (TB)"].map(lambda x: f"{x:.3f}")
        day_table["Active Subscribers"] = day_table["Active Subscribers"].map(lambda x: f"{int(x):,}")
        day_table["Usage Records"] = day_table["Usage Records"].map(lambda x: f"{int(x):,}")
        st.dataframe(day_table, use_container_width=True, hide_index=True, height=180)
    else:
        st.info("No daily table rows available.")

    provenance()