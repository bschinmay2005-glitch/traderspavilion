import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config & Terminal Styling
st.set_page_config(page_title="NSE Sector Rotation Terminal", layout="wide")

st.markdown("""
    <style>
    /* Dark Terminal Theme */
    .stApp {
        background-color: #080c14;
        color: #e0e0e0;
    }
    .sector-card {
        background-color: #121722;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }
    h2, h3 {
        color: #3b82f6 !important;
        font-family: 'Courier New', monospace;
        border-bottom: 1px solid #1f2937;
        padding-bottom: 10px;
    }
    /* Remove padding from streamlit containers for tighter grid */
    [data-testid="column"] {
        padding: 0 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. TradingView Widget Component Function
def tv_mini_chart(symbol):
    """Embeds the TradingView Mini Chart Widget."""
    html_code = f"""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
      {{
      "symbol": "{symbol}",
      "width": "100%",
      "height": 150,
      "locale": "en",
      "dateRange": "1M",
      "colorTheme": "dark",
      "isTransparent": true,
      "autosize": false,
      "largeChartUrl": ""
      }}
      </script>
    </div>
    """
    return components.html(html_code, height=160)

# 3. Ticker Groups
groups = {
    "Key Sectoral": [
        "NSE:NIFTY", "NSE:CNXAUTO", "NSE:CNXIT", 
        "NSE:CNXPSUBANK", "NSE:CNXPHARMA", "NSE:CNXMETAL", 
        "NSE:CNXREALTY", "NSE:CNXENERGY", "NSE:CNXINFRA"
    ],
    "Thematic & Finance": [
        "NSE:NIFTY_FIN_SERVICE", "NSE:CNXFMCG", "NSE:CNXMEDIA", 
        "NSE:CNXCONSUMP", "NSE:CNXPSE", "NSE:CNXSERVICE"
    ],
    "Emerging & Others": [
        "NSE:NIFTY_OIL_AND_GAS", "NSE:NIFTY_HEALTHCARE", 
        "NSE:NIFTY_INDIA_MANUFACTURING", "NSE:NIFTY_INDIA_DEFENCE"
    ]
}

# 4. Dashboard Header
st.title("⚡ NSE Sectoral Rotation Terminal")
st.markdown("---")

# 5. Grid Rendering Logic
for section_title, tickers in groups.items():
    st.subheader(section_title)
    
    # Create rows based on 3-column grid
    cols = st.columns(3)
    for index, ticker in enumerate(tickers):
        with cols[index % 3]:
            st.markdown(f'<div class="sector-card">', unsafe_allow_html=True)
            tv_mini_chart(ticker)
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #4b5563; font-size: 0.8rem; margin-top: 50px;">
    Browser-side execution powered by TradingView. No API limits applied.
</div>
""", unsafe_allow_html=True)
