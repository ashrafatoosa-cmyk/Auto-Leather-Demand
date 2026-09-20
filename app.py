import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

from PIL import Image

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_png_path = os.path.join(base_dir, "assets", "logo.png")
logo_avif_path = os.path.join(base_dir, "assets", "logo-small-2.avif")
logo_path = logo_png_path if os.path.exists(logo_png_path) else logo_avif_path

page_icon = "🏎️"
if os.path.exists(logo_path):
    try:
        page_icon = Image.open(logo_path)
    except Exception:
        page_icon = "🏎️"

st.set_page_config(
    page_title="AutoLeather Intelligence Factory Demand & Upholstery DSS",
    page_icon=page_icon,
    layout="wide"
)

# Inject Custom CSS for Dark Executive Appearance
st.markdown("""
<style>
    /* Header layout */
    .header-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }
    .header-logo {
        height: 44px;
        width: auto;
        object-fit: contain;
        flex-shrink: 0;
    }
    .header-text h1 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        line-height: 1.2 !important;
    }
    .header-text p {
        color: #94A3B8 !important;
        font-size: 0.95rem !important;
        margin: 3px 0 0 0 !important;
        padding: 0 !important;
    }

    /* Metric Tiles CSS */
    .metric-tile {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #38BDF8;
    }
    .metric-subtext {
        font-size: 0.8rem;
        color: #CBD5E1;
        margin-top: 8px;
    }

    @media (max-width: 768px) {
        .header-container {
            gap: 10px !important;
            margin-bottom: 8px !important;
        }
        .header-logo {
            height: 30px !important;
            max-width: 60px !important;
        }
        .header-text h1 {
            font-size: 1.15rem !important;
            line-height: 1.25 !important;
        }
        .header-text p {
            font-size: 0.74rem !important;
            margin-top: 2px !important;
        }
        h1, .stHeading h1, [data-testid="stHeading"] h1 {
            font-size: 1.35rem !important;
            line-height: 1.3 !important;
        }
        h2, .stHeading h2, [data-testid="stHeading"] h2,
        h3, .stHeading h3, [data-testid="stHeading"] h3 {
            font-size: 1.1rem !important;
            line-height: 1.3 !important;
            margin-top: 12px !important;
            margin-bottom: 6px !important;
        }
        p, .stMarkdown p, span {
            font-size: 0.84rem !important;
        }
        .metric-tile {
            padding: 10px 8px !important;
            margin-bottom: 8px !important;
        }
        .metric-label {
            font-size: 0.65rem !important;
            margin-bottom: 4px !important;
        }
        .metric-value {
            font-size: 1.35rem !important;
        }
        .metric-subtext {
            font-size: 0.72rem !important;
            margin-top: 4px !important;
        }
        button[data-baseweb="tab"] {
            font-size: 0.82rem !important;
            padding: 6px 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

if os.path.exists(logo_path):
    try:
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        mime = "image/png" if logo_path.endswith(".png") else "image/avif"
        st.markdown(f"""
        <div class="header-container">
            <img src="data:{mime};base64,{logo_b64}" class="header-logo" alt="Auto Leathers Logo" />
            <div class="header-text">
                <h1>AutoLeather Intelligence Factory Demand & Upholstery DSS</h1>
                <p>Automotive Interior Cutting & Sewing Operations | OEM & Aftermarket Horizon.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.image(logo_path, width=55)
        st.title("AutoLeather Intelligence Factory Demand & Upholstery DSS")
        st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-top: -15px;'>Automotive Interior Cutting & Sewing Operations | OEM & Aftermarket Horizon.</p>", unsafe_allow_html=True)
else:
    st.title("AutoLeather Intelligence Factory Demand & Upholstery DSS")
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-top: -15px;'>Automotive Interior Cutting & Sewing Operations | OEM & Aftermarket Horizon.</p>", unsafe_allow_html=True)

# Load Data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df_compare = pd.read_csv(os.path.join(base_dir, "dashboard_forecast_comparison.csv"))
    
    # Hardcoded 12-month 52-week dataset to bypass all CSV caching issues
    future_data = {'Forecast_Week': ['2026-06-01', '2026-06-08', '2026-06-15', '2026-06-22', '2026-06-29', '2026-07-06', '2026-07-13', '2026-07-20', '2026-07-27', '2026-08-03', '2026-08-10', '2026-08-17', '2026-08-24', '2026-08-31', '2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28', '2026-10-05', '2026-10-12', '2026-10-19', '2026-10-26', '2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23', '2026-11-30', '2026-12-07', '2026-12-14', '2026-12-21', '2026-12-28', '2027-01-04', '2027-01-11', '2027-01-18', '2027-01-25', '2027-02-01', '2027-02-08', '2027-02-15', '2027-02-22', '2027-03-01', '2027-03-08', '2027-03-15', '2027-03-22', '2027-03-29', '2027-04-05', '2027-04-12', '2027-04-19', '2027-04-26', '2027-05-03', '2027-05-10', '2027-05-17', '2027-05-24', '2027-05-31'], 'Projected_Seat_Covers': [46, 45, 49, 52, 47, 48, 54, 52, 49, 53, 50, 51, 53, 47, 47, 51, 50, 54, 50, 48, 57, 51, 52, 47, 49, 51, 47, 51, 47, 48, 47, 54, 48, 44, 50, 44, 48, 41, 43, 48, 50, 49, 48, 48, 45, 48, 49, 54, 53, 47, 54, 53, 53]}
    df_future = pd.DataFrame(future_data)
    
    df_brand = pd.read_csv(os.path.join(base_dir, "dashboard_brand_insights.csv"))
    df_color = pd.read_csv(os.path.join(base_dir, "dashboard_color_insights.csv"))
    return df_compare, df_future, df_brand, df_color

try:
    df_compare, df_future, df_brand, df_color = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 1. Top KPI Cards
st.subheader("Key Performance Indicators")
st.markdown('<div style="border-top: 3px solid #38BDF8; margin-top: -10px; margin-bottom: 20px; width: 100%;"></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_projected_demand = df_future['Projected_Seat_Covers'].head(4).sum()
top_brand = df_brand.iloc[0]
top_color = df_color.iloc[0]

def metric_html(label, value, subtext=""):
    return f"""
    <div class="metric-tile">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """

col1.markdown(metric_html("✂️ Next Month Target", f"{total_projected_demand}", "Seat sets to cut/stitch"), unsafe_allow_html=True)
col2.markdown(metric_html("🚘 Top Vehicle Make", top_brand['Brand'], "Leading OEM Inflow"), unsafe_allow_html=True)
col3.markdown(metric_html("💺 Leather Hide Preference", top_color['Colour'], "Perforated / Smooth Hide"), unsafe_allow_html=True)
col4.markdown(metric_html("⚙️ Forecast Model", "LSTM Neural Net", "Production Planner Engine"), unsafe_allow_html=True)

# 2. Main Visuals
st.subheader("Forecast Comparison")

view_mode = st.radio("Forecast Granularity:", ["Weekly View", "Monthly View"], index=1, horizontal=True)

df_compare['Date'] = pd.to_datetime(df_compare['Date'])

if view_mode == "Weekly View":
    plot_df = df_compare
    mode_str = 'lines'
    
    st.markdown("<p style='color: #94A3B8; font-size: 0.78rem; margin-bottom: 6px;'><strong>SARIMAX Baseline:</strong> WAPE 32.91% | MAPE 48.25% &nbsp;&bull;&nbsp; <strong>Multivariate LSTM:</strong> WAPE 30.78% | MAPE 44.51%</p>", unsafe_allow_html=True)
else:
    plot_df = df_compare.set_index('Date').resample('ME').sum().reset_index()
    mode_str = 'lines+markers'
    
    st.markdown("<p style='color: #94A3B8; font-size: 0.78rem; margin-bottom: 6px;'><strong>SARIMAX Baseline (Monthly):</strong> WAPE 19.79% | MAPE 21.46% &nbsp;&bull;&nbsp; <strong>Multivariate LSTM (Monthly):</strong> WAPE 18.69% | MAPE 19.54%</p>", unsafe_allow_html=True)

fig_line = go.Figure()

# Actual Demand: Silver/White (#F8FAFC) with dot markers.
fig_line.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['Actual_Demand'],
                    mode='lines+markers', name='Actual Demand', 
                    line=dict(color='#F8FAFC', width=2),
                    marker=dict(size=6, color='#F8FAFC')))

