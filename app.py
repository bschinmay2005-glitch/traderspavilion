import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sector Rotation Terminal", layout="wide")

# Custom CSS for the "Strike" Dark Mode Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .metric-card {
        background-color: #0f111a;
        border: 1px solid #1e222d;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; color: #00ffcc !important; }
    </style>
""", unsafe_allow_html=True)

def render_comparison_chart():
    """The 'Rotation' view - Multiple sectors vs Nifty"""
    html = """
    <div class="tradingview-widget-container" style="height:500px;">
      <div id="tradingview_rotation"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "NSE:NIFTY",
        "interval": "D",
        "timezone": "Asia/Kolkata",
        "theme": "dark",
        "style": "3",
        "locale": "en",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "container_id": "tradingview_rotation",
        "watchlist": [
            "NSE:CNXAUTO", "NSE:CNXIT", "NSE:CNXPSUBANK", "NSE:CNXMETAL", 
            "NSE:CNXREALTY", "NSE:NIFTY_FIN_SERVICE", "NSE:CNXFMCG"
        ],
        "details": true,
        "hotlist": true,
        "calendar": false
      });
      </script>
    </div>
    """
    components.html(html, height=500)

def render_gauge(symbol):
    """Replicates the Leading/Lagging sentiment using TA Gauges"""
    html = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1D",
        "width": "100%",
        "isTransparent": true,
        "height": 280,
        "symbol": "{symbol}",
        "showIntervalTabs": true,
        "displayMode": "single",
        "locale": "en",
        "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(html, height=280)

# --- Layout ---

st.title("📊 Sector Rotation Intelligence")
st.markdown("Relative Strength & Momentum Matrix")

# 1. Top Section: The Comparison Chart (The "Strike" Rotation View)
st.subheader("Performance Comparison (Relative to Nifty)")
render_comparison_chart()

st.markdown("---")

# 2. Sector Grid: The Sentiment Matrix
sectors = {
    "Cyclical / High Beta": ["NSE:CNXAUTO", "NSE:CNXMETAL", "NSE:CNXREALTY"],
    "Defensive / Stability": ["NSE:CNXFMCG", "NSE:CNXPHARMA", "NSE:CNXINFRA"],
    "Financials & IT": ["NSE:NIFTY_FIN_SERVICE", "NSE:CNXPSUBANK", "NSE:CNXIT"]
}

for group_name, ticker_list in sectors.items():
    st.subheader(group_name)
    cols = st.columns(3)
    for i, ticker in enumerate(ticker_list):
        with cols[i]:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f"**{ticker.split(':')[-1]}**")
            render_gauge(ticker)
            st.markdown('</div>', unsafe_allow_html=True)
