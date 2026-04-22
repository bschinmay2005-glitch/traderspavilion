import streamlit as st
import streamlit.components.v1 as components

# 1. UI Configuration & "Strike" Aesthetic
st.set_page_config(page_title="Strike-Style Sector Rotation", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    .sector-box {
        background-color: #0f111a;
        border: 1px solid #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .sector-box:hover { border-color: #3b82f6; transform: translateY(-5px); }
    h2, h3 { color: #60a5fa !important; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. Component: The Rotation Comparison Chart
def render_master_rotation():
    """Embeds an advanced chart pre-configured for sector comparison."""
    html = """
    <div class="tradingview-widget-container" style="height:600px;">
      <div id="rotation_chart"></div>
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
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "hide_legend": false,
        "save_image": false,
        "container_id": "rotation_chart",
        "watchlist": [
            "NSE:CNXAUTO", "NSE:CNXIT", "NSE:CNXPSUBANK", "NSE:NIFTY_FIN_SERVICE",
            "NSE:CNXPHARMA", "NSE:CNXMETAL", "NSE:CNXREALTY", "NSE:CNXENERGY"
        ]
      });
      </script>
    </div>
    """
    components.html(html, height=600)

# 3. Component: The Sentiment/Momentum Gauge (The 'Strike' Logic)
def render_momentum_gauge(symbol):
    """Summarizes technicals to act as a proxy for RRG Quadrants."""
    html = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1D",
        "width": "100%",
        "height": 240,
        "symbol": "{symbol}",
        "showIntervalTabs": false,
        "displayMode": "single",
        "locale": "en",
        "colorTheme": "dark",
        "isTransparent": true
      }}
      </script>
    </div>
    """
    components.html(html, height=250)

# --- APP LAYOUT ---

st.title("🏹 Strike Sector Rotation Terminal")
st.write("Visualizing Relative Strength & Sectoral Momentum")

# Top Section: Performance Comparison
with st.container():
    st.subheader("📍 Relative Performance Hub")
    st.info("Tip: Click the '+' button in the chart to overlay Nifty 50 and see 'Real' rotation.")
    render_master_rotation()

st.markdown("---")

# Bottom Section: The Sectoral Grid
index_groups = {
    "🔥 Leading & High Beta": ["NSE:CNXAUTO", "NSE:CNXIT", "NSE:CNXPSUBANK", "NSE:CNXMETAL", "NSE:CNXREALTY", "NSE:CNXENERGY"],
    "🛡️ Defensive & Thematic": ["NSE:CNXPHARMA", "NSE:CNXFMCG", "NSE:CNXINFRA", "NSE:CNXCONSUMP", "NSE:CNXPSE", "NSE:CNXSERVICE"],
    "🚀 Emerging Sectors": ["NSE:NIFTY_OIL_AND_GAS", "NSE:NIFTY_HEALTHCARE", "NSE:NIFTY_INDIA_MANUFACTURING", "NSE:NIFTY_INDIA_DEFENCE"]
}

for group, tickers in index_groups.items():
    st.subheader(group)
    cols = st.columns(3)
    for i, ticker in enumerate(tickers):
        with cols[i % 3]:
            st.markdown(f'<div class="sector-box">', unsafe_allow_html=True)
            st.markdown(f"**{ticker.split(':')[-1].replace('CNX', 'NIFTY ')}**")
            render_momentum_gauge(ticker)
            st.markdown('</div>', unsafe_allow_html=True)
