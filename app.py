import streamlit as st
import yfinance as yf
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Market Terminal", layout="wide")

# --- UI STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0f172a; color: #f8fafc; }
        .section-header { 
            border-left: 4px solid #3b82f6; padding-left: 15px; 
            margin: 2rem 0 1rem 0; font-size: 1.5rem; font-weight: 700; 
        }
        .market-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 10px;
            text-decoration: none !important;
            display: block;
            transition: 0.2s;
        }
        .market-card:hover { background: rgba(255, 255, 255, 0.08); transform: translateY(-2px); }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
        .price-row { display: flex; align-items: center; justify-content: space-between; }
        .ticker-price { color: #ffffff; font-size: 1.1rem; font-weight: 700; }
        .pct-box { font-size: 0.8rem; font-weight: 600; padding: 2px 6px; border-radius: 4px; }
        .pos-bg { background: rgba(16, 185, 129, 0.15); color: #10b981; }
        .neg-bg { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING WITH YFINANCE ---
@st.cache_data(ttl=120)
def get_market_data():
    ticker_map = {
        "^DJI": "Dow Jones", "^IXIC": "Nasdaq", "^GSPC": "S&P 500",
        "^FTSE": "FTSE 100", "^FCHI": "CAC 40", "^GDAXI": "DAX",
        "IN_OR.SN": "GIFT Nifty", "^N225": "Nikkei 225", "^STI": "Straits Times", "^HSI": "Hang Seng",
        "^NSEI": "Nifty 50", "^BSESN": "BSE Sensex", "^NSEBANK": "Nifty Bank", "^VIX": "India VIX",
        "^RUT": "Small Cap 2000", "^VXV": "S&P 500 VIX", "^GSPTSE": "S&P/TSX", "^BVSP": "Bovespa",
        "^MXX": "S&P/BMV IPC", "STOXX50E": "Euro Stoxx 50", "^AEX": "AEX", "^IBEX": "IBEX 35",
        "FTSEMIB.MI": "FTSE MIB", "^SSMI": "SMI", "PSI20.LS": "PSI", "BEL20.BR": "BEL 20",
        "^ATX": "ATX", "^OMX": "OMXS30", "IMOEX.ME": "MOEX Russia", "RTSI.ME": "RTSI",
        "WIG20.WA": "WIG20", "^BUMIX": "Budapest SE", "XU100.IS": "BIST 100", "^TA35": "TA 35",
        "^TASI.SR": "Tadawul All Share", "^AXJO": "S&P/ASX 200", "000001.SS": "Shanghai",
        "399001.SZ": "SZSE Component", "000300.SS": "China A50", "^TWII": "Taiwan Weighted",
        "^KS11": "KOSPI", "^JKSE": "IDX Composite", "^PSEI": "PSEI Composite"
    }
    
    symbols = list(ticker_map.keys())
    # Fetch all data in one go for speed
    data = yf.download(symbols, period="2d", interval="1d", group_by='ticker', progress=False)
    
    final_results = {}
    for sym in symbols:
        try:
            # Get latest and previous close to calculate change
            if sym in data:
                current_close = data[sym]['Close'].iloc[-1]
                prev_close = data[sym]['Close'].iloc[-2]
                pct_change = ((current_close - prev_close) / prev_close) * 100
                
                final_results[ticker_map[sym]] = {
                    "price": f"{current_close:,.2f}",
                    "change": f"{pct_change:+.2f}%",
                    "is_pos": pct_change >= 0
                }
        except:
            continue
    return final_results

def draw_card(name, data_dict):
    stats = data_dict.get(name)
    if not stats: return
    
    bg_class = "pos-bg" if stats['is_pos'] else "neg-bg"
    arrow = "▲" if stats['is_pos'] else "▼"
    tv_url = f"https://www.tradingview.com/chart/?symbol={name.replace(' ', '')}"
    
    st.markdown(f"""
        <a href="{tv_url}" target="_blank" class="market-card">
            <div class="ticker-name">{name}</div>
            <div class="price-row">
                <span class="ticker-price">{stats['price']}</span>
                <span class="pct-box {bg_class}">{arrow} {stats['change']}</span>
            </div>
        </a>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏦 Global Market Monitor")
    
    with st.spinner("Fetching Live Market Data..."):
        data = get_market_data()
    
    if not data:
        st.error("API Limit reached or source blocked. Retrying in 60s...")
        return

    # --- PRIMARY MARKETS ---
    st.markdown('<div class="section-header">🌍 Primary Global Markets</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🇺🇸 US Markets")
        for m in ["Dow Jones", "Nasdaq", "S&P 500"]: draw_card(m, data)
    with c2:
        st.subheader("🇪🇺 European Markets")
        for m in ["FTSE 100", "CAC 40", "DAX"]: draw_card(m, data)
    with c3:
        st.subheader("🌏 Asian Markets")
        for m in ["GIFT Nifty", "Nikkei 225", "Straits Times", "Hang Seng"]: draw_card(m, data)

    # --- COMPREHENSIVE GRID ---
    st.markdown('<div class="section-header">📊 Comprehensive Market Overview</div>', unsafe_allow_html=True)
    all_others = [
        "Nifty 50", "BSE Sensex", "Nifty Bank", "India VIX", "Small Cap 2000", 
        "S&P 500 VIX", "S&P/TSX", "Bovespa", "S&P/BMV IPC", "Euro Stoxx 50", 
        "AEX", "IBEX 35", "FTSE MIB", "SMI", "PSI", "BEL 20", "ATX", "OMXS30", 
        "MOEX Russia", "RTSI", "WIG20", "Budapest SE", "BIST 100", "TA 35", 
        "Tadawul All Share", "S&P/ASX 200", "Shanghai", "SZSE Component", 
        "China A50", "Taiwan Weighted", "KOSPI", "IDX Composite", "PSEI Composite"
    ]
    
    grid_cols = st.columns(5)
    for idx, name in enumerate(all_others):
        with grid_cols[idx % 5]:
            draw_card(name, data)

    st.caption(f"Powered by yfinance • Sync Time: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
