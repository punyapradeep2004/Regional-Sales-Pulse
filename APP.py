# ============================================================
# REGIONAL SALES PULSE
# Interactive Business Intelligence Dashboard
# ============================================================

import warnings
from datetime import date
from html import escape
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# --------------------------- PAGE CONFIG ---------------------------
st.set_page_config(
    page_title="Regional Sales Pulse | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
.stApp [data-testid="stAppViewContainer"] .main .block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
    height: 2rem;
    border-bottom: none !important;
    box-shadow: none !important;
}

[data-testid="stAppViewContainer"] {
    border-top: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)
# --------------------------- PROFESSIONAL THEME ---------------------------
BG = "#F4F6F9"
NAVY = "#14243A"
PRIMARY = "#2F527A"
STEEL = "#6E88A6"
PLATINUM = "#D5DDE6"
GOLD = "#B69A63"
GREEN = "#287A68"
RED = "#B65C62"
WHITE = "#FFFFFF"
TEXT = "#26364A"
MUTED = "#758397"
GRID = "#E9EDF2"

st.markdown(
    f"""
    <style>
    .stApp {{ background: {BG}; color: {TEXT}; }}
    [data-testid="stSidebar"] {{ background: {NAVY}; }}
    [data-testid="stSidebar"] * {{ color: #F4F6F9 !important; }}
    [data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: #14243A !important;
    }}

    /* Compact filter dropdown arrow beside each filter heading */
    /* Arrow button stays blue like the sidebar, both before and after opening */
    [data-testid="stSidebar"] [data-testid="stPopover"] > button {{
        background: #173F70 !important;
        color: #FFFFFF !important;
        border: 1px solid #6E88A6 !important;
        border-radius: 7px !important;
        min-height: 1.75rem !important;
        height: 1.75rem !important;
        min-width: 1.9rem !important;
        width: 1.9rem !important;
        padding: 0 !important;
        margin-top: 0 !important;
        box-shadow: none !important;
    }}
    [data-testid="stSidebar"] [data-testid="stPopover"] > button:hover,
    [data-testid="stSidebar"] [data-testid="stPopover"] > button:focus,
    [data-testid="stSidebar"] [data-testid="stPopover"] > button:active {{
        background: #173F70 !important;
        color: #FFFFFF !important;
        border-color: #9FB4CC !important;
        box-shadow: none !important;
    }}
    [data-testid="stSidebar"] [data-testid="stPopover"] > button *,
    [data-testid="stSidebar"] [data-testid="stPopover"] > button svg {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        font-size: 0.8rem !important;
    }}

    /* Force the five sidebar filter arrow buttons to stay navy-blue. */
    [data-testid="stSidebar"] [data-testid="stPopover"] button,
    [data-testid="stSidebar"] [data-testid="stPopover"] button:hover,
    [data-testid="stSidebar"] [data-testid="stPopover"] button:focus,
    [data-testid="stSidebar"] [data-testid="stPopover"] button:active,
    [data-testid="stSidebar"] [data-testid="stPopover"] button:focus-visible,
    [data-testid="stSidebar"] [data-testid="stPopover"] button[aria-expanded="true"] {{
        background-color: #173F70 !important;
        background: #173F70 !important;
        color: white !important;
        border: 1px solid #6E88A6 !important;
        box-shadow: none !important;
        min-height: 1.75rem !important;
        height: 1.75rem !important;
        padding: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stPopover"] button svg,
    [data-testid="stSidebar"] [data-testid="stPopover"] button span,
    [data-testid="stSidebar"] [data-testid="stPopover"] button p {{
        color: white !important;
        stroke: white !important;
    }}

    [data-testid="stPopoverBody"],
    [data-testid="stPopoverBody"] * {{
        color: #14243A !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stCheckbox"] {{
        padding: 0.05rem 0 !important;
    }}
    [data-testid="stPopoverBody"] input {{
        accent-color: #C85B72 !important;
    }}
    .selected-filter-box {{
        background: #FFFFFF;
        border: 1px solid #D5DDE6;
        border-radius: 7px;
        padding: 7px 8px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 5px;
        min-height: 36px;
        margin: 2px 0 11px 0;
    }}
    .selected-filter-tag {{
        display: inline-flex;
        align-items: center;
        background: #C85B72;
        color: #FFFFFF !important;
        border-radius: 5px;
        padding: 3px 8px;
        font-size: 0.73rem;
        line-height: 1.35;
        font-weight: 650;
        white-space: nowrap;
    }}

    [data-testid="stSidebar"] [class*="st-key-remove_tag_"] button {{
        background: #C85B72 !important;
        color: #FFFFFF !important;
        border: 0 !important;
        border-radius: 6px !important;
        min-height: 1.65rem !important;
        height: 1.65rem !important;
        padding: 0.1rem 0.5rem !important;
        font-size: 0.72rem !important;
        font-weight: 650 !important;
        white-space: nowrap !important;
    }}
    [data-testid="stSidebar"] [class*="st-key-remove_tag_"] button * {{
        color: #FFFFFF !important;
    }}

    .selected-filter-empty {{
        color: #758397 !important;
        font-size: 0.75rem;
        font-style: italic;
    }}

    /* Visible Order Date Range display: black dates on a white box */
    [data-testid="stSidebar"] [data-testid="stTextInput"] input {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #FFFFFF !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }}
    /* Compact native calendar control: keep its calendar button visible,
       but hide the duplicate date text inside this small control. */
    [data-testid="stSidebar"] [data-testid="stDateInput"] input {{
        width: 1px !important;
        min-width: 1px !important;
        max-width: 1px !important;
        padding: 0 !important;
        border: 0 !important;
        opacity: 0 !important;
        color: transparent !important;
        -webkit-text-fill-color: transparent !important;
    }}
    [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"] {{
        width: 1px !important;
        min-width: 1px !important;
        border: 0 !important;
        background: transparent !important;
    }}
    [data-testid="stSidebar"] [data-testid="stDateInput"] button {{
        background: #FFFFFF !important;
        color: #14243A !important;
        border: 1px solid #D5DDE6 !important;
        min-width: 2.5rem !important;
        min-height: 2.5rem !important;
    }}
    [data-testid="stSidebar"] [data-testid="stDateInput"] svg {{
        color: #14243A !important;
        fill: #14243A !important;
    }}
    .main-title {{
        color: {NAVY}; font-size: 2.55rem; font-weight: 800;
        letter-spacing: 1.2px; margin-bottom: 0.05rem;
    }}
    .sub-title {{
        color: {PRIMARY}; font-size: 1.12rem; font-weight: 700;
        letter-spacing: 1.8px; margin-top: 0;
    }}
    .tagline {{
        color: {MUTED}; font-size: 0.94rem; margin-top: 0.35rem;
        margin-bottom: 1.15rem;
    }}
    .section-title {{
        color: {NAVY}; font-size: 1.25rem; font-weight: 750;
        border-bottom: 2px solid {PLATINUM};
        padding-bottom: 0.35rem; margin-top: 1.1rem;
    }}
    .kpi-card {{
        background: {WHITE}; border: 1px solid {PLATINUM};
        border-top: 4px solid {PRIMARY}; border-radius: 12px;
        padding: 15px 17px 13px 17px; min-height: 112px;
        box-shadow: 0 2px 8px rgba(20,36,58,0.045);
    }}
    .kpi-label {{
        color: {MUTED}; font-size: 0.78rem; font-weight: 700;
        letter-spacing: 0.8px; text-transform: uppercase;
    }}
    .kpi-value {{
        color: {NAVY}; font-size: 1.55rem; font-weight: 800;
        margin-top: 8px; white-space: nowrap;
    }}
    .meta-line {{
        color: {MUTED}; font-size: 0.82rem;
        border-bottom: 1px solid {PLATINUM}; padding-bottom: 10px;
    }}
    div[data-testid="stExpander"] {{
        background: {WHITE}; border: 1px solid {PLATINUM};
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------- DATA LOADING ---------------------------
@st.cache_data
def load_data(file_bytes=None):
    """Load the supplied Superstore CSV and prepare the analysis columns."""
    if file_bytes is None:
        data = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    else:
        from io import BytesIO
        data = pd.read_csv(BytesIO(file_bytes), encoding="latin1")

    required = [
        "Order ID", "Order Date", "Region", "Segment", "Category",
        "Sub-Category", "Ship Mode", "Sales", "Profit", "Discount"
    ]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"Required columns are missing: {missing}")

    data = data.copy()
    # The supplied CSV stores dates in day-month-year order.
    data["Order Date"] = pd.to_datetime(
        data["Order Date"], dayfirst=True, errors="coerce"
    )
    for column in ["Sales", "Profit", "Discount"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(
        subset=["Order Date", "Sales", "Profit", "Discount", "Order ID"]
    )
    return data

# The app looks for the CSV beside app.py. If it is not found, allow upload.
try:
    df = load_data()
except FileNotFoundError:
    st.info("Upload the Sample Superstore CSV to open the dashboard.")
    uploaded = st.file_uploader("Upload Sample - Superstore.csv", type=["csv"])
    if uploaded is None:
        st.stop()
    df = load_data(uploaded.getvalue())

if df.empty:
    st.error("The dataset contains no valid records after date and numeric checks.")
    st.stop()

# --------------------------- SIDEBAR FILTERS ---------------------------
st.sidebar.markdown("## DATA FILTERS")
st.sidebar.caption("Choose filters to update the complete dashboard.")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

# Order Date Range: show dates in one white box and a native calendar icon beside it.
default_start_date = date(2014, 1, 3)
default_end_date = date(2017, 12, 30)

# Keep the default dates within the available dataset period.
default_start_date = max(min_date, min(default_start_date, max_date))
default_end_date = max(default_start_date, min(default_end_date, max_date))

if "order_date_range_value" not in st.session_state:
    st.session_state["order_date_range_value"] = (
        default_start_date,
        default_end_date
    )

st.sidebar.markdown("**Order Date Range**")

date_display_col, date_calendar_col = st.sidebar.columns([0.86, 0.14], gap="small")

with date_display_col:
    selected_start, selected_end = st.session_state["order_date_range_value"]
    st.text_input(
        "Selected order dates",
        value=f"{selected_start:%d/%m/%Y} - {selected_end:%d/%m/%Y}",
        disabled=True,
        label_visibility="collapsed",
        key="order_date_range_display"
    )

with date_calendar_col:
    # This is the real Streamlit date-range calendar control.
    # Its text field is visually collapsed by CSS, leaving the calendar icon.
    picked_dates = st.date_input(
        "Calendar",
        value=st.session_state["order_date_range_value"],
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY",
        key="order_date_range_picker",
        label_visibility="collapsed"
    )

if isinstance(picked_dates, (tuple, list)) and len(picked_dates) == 2:
    st.session_state["order_date_range_value"] = (
        picked_dates[0],
        picked_dates[1]
    )

start_date, end_date = st.session_state["order_date_range_value"]

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
subcategories = sorted(df["Sub-Category"].dropna().unique().tolist())
segments = sorted(df["Segment"].dropna().unique().tolist())
ship_modes = sorted(df["Ship Mode"].dropna().unique().tolist())


# Each filter has a small arrow beside its heading. The popover contains
# checkboxes, while the selected values appear as removable red tags below.
def _select_all_filter_options(master_key, option_keys):
    value = bool(st.session_state[master_key])
    for option_key in option_keys:
        st.session_state[option_key] = value


def _remove_filter_option(option_key, master_key, option_keys):
    st.session_state[option_key] = False
    st.session_state[master_key] = all(
        bool(st.session_state.get(key, False)) for key in option_keys
    )


def _sync_filter_select_all(master_key, option_keys):
    st.session_state[master_key] = all(
        bool(st.session_state.get(option_key, False))
        for option_key in option_keys
    )


def render_sidebar_filter(label, options, key_prefix):
    master_key = f"{key_prefix}_select_all"
    option_keys = [f"{key_prefix}_option_{i}" for i in range(len(options))]

    # Initialize each option as selected on the first dashboard load.
    for option_key in option_keys:
        if option_key not in st.session_state:
            st.session_state[option_key] = True
    if master_key not in st.session_state:
        st.session_state[master_key] = True

    heading_col, arrow_col = st.sidebar.columns([0.82, 0.18], gap="small")
    with heading_col:
        st.markdown(
            f'<div style="color:#F4F6F9;font-weight:700;'
            f'font-size:0.93rem;padding-top:0.24rem;">{escape(label)}</div>',
            unsafe_allow_html=True
        )

    with arrow_col:
        with st.popover("▾", use_container_width=True):
            st.checkbox(
                "Select All",
                key=master_key,
                on_change=_select_all_filter_options,
                args=(master_key, option_keys)
            )
            st.divider()
            for option, option_key in zip(options, option_keys):
                st.checkbox(
                    str(option),
                    key=option_key,
                    on_change=_sync_filter_select_all,
                    args=(master_key, option_keys)
                )

    selected_values = [
        option for option, option_key in zip(options, option_keys)
        if st.session_state.get(option_key, False)
    ]

    # The white container holds actual clickable red tag-buttons.
    # Clicking a tag removes only that one option from the active filter.
    with st.sidebar.container(border=True):
        if selected_values:
            tag_cols = st.columns(min(3, len(selected_values)), gap="small")
            for index, (value, option_key) in enumerate(
                (item for item in zip(options, option_keys)
                 if st.session_state.get(item[1], False))
            ):
                with tag_cols[index % len(tag_cols)]:
                    st.button(
                        f"{value} ×",
                        key=f"remove_tag_{key_prefix}_{index}",
                        on_click=_remove_filter_option,
                        args=(option_key, master_key, option_keys),
                        use_container_width=True
                    )
        else:
            st.caption("No options selected")

    # Read state again after rendering the removable tags.
    return [
        option for option, option_key in zip(options, option_keys)
        if st.session_state.get(option_key, False)
    ]


selected_regions = render_sidebar_filter("Region", regions, "region_filter")
selected_categories = render_sidebar_filter(
    "Product Category", categories, "category_filter"
)
selected_subcategories = render_sidebar_filter(
    "Sub-Category", subcategories, "subcategory_filter"
)
selected_segments = render_sidebar_filter(
    "Customer Segment", segments, "segment_filter"
)
selected_ship_modes = render_sidebar_filter(
    "Ship Mode", ship_modes, "shipmode_filter"
)


st.sidebar.markdown("---")
st.sidebar.caption(
    "All KPIs, charts, summaries, insights and recommendations respond to these filters."
)

filtered = df[
    (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Sub-Category"].isin(selected_subcategories))
    & (df["Segment"].isin(selected_segments))
    & (df["Ship Mode"].isin(selected_ship_modes))
].copy()

# --------------------------- HEADER ---------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:18px;">
    <h1 style="color:#14243A; font-size:2.7rem;
               font-weight:800; letter-spacing:2px;
               margin-bottom:8px;">
        REGIONAL SALES PULSE
    </h1>
    <p style="color:#2F527A; font-size:1rem;
              font-weight:700; letter-spacing:2px;
              margin-bottom:8px;">
        SALES PERFORMANCE AND PROFITABILITY ANALYTICS
    </p>
    <p style="color:#758397; font-size:0.9rem;">
        Interactive Business Intelligence Dashboard for Analyzing Sales and Trends,
        Product Profitability, Discount Impact, and Regional Performance
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="meta-line"><b>Data Source:</b> Sample - Superstore.csv'
    f' &nbsp;&nbsp; | &nbsp;&nbsp; <b>Displayed Period:</b> {min_date:%d-%m-%Y} to {max_date:%d-%m-%Y}'
    f' &nbsp;&nbsp; | &nbsp;&nbsp; <b>Selected Period:</b> {start_date:%d-%m-%Y} to {end_date:%d-%m-%Y}</div>',
    unsafe_allow_html=True
)

if filtered.empty:
    st.warning("No records match the selected filters. Please change the date range, region or category.")
    st.stop()

# --------------------------- KPI CALCULATIONS ---------------------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
total_records = len(filtered)
total_orders = filtered["Order ID"].nunique()

st.markdown('<div class="section-title">KEY PERFORMANCE INDICATORS</div>', unsafe_allow_html=True)

kpi_items = [
    ("TOTAL SALES", f"${total_sales:,.2f}"),
    ("TOTAL PROFIT", f"${total_profit:,.2f}"),
    ("PROFIT MARGIN", f"{profit_margin:.2f}%"),
    ("TOTAL RECORDS", f"{total_records:,}"),
    ("TOTAL ORDERS", f"{total_orders:,}")
]
cols = st.columns(5)
for col, (label, value) in zip(cols, kpi_items):
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True
        )

# --------------------------- CHART HELPERS ---------------------------
def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family="Arial", color=TEXT, size=11),
        margin=dict(l=18, r=18, t=55, b=35),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor=NAVY, font_color=WHITE),
    )
    fig.update_xaxes(showgrid=False, linecolor=PLATINUM, zerolinecolor=PLATINUM)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=PLATINUM)
    return fig

# --------------------------- ROW 1: TWO CHARTS ---------------------------
st.markdown('<div class="section-title">PRODUCT AND REGIONAL PERFORMANCE</div>', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    subcat = (
        filtered.groupby("Sub-Category", as_index=False)["Profit"]
        .sum().sort_values("Profit", ascending=True)
    )
    fig_sub = go.Figure()
    fig_sub.add_trace(go.Bar(
        x=subcat["Profit"], y=subcat["Sub-Category"], orientation="h",
        marker_color=[RED if value < 0 else PRIMARY for value in subcat["Profit"]],
        hovertemplate="%{y}<br>Profit: $%{x:,.2f}<extra></extra>"
    ))
    fig_sub.add_vline(x=0, line_dash="dash", line_color=MUTED)
    fig_sub.update_layout(title="Profit by Product Sub-Category",
                          xaxis_title="Total Profit ($)", yaxis_title="")
    chart_layout(fig_sub, 480)
    st.plotly_chart(fig_sub, use_container_width=True)

with right:
    region_summary = (
        filtered.groupby("Region", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )
    region_summary["Profit Margin"] = np.where(
        region_summary["Sales"] != 0,
        region_summary["Profit"] / region_summary["Sales"] * 100,
        0
    )
    fig_region = make_subplots(specs=[[{"secondary_y": True}]])
    fig_region.add_trace(go.Bar(
        x=region_summary["Region"], y=region_summary["Sales"],
        name="Sales", marker_color=PRIMARY,
        hovertemplate="%{x}<br>Sales: $%{y:,.2f}<extra></extra>"
    ), secondary_y=False)
    fig_region.add_trace(go.Scatter(
        x=region_summary["Region"], y=region_summary["Profit Margin"],
        name="Profit Margin", mode="lines+markers+text",
        text=[f"{v:.1f}%" for v in region_summary["Profit Margin"]],
        textposition="top center", line=dict(color=GOLD, width=3),
        marker=dict(size=9),
        hovertemplate="%{x}<br>Margin: %{y:.2f}%<extra></extra>"
    ), secondary_y=True)
    fig_region.update_layout(title="Regional Sales and Profit Margin",
                             barmode="group")
    fig_region.update_yaxes(title_text="Sales ($)", secondary_y=False)
    fig_region.update_yaxes(title_text="Profit Margin (%)", secondary_y=True)
    chart_layout(fig_region, 480)
    st.plotly_chart(fig_region, use_container_width=True)

# --------------------------- ROW 2: CUSTOMER + DISCOUNT ---------------------------
st.markdown('<div class="section-title">CUSTOMER AND DISCOUNT ANALYSIS</div>', unsafe_allow_html=True)
left2, right2 = st.columns(2)

with left2:
    segment_summary = (
        filtered.groupby("Segment", as_index=False)
        .agg(Sales=("Sales", "sum"))
        .sort_values("Sales", ascending=False)
    )
    segment_colors = {
        "Consumer": "#243B53",
        "Corporate": "#486581",
        "Home Office": "#5B9A9A"
    }
    fig_segment = go.Figure()
    fig_segment.add_trace(go.Bar(
        x=segment_summary["Segment"], y=segment_summary["Sales"],
        marker_color=[segment_colors.get(name, "#486581")
                      for name in segment_summary["Segment"]],
        text=[f"${value:,.0f}" for value in segment_summary["Sales"]],
        textposition="outside",
        hovertemplate="%{x}<br>Sales: $%{y:,.2f}<extra></extra>"
    ))
    fig_segment.update_layout(
        title="Sales by Customer Segment",
        xaxis_title="", yaxis_title="Total Sales ($)"
    )
    chart_layout(fig_segment, 390)
    st.plotly_chart(fig_segment, use_container_width=True)


with right2:
    # Calculate profit for each Order ID at each discount level
    order_discount_profit = (
        filtered.groupby(["Discount", "Order ID"], as_index=False)
        .agg(Order_Profit=("Profit", "sum"))
    )

    # Calculate average order profit at each discount level
    discount_summary = (
        order_discount_profit.groupby("Discount", as_index=False)
        .agg(
            Average_Profit=("Order_Profit", "mean"),
            Total_Profit=("Order_Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .sort_values("Discount")
    )

    # Create Discount Impact Chart
    fig_discount = make_subplots(
        specs=[[{"secondary_y": True}]]
    )

    fig_discount.add_trace(
        go.Bar(
            x=discount_summary["Discount"] * 100,
            y=discount_summary["Total_Profit"],
            name="Total Profit",
            marker_color=PRIMARY,
            customdata=discount_summary[["Orders"]].to_numpy(),
            hovertemplate=(
                "Discount: %{x:.0f}%"
                "<br>Total Profit: $%{y:,.2f}"
                "<br>Orders: %{customdata[0]}"
                "<extra></extra>"
            )
        ),
        secondary_y=False
    )

    fig_discount.add_trace(
        go.Scatter(
            x=discount_summary["Discount"] * 100,
            y=discount_summary["Average_Profit"],
            name="Average Profit per Order ID",
            mode="lines+markers",
            line=dict(color=GOLD, width=3),
            marker=dict(size=9, color=GOLD),
            hovertemplate=(
                "Discount: %{x:.0f}%"
                "<br>Average Profit per Order ID: $%{y:,.2f}"
                "<extra></extra>"
            )
        ),
        secondary_y=True
    )

    fig_discount.add_hline(
        y=0,
        line_dash="dash",
        line_color=RED
    )

    fig_discount.update_layout(
        title="Discount Level vs Average and Total Profit",
        template="plotly_white",
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=15, r=15, t=60, b=35)
    )

    fig_discount.update_xaxes(
        title_text="Discount Level (%)"
    )

    fig_discount.update_yaxes(
        title_text="Total Profit ($)",
        secondary_y=False
    )

    fig_discount.update_yaxes(
        title_text="Average Profit per Order ID($)",
        secondary_y=True
    )

    chart_layout(fig_discount, 390)

    st.plotly_chart(
        fig_discount,
        use_container_width=True
    )



# --------------------------- ROW 3: MONTHLY TREND + FORECAST ---------------------------
st.markdown('<div class="section-title">MONTHLY SALES TREND AND NEXT-MONTH ESTIMATE</div>', unsafe_allow_html=True)

# Use the same monthly grouping and three-model comparison as the notebook.
# PeriodIndex keeps the evaluation aligned with the notebook calculations.
monthly_sales = (
    filtered.groupby(filtered["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .sort_index()
)

forecast_value = None
forecast_date = None
forecast_wape = None
forecast_method = None
forecast_comparison = pd.DataFrame()

# A fair comparison of all three methods requires enough history for
# the 6-month moving average and the 12-month seasonal lag.
if len(monthly_sales) >= 18:
    forecast_3m = monthly_sales.shift(1).rolling(3).mean()
    forecast_6m = monthly_sales.shift(1).rolling(6).mean()
    seasonal_forecast = monthly_sales.shift(12)

    forecast_comparison = pd.DataFrame({
        "Actual Sales": monthly_sales,
        "3-Month MA": forecast_3m,
        "6-Month MA": forecast_6m,
        "Seasonal Naive": seasonal_forecast
    }).dropna().tail(12)

    if not forecast_comparison.empty:
        forecast_results = []
        actual = forecast_comparison["Actual Sales"]

        for method in ["3-Month MA", "6-Month MA", "Seasonal Naive"]:
            predicted = forecast_comparison[method]
            wape = (
                np.abs(actual - predicted).sum()
                / np.abs(actual).sum() * 100
                if np.abs(actual).sum() != 0 else np.nan
            )
            forecast_results.append({"Method": method, "WAPE": wape})

        forecast_results_df = pd.DataFrame(forecast_results).dropna()
        if not forecast_results_df.empty:
            best_forecast_row = forecast_results_df.loc[
                forecast_results_df["WAPE"].idxmin()
            ]
            forecast_method = str(best_forecast_row["Method"])
            forecast_wape = float(best_forecast_row["WAPE"])

            if forecast_method == "3-Month MA":
                forecast_value = float(monthly_sales.tail(3).mean())
            elif forecast_method == "6-Month MA":
                forecast_value = float(monthly_sales.tail(6).mean())
            else:
                forecast_value = float(monthly_sales.iloc[-12])

            forecast_date = (
                monthly_sales.index[-1].to_timestamp()
                + pd.offsets.MonthBegin(1)
            )

# Convert monthly PeriodIndex to timestamps for the chart.
monthly_chart_dates = monthly_sales.index.to_timestamp()

fig_month = go.Figure()
fig_month.add_trace(go.Scatter(
    x=monthly_chart_dates, y=monthly_sales.values,
    name="Actual Monthly Sales", mode="lines+markers",
    line=dict(color=PRIMARY, width=2.5), marker=dict(size=5),
    hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>"
))
if forecast_value is not None:
    fig_month.add_trace(go.Scatter(
        x=[monthly_chart_dates[-1], forecast_date],
        y=[monthly_sales.iloc[-1], forecast_value],
        name=f"Next-Month Estimate ({forecast_method})", mode="lines+markers",
        line=dict(color=GOLD, width=3, dash="dash"),
        marker=dict(size=9, symbol="diamond"),
        hovertemplate="%{x|%b %Y}<br>Estimated Sales: $%{y:,.2f}<extra></extra>"
    ))
fig_month.update_layout(
    title="Monthly Sales Trend with Best-Performing Forecast Method",
    xaxis_title="Month", yaxis_title="Sales ($)"
)
chart_layout(fig_month, 430)
st.plotly_chart(fig_month, use_container_width=True)

if forecast_value is not None:
    accuracy_text = (
        f"Best method: {forecast_method}. Historical back-test WAPE: {forecast_wape:.2f}% (last 12 comparable months)."
        if forecast_wape is not None else
        "Historical back-test accuracy could not be calculated for this selection."
    )
    forecast_col, method_col = st.columns([1.35, 2.65])
    with forecast_col:
        st.markdown(
            f"""
            <div style="background:#FFFFFF;border:1px solid #D5DDE6;
                        border-left:5px solid #2F527A;border-radius:12px;
                        padding:16px 18px;min-height:118px;">
                <div style="font-size:0.76rem;font-weight:700;letter-spacing:1px;
                            color:#758397;">NEXT MONTH SALES ESTIMATE</div>
                <div style="font-size:1.85rem;font-weight:800;color:#14243A;
                            margin-top:7px;">${forecast_value:,.2f}</div>
                <div style="font-size:0.82rem;color:#486581;margin-top:3px;">
                    {forecast_date:%B %Y}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with method_col:
        st.markdown(f"**Best forecast method: {forecast_method}**")
        st.caption(
            "Selected from 3-month moving average, 6-month moving average and Seasonal Naive methods. "
            + accuracy_text
        )
        st.caption("Forecast is an estimate based on historical sales patterns, not a guarantee.")
else:
    st.info(
         "The three-method forecast comparison needs at least 18 monthly observations. "
        "Widen the selected date range to enable the comparison and next-month estimate."
    )


# --------------------------- BUSINESS INSIGHTS ---------------------------

# All calculations use the currently filtered dataset.
# Insights and recommendations update automatically when filters change.

# 1. REGIONAL PERFORMANCE
region_summary = (
    filtered.groupby("Region", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

region_summary["Profit Margin"] = np.where(
    region_summary["Sales"] != 0,
    region_summary["Profit"] / region_summary["Sales"] * 100,
    0
)

highest_sales_region = region_summary.loc[
    region_summary["Sales"].idxmax()
]

highest_profit_region = region_summary.loc[
    region_summary["Profit"].idxmax()
]

lowest_margin_region = region_summary.loc[
    region_summary["Profit Margin"].idxmin()
]


# 2. ANNUAL SALES TREND
annual_sales = (
    filtered.assign(Year=filtered["Order Date"].dt.year)
    .groupby("Year")["Sales"]
    .sum()
    .sort_index()
)

annual_values_text = "; ".join(
    f"{int(year)}: ${value:,.2f}"
    for year, value in annual_sales.items()
)
annual_growth_text = []
if len(annual_sales) >= 2:
    annual_growth_series = annual_sales.pct_change() * 100
    annual_growth_text = [
        f"{int(year)}: {growth:+.2f}%"
        for year, growth in annual_growth_series.dropna().items()
    ]

if len(annual_sales) >= 2:

    first_year = annual_sales.index[0]
    latest_year = annual_sales.index[-1]

    first_year_sales = float(annual_sales.iloc[0])
    latest_year_sales = float(annual_sales.iloc[-1])

    sales_change = latest_year_sales - first_year_sales

    sales_growth = (
        sales_change / abs(first_year_sales) * 100
        if first_year_sales != 0 else None
    )

else:
    first_year = None
    latest_year = None
    first_year_sales = None
    latest_year_sales = None
    sales_change = None
    sales_growth = None


# 3. CATEGORY AND SUB-CATEGORY PROFITABILITY
category_summary = (
    filtered.groupby("Category", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

category_summary["Profit Margin"] = np.where(
    category_summary["Sales"] != 0,
    category_summary["Profit"] / category_summary["Sales"] * 100,
    0
)

best_profit_category = category_summary.loc[
    category_summary["Profit"].idxmax()
]

subcategory_summary = (
    filtered.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values()
)

loss_items = subcategory_summary[subcategory_summary < 0]


# 4. DISCOUNT IMPACT ON PROFITABILITY

# Correlation between discount and profit using filtered records.
discount_correlation = filtered["Discount"].corr(
    filtered["Profit"]
)

# Calculate profit at order level for each discount level.
order_discount_data = (
    filtered.groupby(
        ["Order ID", "Discount"],
        as_index=False
    )
    .agg(
        Order_Profit=("Profit", "sum")
    )
)

order_discount_summary = (
    order_discount_data.groupby("Discount", as_index=False)
    .agg(
        Average_Order_Profit=("Order_Profit", "mean"),
        Number_of_Orders=("Order ID", "nunique")
    )
    .sort_values("Discount")
)

negative_discount = order_discount_summary[
    order_discount_summary["Average_Order_Profit"] < 0
]

if not negative_discount.empty:

    first_negative_discount = float(
        negative_discount["Discount"].min() * 100
    )

    negative_discount_orders = int(
        order_discount_data[
            order_discount_data["Discount"]
            >= negative_discount["Discount"].min()
        ]["Order ID"].nunique()
    )

else:
    first_negative_discount = None
    negative_discount_orders = 0


# 5. CUSTOMER SEGMENT PERFORMANCE
segment_summary = (
    filtered.groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Sales", ascending=False)
)

leading_segment = segment_summary.iloc[0]
leading_segment_name = str(segment_summary.index[0])

highest_profit_segment = segment_summary["Profit"].idxmax()


# 6. FORECAST PERFORMANCE
# forecast_wape and forecast_method are calculated earlier
# in the existing Seasonal Naive forecast section.

insights = []


# INSIGHT 1: REGIONAL PERFORMANCE
insights.append(
    f"<strong>1. Regional Performance:</strong> "
    f"{escape(str(highest_sales_region['Region']))} recorded the highest sales "
    f"(${highest_sales_region['Sales']:,.2f}), while "
    f"{escape(str(highest_profit_region['Region']))} generated the highest profit "
    f"(${highest_profit_region['Profit']:,.2f}) with a profit margin of "
    f"{(highest_profit_region['Profit'] / highest_profit_region['Sales'] * 100) if highest_profit_region['Sales'] else 0:.2f}%. "
    f"{escape(str(lowest_margin_region['Region']))} recorded the lowest "
    f"profit margin ({lowest_margin_region['Profit Margin']:.2f}%), "
    f"indicating an area requiring profitability improvement."
)


# INSIGHT 2: YEAR-WISE SALES TREND
if len(annual_sales) >= 2:
    growth_details = (
        "; year-on-year growth: " + ", ".join(annual_growth_text)
        if annual_growth_text else ""
    )
    insights.append(
        f"<strong>2. Sales Trend:</strong> Annual sales by year were "
        f"{annual_values_text}{growth_details}. "
        f"This shows the actual year-by-year sales movement in the selected data."
    )
elif len(annual_sales) == 1:
    insights.append(
        f"<strong>2. Sales Trend:</strong> Sales for {int(annual_sales.index[0])} "
        f"were ${annual_sales.iloc[0]:,.2f}. At least two years are required "
        f"to calculate year-on-year growth."
    )
else:
    insights.append(
        "<strong>2. Sales Trend:</strong> No annual sales data is available "
        "for the current selection."
    )


# INSIGHT 3: CATEGORY AND SUB-CATEGORY PROFITABILITY
if not loss_items.empty:

    worst_subcategories = loss_items.head(3)

    loss_details = ", ".join(
        f"{escape(str(name))} (${value:,.2f})"
        for name, value in worst_subcategories.items()
    )

    combined_loss = abs(float(loss_items.sum()))

    insights.append(
        f"<strong>3. Category and Sub-category Profitability:</strong> "
        f"{escape(str(best_profit_category['Category']))} generated the highest "
        f"category profit (${best_profit_category['Profit']:,.2f}). "
        f"{len(loss_items)} sub-categories recorded negative profit. "
        f"The largest losses were recorded by {loss_details}. "
        f"Combined sub-category losses total ${combined_loss:,.2f}."
    )

else:

    insights.append(
        f"<strong>3. Category and Sub-category Profitability:</strong> "
        f"{escape(str(best_profit_category['Category']))} generated the highest "
        f"category profit (${best_profit_category['Profit']:,.2f}). "
        f"All sub-categories recorded non-negative total profit "
        f"under the selected filters."
    )


# INSIGHT 4: DISCOUNT IMPACT
if pd.notna(discount_correlation):

    correlation_text = f"{discount_correlation:.3f}"

else:

    correlation_text = "not available"


if first_negative_discount is not None:

    discount_group = order_discount_summary[
        order_discount_summary["Discount"]
        == negative_discount["Discount"].min()
    ].iloc[0]

    insights.append(
        f"<strong>4. Discount Impact on Profitability:</strong> "
        f"Discount and profit showed a correlation of {correlation_text}. "
        f"Average order profit remained "
        f"{'positive' if discount_group['Average_Order_Profit'] >= 0 else 'negative'} "
        f"at the {first_negative_discount:.0f}% discount level, with an average "
        f"of ${discount_group['Average_Order_Profit']:,.2f}. "
        f"This discount group contained "
        f"{int(discount_group['Number_of_Orders']):,} orders. "
        f"Average order profit becomes negative at this and other observed "
        f"discount levels. This indicates an association, not causation."
    )

else:

    insights.append(
        f"<strong>4. Discount Impact on Profitability:</strong> "
        f"Discount and profit showed a correlation of {correlation_text}. "
        f"Average order profit remained non-negative across all observed "
        f"discount levels in the current selection."
    )


# INSIGHT 5: CUSTOMER SEGMENT AND FORECAST PERFORMANCE
if forecast_wape is not None:

    forecast_text = (
        f"The {escape(str(forecast_method))} method achieved the lowest "
        f"WAPE among the three tested forecasting methods "
        f"({forecast_wape:.2f}%)."
    )

else:

    forecast_text = (
        "Forecast accuracy could not be compared for the current "
        "date selection because at least 18 monthly observations "
        "are required for all three methods."
    )

insights.append(
    f"<strong>5. Customer Segment and Forecast Performance:</strong> "
    f"{escape(leading_segment_name)} was the strongest customer segment "
    f"in sales, generating ${leading_segment['Sales']:,.2f} in sales "
    f"and ${leading_segment['Profit']:,.2f} in profit. "
    f"{escape(str(highest_profit_segment))} generated the highest "
    f"segment profit. {forecast_text}"
)


# --------------------------- DISPLAY BUSINESS INSIGHTS ---------------------------

insight_title_col, insight_dropdown_col = st.columns(
    [5.0, 0.45],
    vertical_alignment="center"
)

with insight_title_col:
    st.markdown(
        '<div class="section-title">BUSINESS INSIGHTS</div>',
        unsafe_allow_html=True
    )

if "show_business_insights" not in st.session_state:
    st.session_state.show_business_insights = True

with insight_dropdown_col:
    if st.button(
        "⌃" if st.session_state.show_business_insights else "⌄",
        key="toggle_business_insights",
        help="Hide or show the five business insights",
        use_container_width=True,
    ):
        st.session_state.show_business_insights = (
            not st.session_state.show_business_insights
        )

if st.session_state.show_business_insights:

    st.caption(
        "The following five insights are based on the currently selected "
        "date range, region, product category, sub-category, customer segment "
        "and shipping mode."
    )

    for insight in insights:

        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E1E7EF;'
            f'border-radius:8px;padding:10px 14px;margin:6px 0;'
            f'color:#26364A;font-size:0.92rem;line-height:1.5;">'
            f'{insight}</div>',
            unsafe_allow_html=True
        )


# --------------------------- BUSINESS RECOMMENDATIONS ---------------------------

recommendations = []


# RECOMMENDATION 1: REGIONAL PROFITABILITY
recommendations.append(
    f"<strong>1. Improve {escape(str(lowest_margin_region['Region']))} "
    f"Region Profitability:</strong> Review discounting strategies, "
    f"product mix, shipping costs and loss-making products in "
    f"{escape(str(lowest_margin_region['Region']))}. "
    f"Its current profit margin is "
    f"{lowest_margin_region['Profit Margin']:.2f}%. "
    f"Monitor profit margin alongside sales to improve regional performance."
)


# RECOMMENDATION 2: SALES TRENDS
if len(annual_sales) >= 2:

    recommendations.append(
        f"<strong>2. Plan Around Sales Trends:</strong> "
        f"Use historical sales patterns from {first_year} to {latest_year} "
        f"to guide inventory planning, staffing and promotional activities. "
        f"Sales changed by "
        f"{sales_growth:+.2f}% from {first_year} to {latest_year}. "
        f"{'Review the reasons for the decline and adjust inventory and promotions.' if sales_growth < 0 else 'Use the growth pattern to guide inventory, staffing and promotional planning.'}"
    )

else:

    recommendations.append(
        "<strong>2. Plan Around Sales Trends:</strong> "
        "Continue monitoring monthly and annual sales patterns to guide "
        "inventory planning, staffing and promotional activities."
    )


# RECOMMENDATION 3: PRODUCT PROFITABILITY
if not loss_items.empty:

    recommendations.append(
        f"<strong>3. Strengthen Product Profitability:</strong> "
        f"Maintain the contribution from "
        f"{escape(str(best_profit_category['Category']))}, which generated "
        f"${best_profit_category['Profit']:,.2f} in profit, while reviewing "
        f"pricing, costs and operational strategies for loss-making "
        f"sub-categories, particularly {', '.join(escape(str(x)) for x in loss_items.index)}."
    )

else:

    recommendations.append(
        f"<strong>3. Strengthen Product Profitability:</strong> "
        f"Maintain the strong contribution from "
        f"{escape(str(best_profit_category['Category']))} and regularly "
        f"monitor product pricing, costs and profitability."
    )


# RECOMMENDATION 4: DISCOUNT CONTROL
if first_negative_discount is not None:

    recommendations.append(
        f"<strong>4. Implement Discount Control Strategies:</strong> "
        f"Introduce margin-based discount limits and carefully evaluate "
        f"discount levels starting at {first_negative_discount:.0f}%, "
        f"where average order profit becomes negative. "
        f"Evaluate promotional success based on profitability "
        f"rather than sales volume alone."
    )

else:

    recommendations.append(
        "<strong>4. Implement Discount Control Strategies:</strong> "
        "Continue monitoring average order profit across discount levels. "
        "Evaluate promotional success based on profitability rather "
        "than sales volume alone."
    )


# RECOMMENDATION 5: FORECASTING
if forecast_wape is not None:

    recommendations.append(
        f"<strong>5. Use Forecasting for Better Business Planning:</strong> "
        f"Use the {escape(str(forecast_method))} method as a reference for sales planning. "
        f"It achieved the lowest WAPE ({forecast_wape:.2f}%) among the three tested methods "
        f"for the current filtered period. Compare actual sales with "
        f"forecasted sales regularly, monitor forecast errors and "
        f"reassess performance as new monthly data becomes available."
    )

else:

    recommendations.append(
        "<strong>5. Use Forecasting for Better Business Planning:</strong> "
        "Compare the 3-month moving average, 6-month moving average and "
        "Seasonal Naive methods when sufficient monthly data is available. "
        "Monitor forecast errors before using estimates for business decisions."
    )


# --------------------------- DISPLAY BUSINESS RECOMMENDATIONS ---------------------------

recommendation_title_col, recommendation_dropdown_col = st.columns(
    [5.0, 0.45],
    vertical_alignment="center"
)

with recommendation_title_col:
    st.markdown(
        '<div class="section-title">BUSINESS RECOMMENDATIONS</div>',
        unsafe_allow_html=True
    )

if "show_business_recommendations" not in st.session_state:
    st.session_state.show_business_recommendations = True

with recommendation_dropdown_col:
    if st.button(
        "⌃" if st.session_state.show_business_recommendations else "⌄",
        key="toggle_business_recommendations",
        help="Hide or show the five business recommendations",
        use_container_width=True,
    ):
        st.session_state.show_business_recommendations = (
            not st.session_state.show_business_recommendations
        )

if st.session_state.show_business_recommendations:

    for recommendation in recommendations:

        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E1E7EF;'
            f'border-radius:8px;padding:10px 14px;margin:6px 0;'
            f'color:#26364A;font-size:0.92rem;line-height:1.5;">'
            f'{recommendation}</div>',
            unsafe_allow_html=True
        )


# --------------------------- PERFORMANCE SUMMARY TABLES ---------------------------

# --------------------------- PERFORMANCE SUMMARY TABLES ---------------------------
st.markdown('<div class="section-title">PERFORMANCE SUMMARY</div>', unsafe_allow_html=True)
tab_category, tab_region, tab_subcategory = st.tabs(
    ["Category Summary", "Region Summary", "Sub-Category Summary"]
)

with tab_category:
    cat_table = (
        filtered.groupby("Category", as_index=False)
        .agg(Records=("Sales", "size"), Sales=("Sales", "sum"),
             Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    )
    cat_table["Profit Margin (%)"] = np.where(
        cat_table["Sales"] != 0, cat_table["Profit"] / cat_table["Sales"] * 100, 0
    )
    st.dataframe(
        cat_table.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}",
            "Profit Margin (%)": "{:.2f}%"
        }),
        use_container_width=True, hide_index=True
    )

with tab_region:
    region_table = (
        filtered.groupby("Region", as_index=False)
        .agg(Records=("Sales", "size"), Sales=("Sales", "sum"),
             Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    )
    region_table["Profit Margin (%)"] = np.where(
        region_table["Sales"] != 0, region_table["Profit"] / region_table["Sales"] * 100, 0
    )
    st.dataframe(
        region_table.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}",
            "Profit Margin (%)": "{:.2f}%"
        }),
        use_container_width=True, hide_index=True
    )

