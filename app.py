import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nifty Sector Terminal", layout="wide")

def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #080c14; color: #f8fafc; }
        .section-header { 
            border-left: 4px solid #3b82f6; padding-left: 15px; 
            margin: 2rem 0 1rem 0; font-size: 1.2rem; font-weight: 700; 
        }
        h1 { color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

def draw_widget(symbol, height=160):
    """Bypasses Python server to fetch data directly in the browser."""
    script = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
      {{
        "symbol": "{symbol}",
        "width": "100%", "height": "{height}",
        "locale": "en", "dateRange": "1D",
        "colorTheme": "dark", "isTransparent": true,
        "autosize": false, "largeChartUrl": ""
      }}
      </script>
    </div>
    """
    return components.html(script, height=height + 10)

def main():
    apply_styles()
    st.title("🏛️ Institutional Nifty Terminal")
    st.caption("Live Direct Feeds • Zero API Latency")

    # Group 1: Key Indices
    st.markdown('<div class="section-header">KEY & BROAD INDICES</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: draw_widget("NSE:NIFTY") # Nifty 50
    with c2: draw_widget("NSE:BANKNIFTY") # Bank
    with c3: draw_widget("NSE:NIFTY_MID_50") # Midcap

    # Group 2: Major Sectoral
    st.markdown('<div class="section-header">MAJOR SECTORAL INDICES</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4: draw_widget("NSE:CNXAUTO")
    with c5: draw_widget("NSE:CNXIT")
    with c6: draw_widget("NSE:CNXPHARMA")
    
    c7, c8, c9 = st.columns(3)
    with c7: draw_widget("NSE:CNXMETAL")
    with c8: draw_widget("NSE:CNXFMCG")
    with c9: draw_widget("NSE:CNXPSUBANK")

    # Group 3: Emerging & Thematic
    st.markdown('<div class="section-header">THEMATIC & EMERGING</div>', unsafe_allow_html=True)
    c10, c11, c12 = st.columns(3)
    with c10: draw_widget("NSE:NIFTY_INDIA_DEFENCE")
    with c11: draw_widget("NSE:NIFTY_OIL_AND_GAS")
    with c12: draw_widget("NSE:NIFTY_IND_MFG") # India Mfg

    c13, c14, c15 = st.columns(3)
    with c13: draw_widget("NSE:CNXREALTY")
    with c14: draw_widget("NSE:CNXINFRA")
    with c15: draw_widget("NSE:CNXENERGY")

if __name__ == "__main__":
    main()
