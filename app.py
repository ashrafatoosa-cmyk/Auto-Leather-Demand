import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Auto Leather Demand Intelligence Dashboard", layout="wide")

# Inject Custom CSS for Dark Executive Appearance
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

st.title("🏎️ AutoLeather Intelligence — Factory Demand & Upholstery DSS")
st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-top: -15px;'>Automotive Interior Cutting & Sewing Operations | OEM & Aftermarket Horizon.</p>", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df_compare = pd.read_csv(os.path.join(base_dir, "dashboard_forecast_comparison.csv"))
    df_future = pd.read_csv(os.path.join(base_dir, "dashboard_future_month_forecast.csv"))
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

total_projected_demand = df_future['Projected_Seat_Covers'].sum()
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
    
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'><strong>SARIMAX Baseline</strong> WAPE: 32.91% | MAPE: 48.25% &nbsp;&nbsp;&nbsp;&nbsp; <strong>Multivariate LSTM</strong> WAPE: 30.78% | MAPE: 44.51%</p>", unsafe_allow_html=True)
else:
    plot_df = df_compare.set_index('Date').resample('ME').sum().reset_index()
    mode_str = 'lines+markers'
    
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'><strong>SARIMAX Baseline (Monthly)</strong> WAPE: 19.79% | MAPE: 21.46% &nbsp;&nbsp;&nbsp;&nbsp; <strong>Multivariate LSTM (Monthly)</strong> WAPE: 18.69% | MAPE: 19.54%</p>", unsafe_allow_html=True)

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
    title=f"Actual vs Forecasted Demand ({view_mode})",
    xaxis_title="Date", 
    yaxis_title="Volume",
    plot_bgcolor='#1E293B',
    paper_bgcolor='#1E293B',
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        font=dict(color='#F8FAFC')
    ),
    font=dict(color="#F8FAFC"),
    margin=dict(l=40, r=40, t=60, b=40)
)
fig_line.update_xaxes(showgrid=False, linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1', gridcolor='#334155')
fig_line.update_yaxes(showgrid=True, gridcolor='#334155', linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1')

st.plotly_chart(fig_line, use_container_width=True)

# 3. Rolling 4-Week Outlook Table
st.subheader("Rolling 4-Week Outlook")
st.dataframe(df_future, use_container_width=True)
st.info("💡 **Practical Note:** Floor managers are advised to stock black leather rolls ahead of time to meet the projected dominant material colour demand.")

# 3.5 Future Monthly Production Targets
st.subheader("Future Monthly Production Targets")

# Ensure Forecast_Week is datetime and aggregate to monthly targets
df_future['Forecast_Week'] = pd.to_datetime(df_future['Forecast_Week'])
df_future_monthly = df_future.set_index('Forecast_Week').resample('ME').sum().reset_index()
# Format the dates for a clean x-axis label
df_future_monthly['Month'] = df_future_monthly['Forecast_Week'].dt.strftime('%B %Y')

fig_future = px.bar(df_future_monthly, x='Month', y='Projected_Seat_Covers', 
                    title="Projected Seat-Cover Volume",
                    text_auto=True,
                    color_discrete_sequence=['#38BDF8'])

fig_future.update_layout(
    plot_bgcolor='#1E293B',
    paper_bgcolor='#1E293B',
    font=dict(color="#F8FAFC")
)
fig_future.update_xaxes(showgrid=False, linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1')
fig_future.update_yaxes(showgrid=True, gridcolor='#334155', linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1')
st.plotly_chart(fig_future, use_container_width=True)

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
        plot_bgcolor='#1E293B',
        paper_bgcolor='#1E293B',
        font=dict(color="#F8FAFC"),
        legend=dict(font=dict(color='#F8FAFC'))
    )
    fig_donut.update_traces(marker=dict(line=dict(color='#1E293B', width=2)))
    st.plotly_chart(fig_donut, use_container_width=True)

with col_chart2:
    fig_bar = px.bar(df_color, x='Colour', y='Total_Orders', title="Customer Color Preferences",
                     color='Colour', color_discrete_sequence=dark_theme_palette)
    
    fig_bar.update_layout(
        plot_bgcolor='#1E293B',
        paper_bgcolor='#1E293B',
        font=dict(color="#F8FAFC"),
        showlegend=False
    )
    fig_bar.update_xaxes(showgrid=False, linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1', gridcolor='#334155')
    fig_bar.update_yaxes(showgrid=True, gridcolor='#334155', linecolor='#CBD5E1', tickcolor='#CBD5E1', color='#CBD5E1')
    st.plotly_chart(fig_bar, width='stretch')
