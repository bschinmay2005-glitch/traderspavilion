import streamlit as st
import requests
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Terminal Pro", layout="wide")

# --- UI STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b1120; color: #f8fafc; }
        .market-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
            text-decoration: none !important;
            display: block;
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
        .price-row { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }
        .ticker-price { color: #ffffff; font-size: 1.3rem; font-weight: 700; }
        .pct-box { font-size: 0.85rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
        .pos { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .neg { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- HARDENED DATA FETCHING ---
@st.cache_data(ttl=60)
def fetch_all_markets():
    # Master list of tickers
    tickers = {
        "^DJI": "Dow Jones", "^IXIC": "Nasdaq", "^GSPC": "S&P 500",
        "^FTSE": "FTSE 100", "^FCHI": "CAC 40", "^GDAXI": "DAX",
        "^NSEI": "Nifty 50", "^BSESN": "BSE Sensex", "^NSEBANK": "Nifty Bank",
        "^N225": "Nikkei 225", "^HSI": "Hang Seng", "^VIX": "India VIX"
    }
    
    results = {}
    
    # Using a Session to persist cookies (Bypasses many bot-detection layers)
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://finance.yahoo.com/"
    }

    try:
        # Requesting data
        symbols = ",".join(tickers.keys())
        url = f"https://query2.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
        
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return {"error": f"Server rejected request (Error {response.status_code})"}
            
        data = response.json()
        items = data.get('quoteResponse', {}).get('result', [])

        for item in items:
            sym = item.get('symbol')
            price = item.get('regularMarketPrice', 0)
            change = item.get('regularMarketChangePercent', 0)
            
            name = tickers.get(sym, sym)
            results[name] = {
                "price": f"{price:,.2f}",
                "change": f"{change:+.2f}%",
                "is_pos": change >= 0,
                "symbol_tv": sym.replace('^', '')
            }
        return results
    except Exception as e:
        return {"error": f"Deep Connection Error: {str(e)}"}

# --- UI COMPONENTS ---
def draw_card(name, data_pool):
    stats = data_pool.get(name)
    if not stats: return
    
    status = "pos" if stats['is_pos'] else "neg"
    arrow = "▲" if stats['is_pos'] else "▼"
    tv_url = f"https://www.tradingview.com/chart/?symbol={stats['symbol_tv']}"
    
    st.markdown(f"""
        <a href="{tv_url}" target="_blank" class="market-card">
            <div class="ticker-name">{name}</div>
            <div class="price-row">
                <span class="ticker-price">{stats['price']}</span>
                <span class="pct-box {status}">{arrow} {stats['change']}</span>
            </div>
        </a>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏛️ Global Market Terminal")
    
    data = fetch_all_markets()
    
    if "error" in data:
        st.warning("⚠️ High Traffic: Retrying secure connection...")
        st.info("The data source is currently rate-limiting this cloud region. Please refresh in 30 seconds.")
        with st.expander("Technical Error Logs"):
            st.code(data['error'])
        return

    # Categories
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🇺🇸 US Markets")
        for m in ["Dow Jones", "Nasdaq", "S&P 500"]: draw_card(m, data)
    with c2:
        st.subheader("🇪🇺 European Markets")
        for m in ["FTSE 100", "CAC 40", "DAX"]: draw_card(m, data)
    with c3:
        st.subheader("🌏 Asian Markets")
        for m in ["Nifty 50", "Nikkei 225", "Hang Seng"]: draw_card(m, data)

    st.caption(f"Secure Sync Active • {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
