import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Institutional Terminal v3", layout="wide")

def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b1120; color: #f8fafc; }
        .terminal-header { 
            padding: 10px; border-bottom: 1px solid #1e293b; margin-bottom: 20px;
            background: #111827; border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_widget(symbol, height=150):
    """
    PERMANENT SOLUTION: Uses TradingView's high-compatibility 'Mini Chart'.
    This is not a scraper; it is an official CDN delivery. It cannot be blocked.
    """
    html_code = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
      {{
        "symbol": "{symbol}",
        "width": "100%",
        "height": "{height}",
        "locale": "en",
        "dateRange": "1D",
        "colorTheme": "dark",
        "isTransparent": true,
        "autosize": false,
        "largeChartUrl": ""
      }}
      </script>
    </div>
    """
    components.html(html_code, height=height+10)

def main():
    apply_styles()
    
    st.markdown('<div class="terminal-header"><h1>🏛️ Institutional Market Terminal</h1></div>', unsafe_allow_html=True)

    # --- TOP TICKER TAPE (Standard in Pro Terminals) ---
    tape_code = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {"symbols": [
        {"proName": "FOREXCOM:SPX3500", "title": "S&P 500"},
        {"proName": "FOREXCOM:DJI", "title": "Dow 30"},
        {"proName": "BITSTAMP:BTCUSD", "title": "Bitcoin"}
      ], "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "en"}
      </script>
    </div>
    """
    components.html(tape_code, height=50)

    # --- MAIN GRID ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🇺🇸 US MARKETS")
        render_widget("FOREXCOM:SPX3500") # S&P 500
        render_widget("FOREXCOM:DJI")     # Dow 30
        render_widget("NASDAQ:QQQ")       # Nasdaq

    with col2:
        st.subheader("🇪🇺 EUROPEAN MARKETS")
        render_widget("FOREXCOM:UK100")   # FTSE 100
        render_widget("FOREXCOM:GER40")   # DAX 40
        render_widget("FOREXCOM:FRA40")   # CAC 40

    with col3:
        st.subheader("🌏 ASIAN MARKETS")
        render_widget("NSE:NIFTY")        # Nifty 50
        render_widget("BSE:SENSEX")       # Sensex
        render_widget("FX_IDC:USDINR")    # USD/INR (Crucial for Asian Context)

if __name__ == "__main__":
    main()