# Multivariate LSTM: Vibrant Neon Blue (#38BDF8), width 2.5, smooth splines.
fig_line.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['LSTM_Forecast'],
                    mode=mode_str, name='LSTM Forecast', 
                    line=dict(color='#38BDF8', width=2.5, shape='spline'),
                    marker=dict(size=6, color='#38BDF8')))

# SARIMAX Baseline: Coral/Amber (#FB923C), dashed line.
fig_line.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['SARIMAX_Forecast'],
                    mode=mode_str, name='SARIMAX Forecast', 
                    line=dict(color='#FB923C', width=2, dash='dash'),
                    marker=dict(size=6, color='#FB923C')))

# Clean Plotly chart layouts
fig_line.update_layout(
    title=dict(text=f"Actual vs Forecasted Demand ({view_mode})", font=dict(size=13, color='#F8FAFC')),
    xaxis_title=None, 
    yaxis_title="Volume",
    height=300,
    plot_bgcolor='#1E293B',
    paper_bgcolor='#1E293B',
    legend=dict(
        orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5,
        font=dict(size=9.5, color='#F8FAFC')
    ),
    font=dict(size=10, color="#F8FAFC"),
    margin=dict(l=35, r=15, t=35, b=45)
)
fig_line.update_xaxes(showgrid=False, linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1', gridcolor='#334155', tickfont=dict(size=9))
fig_line.update_yaxes(showgrid=True, gridcolor='#334155', linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1', tickfont=dict(size=9))

st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})

