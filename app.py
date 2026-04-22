import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Market Terminal", layout="wide")

# --- UI STYLES ---
st.markdown("""
<style>
    .stApp { background: #0b1120; }
    .section-header { 
        color: #f8fafc; 
        border-left: 4px solid #3b82f6; 
        padding-left: 15px; 
        margin: 20px 0; 
        font-weight: bold; 
    }
</style>
""", unsafe_allow_html=True)

def tradingview_widget(symbols):
    """Generates the official TradingView Market Overview Widget"""
    script = f"""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>
      {{
      "colorTheme": "dark",
      "dateRange": "12M",
      "showChart": true,
      "locale": "en",
      "width": "100%",
      "height": "450",
      "largeChartUrl": "",
      "isTransparent": true,
      "showSymbolLogo": true,
      "showFloatingTooltip": false,
      "tabs": [
        {{
          "title": "Global Indices",
          "symbols": {symbols},
          "originalTitle": "Indices"
        }}
      ]
    }}
      </script>
    </div>
    """
    return components.html(script, height=460)

st.title("🏛️ Institutional Market Terminal")

# --- SECTION 1: WESTERN MARKETS ---
st.markdown('<div class="section-header">🇺🇸 US & 🇪🇺 EUROPEAN INDICES</div>', unsafe_allow_html=True)
us_eu_symbols = [
    {"s": "FOREXCOM:SPX3500", "d": "S&P 500"},
    {"s": "FOREXCOM:DJI", "d": "Dow 30"},
    {"s": "INDEX:IUXX", "d": "Nasdaq 100"},
    {"s": "INDEX:UKX", "d": "FTSE 100"},
    {"s": "INDEX:DAX", "d": "DAX 40"}
]
tradingview_widget(us_eu_symbols)

# --- SECTION 2: ASIAN MARKETS ---
st.markdown('<div class="section-header">🌏 ASIAN & EMERGING MARKETS</div>', unsafe_allow_html=True)
asia_symbols = [
    {"s": "NSE:NIFTY", "d": "Nifty 50"},
    {"s": "BSE:SENSEX", "d": "SENSEX"},
    {"s": "INDEX:NKY", "d": "Nikkei 225"},
    {"s": "INDEX:HSI", "d": "Hang Seng"}
]
tradingview_widget(asia_symbols)

st.caption("Data provided by TradingView Real-Time Feeds • No API Key Required")
