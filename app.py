import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NSE Sector Rotation", layout="wide")

# CSS: True Black Terminal Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .index-card {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    h2 { color: #58a6ff !important; font-size: 1.2rem; border-bottom: 1px solid #30363d; padding-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

def render_gauge(symbol):
    html = f"""
    <div style="height:220px;">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1D", "width": "100%", "isTransparent": true, "height": 220,
        "symbol": "{symbol}", "showIntervalTabs": false, "displayMode": "single",
        "locale": "en", "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(html, height=220)

# --- INDEX MAPPING ---
# Categorized exactly as requested
groups = {
    "📊 Key Sectoral": [
        "NSE:CNXAUTO", "NSE:CNXIT", "NSE:CNXPSUBANK", "NSE:NIFTY_FIN_SERVICE",
        "NSE:CNXPHARMA", "NSE:CNXFMCG", "NSE:CNXMETAL", "NSE:CNXREALTY"
    ],
    "🏦 Banking & Finance": [
        "NSE:NIFTY_PVT_BANK", "NSE:NIFTY_FIN_SERVICE_25_50", "NSE:CNXSERVICE"
    ],
    "🏗️ Thematic & Infrastructure": [
        "NSE:CNXINFRA", "NSE:CNXENERGY", "NSE:CNXMEDIA", "NSE:CNXCOMMODITIES", 
        "NSE:CNXCONSUMP", "NSE:CNXPSE"
    ],
    "🚀 Emerging & New Specific": [
        "NSE:NIFTY_CONSR_DURBL", "NSE:NIFTY_HEALTHCARE", "NSE:NIFTY_OIL_AND_GAS", 
        "NSE:NIFTY_INDIA_MANUFACTURING", "NSE:NIFTY_INDIA_DEFENCE"
    ]
}

st.title("🎯 NSE Sectoral Matrix")

# Render the Grid
for group_name, tickers in groups.items():
    st.subheader(group_name)
    cols = st.columns(4) # 4 columns for a dense terminal feel
    for i, ticker in enumerate(tickers):
        with cols[i % 4]:
            st.markdown(f'<div class="index-card">', unsafe_allow_html=True)
            # Displaying a cleaner name for the UI
            label = ticker.split(':')[-1].replace('CNX', 'NIFTY ')
            st.markdown(f"<code style='color:#8b949e'>{label}</code>", unsafe_allow_html=True)
            render_gauge(ticker)
            st.markdown('</div>', unsafe_allow_html=True)