# 3. Forward Production Outlook
st.subheader("Forward Production Outlook (1-Year Horizon)")

tab1, tab2 = st.tabs(["Monthly Horizon (June 2026 – May 2027)", "Weekly Rolling Schedule"])

with tab1:
    df_monthly = df_future.copy()
    df_monthly['Forecast_Week'] = pd.to_datetime(df_monthly['Forecast_Week'])
    df_monthly = df_monthly.set_index('Forecast_Week').resample('ME').sum().reset_index()
    df_monthly['Month'] = df_monthly['Forecast_Week'].dt.strftime('%B %Y')
    df_monthly['Projected Seat Covers'] = df_monthly['Projected_Seat_Covers']
    df_monthly['Safety Buffer (Units)'] = (df_monthly['Projected Seat Covers'] * 0.15).astype(int)
    
    def get_status(idx):
        if idx <= 2: return "✅ Sourced"
        elif idx <= 6: return "⏳ Pending"
        else: return "⚠️ Action Required"
        
    df_monthly['Procurement Status'] = [get_status(i) for i in range(len(df_monthly))]
    
    df_monthly = df_monthly[['Month', 'Projected Seat Covers', 'Safety Buffer (Units)', 'Procurement Status']]
    st.dataframe(df_monthly, use_container_width=True, hide_index=True)

with tab2:
    horizon_options = {
        "Next 12 Weeks (1 Quarter — Operational Focus)": 12,
        "Next 26 Weeks (6 Months — Medium Term)": 26,
        "Full 52 Weeks (Full Year — May 2027)": len(df_future),
    }
    selected_horizon = st.selectbox(
        "Select Schedule Horizon:",
        options=list(horizon_options.keys()),
        index=2,
    )
    weeks_to_show = horizon_options[selected_horizon]
    df_weekly = df_future.head(weeks_to_show).copy()
    df_weekly = df_weekly.rename(columns={'Forecast_Week': 'Forecast Week', 'Projected_Seat_Covers': 'Projected Seat Covers'})
    df_weekly['Shift Target'] = (df_weekly['Projected Seat Covers'] // 5 + 1).astype(str) + " units/shift"
    df_weekly = df_weekly[['Forecast Week', 'Projected Seat Covers', 'Shift Target']]
    st.dataframe(df_weekly, use_container_width=True, hide_index=True)
    st.info("💡 **Practical Note:** Floor managers are advised to stock black leather rolls ahead of time to meet the projected dominant material colour demand.")

# 4. Demand Distribution Breakdown
st.subheader("Demand Distribution Breakdown")
col_chart1, col_chart2 = st.columns(2)

# Distinct vibrant accents for dark theme readability
dark_theme_palette = [
    '#38BDF8', '#818CF8', '#C084FC', '#F472B6', '#FB7185', 
    '#FBBF24', '#34D399', '#2DD4BF', '#60A5FA', '#E879F9',
    '#A78BFA', '#F43F5E', '#F59E0B', '#10B981'
]

with col_chart1:
    fig_donut = px.pie(df_brand, names='Brand', values='Total_Orders', hole=0.4, 
                       title="Volume Distribution by Brand",
                       color_discrete_sequence=dark_theme_palette)
    fig_donut.update_layout(
        title=dict(text="Volume Distribution by Brand", font=dict(size=13, color='#F8FAFC')),
        height=260,
        plot_bgcolor='#1E293B',
        paper_bgcolor='#1E293B',
        font=dict(size=10, color="#F8FAFC"),
        legend=dict(font=dict(size=9, color='#F8FAFC')),
        margin=dict(l=10, r=10, t=35, b=15)
    )
    fig_donut.update_traces(marker=dict(line=dict(color='#1E293B', width=2)))
    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

with col_chart2:
    fig_bar = px.bar(df_color, x='Colour', y='Total_Orders', title="Customer Color Preferences",
                     color='Colour', color_discrete_sequence=dark_theme_palette)
    
    fig_bar.update_layout(
        title=dict(text="Customer Color Preferences", font=dict(size=13, color='#F8FAFC')),
        height=260,
        plot_bgcolor='#1E293B',
        paper_bgcolor='#1E293B',
        font=dict(size=10, color="#F8FAFC"),
        showlegend=False,
        margin=dict(l=35, r=15, t=35, b=30)
    )
    fig_bar.update_xaxes(showgrid=False, linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1', gridcolor='#334155', tickfont=dict(size=9))
    fig_bar.update_yaxes(showgrid=True, gridcolor='#334155', linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1', tickfont=dict(size=9))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
