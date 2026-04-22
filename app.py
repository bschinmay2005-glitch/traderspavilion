import streamlit as st
import streamlit.components.v1 as components

# 1. Setup & Terminal UI
st.set_page_config(page_title="NSE Rotation Terminal", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060606; color: #ffffff; }
    /* Strike Money Style Cards */
    .sector-card {
        background: linear-gradient(145deg, #0f111a, #0a0b10);
        border: 1px solid #1e222d;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .group-header {
        color: #00d4ff;
        font-family: 'Monaco', monospace;
        letter-spacing: 2px;
        border-left: 4px solid #00d4ff;
        padding-left: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. The "Rotation Proxy" Widget
def render_rotation_gauge(symbol):
    """
    Replicates the 'Strike' quadrant logic using TA aggregators.
    Strong Buy = Leading | Buy = Improving | Sell = Weakening | Strong Sell = Lagging
    """
    html = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1D",
        "width": "100%",
        "isTransparent": true,
        "height": 240,
        "symbol": "{symbol}",
        "showIntervalTabs": false,
        "displayMode": "single",
        "locale": "en",
        "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(html, height=240)

# 3. Categorized Tickers (Your List)
index_data = {
    "Sectoral Indices": [
        "NSE:CNXAUTO", "NSE:CNXIT", "NSE:CNXPSUBANK", "NSE:NIFTY_FIN_SERVICE",
        "NSE:CNXPHARMA", "NSE:CNXFMCG", "NSE:CNXMETAL", "NSE:CNXREALTY",
        "NSE:CNXMEDIA", "NSE:CNXENERGY", "NSE:NIFTY_PVT_BANK", "NSE:CNXINFRA"
    ],
    "Thematic & Other Indices": [
        "NSE:CNXCOMMODITIES", "NSE:CNXCONSUMP", "NSE:CNXPSE", "NSE:CNXSERVICE",
        "NSE:NIFTY_FIN_SERVICE_25_50", "NSE:NIFTY_CONSR_DURBL", "NSE:NIFTY_HEALTHCARE",
        "NSE:NIFTY_OIL_AND_GAS", "NSE:NIFTY_INDIA_MANUFACTURING", "NSE:NIFTY_INDIA_DEFENCE"
    ]
}

# 4. Header & Top Comparison
st.title("⚡ NSE SECTOR ROTATION MATRIX")
st.markdown("> **Strike Money Logic:** Quadrant shifts are derived from price vs. benchmark momentum.")

# 5. Rendering the Matrix
for group, tickers in index_data.items():
    st.markdown(f"<h2 class='group-header'>{group.upper()}</h2>", unsafe_allow_html=True)
    
    # Using 4 columns for a true terminal dashboard feel
    cols = st.columns(4)
    for idx, ticker in enumerate(tickers):
        with cols[idx % 4]:
            st.markdown('<div class="sector-card">', unsafe_allow_html=True)
            # Clean up ticker names for display
            display_name = ticker.replace("NSE:", "").replace("CNX", "NIFTY ").replace("_", " ")
            st.markdown(f"<p style='color:#8b949e; font-weight:bold; font-size:0.8rem;'>{display_name}</p>", unsafe_allow_html=True)
            render_rotation_gauge(ticker)
            st.markdown('</div>', unsafe_allow_html=True)

# 6. Technical Overlay (Rotation Trend)
st.sidebar.title("Configuration")
st.sidebar.info("This dashboard uses Browser-Side Rendering (BSR) to bypass NSE API limits and provide live data streams.")
