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
    background: transparent;
    height: 2rem;
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
    discount_summary = (
        filtered.groupby("Discount", as_index=False)
        .agg(
            Average_Profit=("Profit", "mean"),
            Total_Profit=("Profit", "sum"),
            Records=("Profit", "size")
        ).sort_values("Discount")
    )
    fig_discount = make_subplots(specs=[[{"secondary_y": True}]])
    fig_discount.add_trace(go.Bar(
        x=discount_summary["Discount"] * 100,
        y=discount_summary["Total_Profit"],
        name="Total Profit", marker_color="#243B53",
        customdata=discount_summary[["Records"]].to_numpy(),
        hovertemplate="Discount: %{x:.0f}%<br>Total Profit: $%{y:,.2f}"
                      "<br>Records: %{customdata[0]}<extra></extra>"
    ), secondary_y=False)
    fig_discount.add_trace(go.Scatter(
        x=discount_summary["Discount"] * 100,
        y=discount_summary["Average_Profit"],
        name="Average Profit", mode="lines+markers",
        line=dict(color="#2A7F78", width=3), marker=dict(size=8, color="#2A7F78"),
        hovertemplate="Discount: %{x:.0f}%<br>Average Profit: $%{y:,.2f}<extra></extra>"
    ), secondary_y=True)
    fig_discount.add_hline(y=0, line_dash="dash", line_color="#A65D68")
    fig_discount.update_layout(title="Discount Level vs Average and Total Profit")
    fig_discount.update_xaxes(title_text="Discount Level (%)")
    fig_discount.update_yaxes(title_text="Total Profit ($)", secondary_y=False)
    fig_discount.update_yaxes(title_text="Average Profit per Record ($)", secondary_y=True)
    chart_layout(fig_discount, 390)
    st.plotly_chart(fig_discount, use_container_width=True)

# --------------------------- ROW 3: MONTHLY TREND + FORECAST ---------------------------
st.markdown('<div class="section-title">MONTHLY SALES TREND AND NEXT-MONTH ESTIMATE</div>', unsafe_allow_html=True)

monthly_sales = (
    filtered.set_index("Order Date")["Sales"]
    .resample("MS").sum().sort_index()
)

forecast_value = None
forecast_date = None
forecast_wape = None
forecast_method = "Seasonal Naive"

if len(monthly_sales) >= 13:
    forecast_date = monthly_sales.index[-1] + pd.offsets.MonthBegin(1)
    reference_date = forecast_date - pd.DateOffset(years=1)
    if reference_date in monthly_sales.index:
        forecast_value = float(monthly_sales.loc[reference_date])

    backtest = pd.DataFrame({
        "Actual": monthly_sales,
        "Predicted": monthly_sales.shift(12)
    }).dropna().tail(12)
    if not backtest.empty and backtest["Actual"].abs().sum() != 0:
        forecast_wape = (
            (backtest["Actual"] - backtest["Predicted"]).abs().sum()
            / backtest["Actual"].abs().sum()
        ) * 100

fig_month = go.Figure()
fig_month.add_trace(go.Scatter(
    x=monthly_sales.index, y=monthly_sales.values,
    name="Actual Monthly Sales", mode="lines+markers",
    line=dict(color=PRIMARY, width=2.5), marker=dict(size=5),
    hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>"
))
if forecast_value is not None:
    fig_month.add_trace(go.Scatter(
        x=[monthly_sales.index[-1], forecast_date],
        y=[monthly_sales.iloc[-1], forecast_value],
        name="Next-Month Estimate", mode="lines+markers",
        line=dict(color=GOLD, width=3, dash="dash"),
        marker=dict(size=9, symbol="diamond"),
        hovertemplate="%{x|%b %Y}<br>Estimated Sales: $%{y:,.2f}<extra></extra>"
    ))