with tab_subcategory:
    sub_table = (
        filtered.groupby("Sub-Category", as_index=False)
        .agg(Records=("Sales", "size"), Sales=("Sales", "sum"),
             Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .sort_values("Profit")
    )
    sub_table["Profit Margin (%)"] = np.where(
        sub_table["Sales"] != 0, sub_table["Profit"] / sub_table["Sales"] * 100, 0
    )
    st.dataframe(
        sub_table.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}",
            "Profit Margin (%)": "{:.2f}%"
        }),
        use_container_width=True, hide_index=True
    )

# --------------------------- DISCOUNT ANALYSIS TABLE ---------------------------
with st.expander("View Detailed Discount Analysis", expanded=False):
    discount_table = discount_summary.copy()
    discount_table["Discount Level (%)"] = discount_table["Discount"] * 100
    discount_table = discount_table[
        ["Discount Level (%)", "Orders", "Average_Profit", "Total_Profit"]
    ].rename(columns={
        "Average_Profit": "Average Profit ($)",
        "Total_Profit": "Total Profit ($)"
    })
    st.dataframe(
        discount_table.style.format({
            "Discount Level (%)": "{:.0f}%",
            "Average Profit ($)": "${:,.2f}",
            "Total Profit ($)": "${:,.2f}"
        }),
        use_container_width=True, hide_index=True
    )

# --------------------------- FOOTER ---------------------------
st.markdown("---")
st.markdown(
    f'<div style="text-align:center;color:{MUTED};font-size:0.80rem;">'
    f'Data source: Sample - Superstore.csv'
    f' &nbsp;|&nbsp; Profit Margin = Total Profit ÷ Total Sales × 100'
    f'</div>',
    unsafe_allow_html=True
)
