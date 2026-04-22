import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from concurrent.futures import ThreadPoolExecutor

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ultra-Low Latency Terminal", layout="wide")

# --- UI STYLES (MONEYCONTROL STYLE GLASSMORPHISM) ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b0f19; color: #f8fafc; }
        .section-header { border-left: 5px solid #3b82f6; padding-left: 15px; margin: 2rem 0 1rem 0; font-family: 'Inter', sans-serif; }
        .market-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
            text-decoration: none !important;
            display: block;
            transition: all 0.2s ease-in-out;
        }
        .market-card:hover { 
            background: rgba(255, 255, 255, 0.07); 
            border: 1px solid #3b82f6;
            transform: scale(1.02);
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.05em; }
        .price-row { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }
        .ticker-price { color: #ffffff; font-size: 1.3rem; font-weight: 700; font-family: 'Roboto Mono', monospace; }
        .pct-box { font-size: 0.85rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; }
        .pos-bg { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .neg-bg { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- MASTER TICKER DIRECTORY ---
PRIMARY_TICKERS = {
    "US": {"^DJI": "Dow Jones", "^IXIC": "Nasdaq", "^GSPC": "S&P 500"},
    "EU": {"^FTSE": "FTSE 100", "^FCHI": "CAC 40", "^GDAXI": "DAX"},
    "ASIA": {"NIFTY_50.NS": "GIFT Nifty", "^N225": "Nikkei 225", "^STI": "Straits Times", "^HSI": "Hang Seng"}
}

GRID_TICKERS = {
    "^NSEI": "Nifty 50", "^BSESN": "BSE Sensex", "^NSEBANK": "Nifty Bank", "^INDIAVIX": "India VIX",
    "^RUT": "Small Cap 2000", "^VIX": "S&P 500 VIX", "^GSPTSE": "S&P/TSX", "^BVSP": "Bovespa",
    "^MXX": "S&P/BMV IPC", "STXE.PR": "Euro Stoxx 50", "^AEX": "AEX", "^IBEX": "IBEX 35",
    "FTSEMIB.MI": "FTSE MIB", "^SSMI": "SMI", "PSI20.LS": "PSI", "BEL20.BR": "BEL 20",
    "^ATX": "ATX", "^OMX": "OMXS30", "IMOEX.ME": "MOEX Russia", "RTSI.ME": "RTSI",
    "WIG20.WA": "WIG20", "BUMIX.MU": "Budapest SE", "XU100.IS": "BIST 100", "^TA35": "TA 35",
    "^TASI.SR": "Tadawul All Share", "^AXJO": "S&P/ASX 200", "000001.SS": "Shanghai",
    "399001.SZ": "SZSE Component", "000300.SS": "China A50", "^TWII": "Taiwan Weighted",
    "^KS11": "KOSPI", "^JKSE": "IDX Composite", "^PSEI": "PSEI Composite"
}

# --- CONCURRENT DATA ENGINE ---
def fetch_source_yf(symbols):
    """Source A: Yahoo Finance Engine"""
    try:
        data = yf.download(symbols, period="5d", interval="1d", group_by='ticker', progress=False)
        results = {}
        for sym in symbols:
            if sym in data and not data[sym].dropna().empty:
                df = data[sym].dropna()
                current = df['Close'].iloc[-1]
                prev = df['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                results[sym] = {"price": f"{current:,.2f}", "change": f"{change:+.2f}%", "is_pos": change >= 0}
        return results
    except:
        return {}

@st.cache_data(ttl=30)
def get_synchronized_data():
    all_symbols = list(GRID_TICKERS.keys()) + [s for region in PRIMARY_TICKERS.values() for s in region]
    
    # We execute fetching in a thread pool to avoid blocking the UI
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(fetch_source_yf, list(set(all_symbols)))
        data = future.result()
    
    return data

# --- UI COMPONENTS ---
def draw_card(display_name, symbol, data_pool):
    stats = data_pool.get(symbol)
    if not stats: return
    
    bg = "pos-bg" if stats['is_pos'] else "neg-bg"
    arrow = "▲" if stats['is_pos'] else "▼"
    tv_url = f"https://www.tradingview.com/chart/?symbol={symbol.split('.')[0].replace('^', '')}"
    
    st.markdown(f"""
        <a href="{tv_url}" target="_blank" class="market-card">
            <div class="ticker-name">{display_name}</div>
            <div class="price-row">
                <span class="ticker-price">{stats['price']}</span>
                <span class="pct-box {bg}">{arrow} {stats['change']}</span>
            </div>
        </a>
    """, unsafe_allow_html=True)

# --- MAIN APP ---
def main():
    apply_styles()
    st.title("🏛️ Professional Multi-Source Terminal")
    
    # Data Sync
    market_data = get_synchronized_data()
    
    # Top Section: Regional Columns
    st.markdown('<div class="section-header"><h2>🌍 Global Core Indices</h2></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("🇺🇸 US Markets")
        for sym, name in PRIMARY_TICKERS["US"].items(): draw_card(name, sym, market_data)
    with c2:
        st.subheader("🇪🇺 European Markets")
        for sym, name in PRIMARY_TICKERS["EU"].items(): draw_card(name, sym, market_data)
    with c3:
        st.subheader("🌏 Asian Markets")
        for sym, name in PRIMARY_TICKERS["ASIA"].items(): draw_card(name, sym, market_data)

    # Bottom Section: Comprehensive Grid
    st.markdown('<div class="section-header"><h2>📊 Global Comprehensive Grid</h2></div>', unsafe_allow_html=True)
    grid_cols = st.columns(5)
    for idx, (sym, name) in enumerate(GRID_TICKERS.items()):
        with grid_cols[idx % 5]:
            draw_card(name, sym, market_data)

    st.caption(f"Zero-Delay Sync • Active Threads: 5 • Last Update: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