fig_month.update_layout(
    title="Monthly Sales Trend with Seasonal Naive Forecast",
    xaxis_title="Month", yaxis_title="Sales ($)"
)
chart_layout(fig_month, 430)
st.plotly_chart(fig_month, use_container_width=True)

if forecast_value is not None:
    accuracy_text = (
        f"Historical back-test WAPE: {forecast_wape:.2f}% (last 12 comparable months)."
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
        st.markdown("**Forecast method: Seasonal Naive**")
        st.caption(
            "Uses sales from the same month in the previous year. "
            + accuracy_text
        )
        st.caption("Forecast is an estimate based on historical seasonal sales patterns, not a guarantee.")
else:
    st.info(
        "The Seasonal Naive estimate needs at least 13 monthly observations and the matching "
        "month from the previous year. Widen the selected date range to enable the estimate."
    )

# --------------------------- BUSINESS INSIGHTS ---------------------------
# Build all findings from the currently filtered records; no sample values are hard-coded.
category_summary = (
    filtered.groupby("Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)
category_summary["Profit Margin"] = np.where(
    category_summary["Sales"] != 0,
    category_summary["Profit"] / category_summary["Sales"] * 100,
    0
)

region_summary = (
    filtered.groupby("Region", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)
region_summary["Profit Margin"] = np.where(
    region_summary["Sales"] != 0,
    region_summary["Profit"] / region_summary["Sales"] * 100,
    0
)

segment_summary = (
    filtered.groupby("Segment")
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
)

loss_subcats = (
    filtered.groupby("Sub-Category")["Profit"].sum().sort_values()
)
loss_items = loss_subcats[loss_subcats < 0]

negative_discount = discount_summary[discount_summary["Average_Profit"] < 0]

insights = []

# 1. Product-level profitability exposure.
if not loss_items.empty:
    worst_name = str(loss_items.index[0])
    worst_value = float(loss_items.iloc[0])
    combined_loss = float(abs(loss_items.sum()))
    insights.append(
        f"<strong>Sub-Category Profitability:</strong> "
        f"{len(loss_items)} of {len(loss_subcats)} sub-categories are loss-making. "
        f"{worst_name} records the largest loss (${abs(worst_value):,.2f}); "
        f"combined losses total ${combined_loss:,.2f}."
    )
else:
    insights.append(
        "<strong>Sub-Category Profitability:</strong> "
        "All sub-categories generate non-negative total profit under the selected filters."
    )

# 2. Regional scale and margin are shown separately to avoid conflating them.
highest_sales_region = None
lowest_margin_region = None
if not region_summary.empty:
    highest_sales_region = region_summary.loc[region_summary["Sales"].idxmax()]
    lowest_margin_region = region_summary.loc[region_summary["Profit Margin"].idxmin()]
    insights.append(
        f"<strong>Regional Performance:</strong> "
        f"{highest_sales_region['Region']} contributes the highest sales "
        f"(${highest_sales_region['Sales']:,.2f}), while "
        f"{lowest_margin_region['Region']} has the lowest profit margin "
        f"({lowest_margin_region['Profit Margin']:.2f}%)."
    )
else:
    insights.append(
        "<strong>Regional Performance:</strong> No regional comparison is available "
        "for the current filter selection."
    )

# 3. Category-level profit and margin.
best_profit_category = None
lowest_margin_category = None
if not category_summary.empty:
    best_profit_category = category_summary.loc[category_summary["Profit"].idxmax()]
    lowest_margin_category = category_summary.loc[category_summary["Profit Margin"].idxmin()]
    insights.append(
        f"<strong>Category Profitability:</strong> "
        f"{best_profit_category['Category']} generates the highest total profit "
        f"(${best_profit_category['Profit']:,.2f}); "
        f"{lowest_margin_category['Category']} has the lowest margin "
        f"({lowest_margin_category['Profit Margin']:.2f}%)."
    )
else:
    insights.append(
        "<strong>Category Profitability:</strong> No category comparison is available "
        "for the current filter selection."
    )

# 4. Discount analysis describes an observed association, not causation.
if not negative_discount.empty:
    first_negative_discount = float(negative_discount["Discount"].min() * 100)
    insights.append(
        f"<strong>Discount Impact:</strong> Average profit per record is negative "
        f"at observed discount levels starting at {first_negative_discount:.0f}%. "
        "This is an observed association and does not establish causation."
    )
else:
    first_negative_discount = None
    insights.append(
        "<strong>Discount Impact:</strong> Average profit per record remains "
        "non-negative across all discount levels in the current selection."
    )

# 5. Customer segment contribution, with sales and profit both reported.
if not segment_summary.empty:
    leading_segment = segment_summary.iloc[0]
    insights.append(
        f"<strong>Customer Segment Contribution:</strong> "
        f"{segment_summary.index[0]} leads sales with "
        f"${leading_segment['Sales']:,.2f} and contributes "
        f"${leading_segment['Profit']:,.2f} in profit."
    )
else:
    insights.append(
        "<strong>Customer Segment Contribution:</strong> No segment comparison is "
        "available for the current filter selection."
    )

insight_title_col, insight_dropdown_col = st.columns(
    [5.0, 0.45], vertical_alignment="center"
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
        st.session_state.show_business_insights = not st.session_state.show_business_insights

if st.session_state.show_business_insights:
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

if not loss_items.empty:
    recommendations.append(
        f"<strong>Address loss-making products:</strong> Review pricing, product "
        f"costs, shipping expense and discount policy for {', '.join(map(str, loss_items.index))}. "
        f"Prioritise {loss_items.index[0]}, which has the largest loss."
    )
else:
    recommendations.append(
        "<strong>Protect product profitability:</strong> Maintain regular sub-category "
        "profitability reviews and investigate any movement into negative profit."
    )

if first_negative_discount is not None:
    recommendations.append(
        f"<strong>Review high-discount transactions:</strong> Examine discounts of "
        f"{first_negative_discount:.0f}% and above, and assess their effect on profit "
        "before expanding promotional offers."
    )
else:
    recommendations.append(
        "<strong>Measure promotion effectiveness:</strong> Evaluate discounts using "
        "incremental sales and profit, rather than sales volume alone."
    )

if lowest_margin_category is not None:
    recommendations.append(
        f"<strong>Improve category margins:</strong> Review product mix, supplier "
        f"costs and discount levels in {lowest_margin_category['Category']}, "
        f"currently the lowest-margin category ({lowest_margin_category['Profit Margin']:.2f}%)."
    )
else:
    recommendations.append(
        "<strong>Monitor category economics:</strong> Compare category-level sales, "
        "profit and margin before changing prices or promotional plans."
    )

if lowest_margin_region is not None and highest_sales_region is not None:
    recommendations.append(
        f"<strong>Investigate regional margin gaps:</strong> Examine cost, product "
        f"and discount mix in {lowest_margin_region['Region']}; compare its practices "
        f"with the highest-sales region, {highest_sales_region['Region']}."
    )
else:
    recommendations.append(
        "<strong>Review regional performance:</strong> Track sales and profit margin "
        "together to identify regions that need operational support."
    )

if not segment_summary.empty:
    recommendations.append(
        "<strong>Refine segment-level targeting:</strong> Tailor campaigns to each "
        "customer segment and monitor both sales and profit to ensure growth remains profitable."
    )
else:
    recommendations.append(
        "<strong>Strengthen customer analysis:</strong> Track segment-level sales, "
        "profit and margin to guide targeted campaigns."
    )

recommendation_title_col, recommendation_dropdown_col = st.columns(
    [5.0, 0.45], vertical_alignment="center"
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
        st.session_state.show_business_recommendations = not st.session_state.show_business_recommendations

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
        ["Discount Level (%)", "Records", "Average_Profit", "Total_Profit"]
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
