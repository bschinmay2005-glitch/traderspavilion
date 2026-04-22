import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Global Market Terminal", layout="wide")

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

def draw_mini_chart(symbol, title):
    """Renders the Mini Chart widget which is more reliable for indices"""
    script = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
      {{
        "symbol": "{symbol}",
        "width": "100%",
        "height": "150",
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
    return components.html(script, height=160)

def main():
    apply_styles()
    st.title("🏛️ Institutional Market Terminal")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="section-header">🇺🇸 US MARKETS</div>', unsafe_allow_html=True)
        # Using CFD symbols which have higher compatibility
        draw_mini_chart("FOREXCOM:DJI", "Dow 30")
        draw_mini_chart("FOREXCOM:NASDAQ", "Nasdaq 100")
        draw_mini_chart("FOREXCOM:SPX3500", "S&P 500")

    with col2:
        st.markdown('<div class="section-header">🇪🇺 EUROPEAN MARKETS</div>', unsafe_allow_html=True)
        draw_mini_chart("FOREXCOM:UK100", "FTSE 100")
        draw_mini_chart("FOREXCOM:GER40", "DAX 40")
        draw_mini_chart("FOREXCOM:FRA40", "CAC 40")

    with col3:
        st.markdown('<div class="section-header">🌏 ASIAN MARKETS</div>', unsafe_allow_html=True)
        draw_mini_chart("NSE:NIFTY", "Nifty 50")
        draw_mini_chart("BSE:SENSEX", "Sensex")
        draw_mini_chart("CAPITALCOM:NI225", "Nikkei 225")

if __name__ == "__main__":
    main()
