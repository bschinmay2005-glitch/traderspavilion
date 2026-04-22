import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Terminal", layout="wide")

# --- UI STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b1120; color: #f8fafc; }
        .section-header { 
            border-left: 4px solid #3b82f6; 
            padding-left: 15px; 
            margin: 2rem 0 1rem 0; 
            font-size: 1.2rem; 
            font-weight: 700; 
        }
    </style>
    """, unsafe_allow_html=True)

def tv_single_ticker(symbol, title):
    """Renders a high-performance live ticker card"""
    # This script is the "Permanent Fix" - it cannot be rate-limited
    script = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {{
        "symbol": "{symbol}",
        "width": "100%",
        "colorTheme": "dark",
        "isTransparent": true,
        "locale": "en"
      }}
      </script>
    </div>
    """
    return components.html(script, height=130)

def main():
    apply_styles()
    st.title("🏛️ Institutional Market Terminal")
    
    # Ticker Tape at the top (Optional but looks very pro)
    tape_script = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      { "symbols": [
        {"proName": "FOREXCOM:SPX3500", "title": "S&P 500"},
        {"proName": "BITSTAMP:BTCUSD", "title": "Bitcoin"},
        {"proName": "NSE:NIFTY", "title": "Nifty 50"}
      ], "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "en" }
      </script>
    </div>
    """
    components.html(tape_script, height=50)

    # --- REGIONAL GRID ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="section-header">🇺🇸 US MARKETS</div>', unsafe_allow_html=True)
        tv_single_ticker("FOREXCOM:DJI", "Dow 30")
        tv_single_ticker("INDEX:IUXX", "Nasdaq 100")
        tv_single_ticker("FOREXCOM:SPX3500", "S&P 500")

    with col2:
        st.markdown('<div class="section-header">🇪🇺 EUROPEAN MARKETS</div>', unsafe_allow_html=True)
        tv_single_ticker("INDEX:UKX", "FTSE 100")
        tv_single_ticker("INDEX:DAX", "DAX 40")
        tv_single_ticker("INDEX:PX1", "CAC 40")

    with col3:
        st.markdown('<div class="section-header">🌏 ASIAN MARKETS</div>', unsafe_allow_html=True)
        tv_single_ticker("NSE:NIFTY", "Nifty 50")
        tv_single_ticker("BSE:SENSEX", "Sensex")
        tv_single_ticker("INDEX:NKY", "Nikkei 225")

if __name__ == "__main__":
    main()
