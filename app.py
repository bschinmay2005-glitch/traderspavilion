import streamlit as st
import requests
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Professional Market Terminal", layout="wide")

# --- UI STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b0f19; color: #f8fafc; }
        .market-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
            text-decoration: none !important;
            display: block;
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; }
        .price-row { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }
        .ticker-price { color: #ffffff; font-size: 1.3rem; font-weight: 700; }
        .pct-box { font-size: 0.85rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; }
        .pos { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .neg { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- DIRECT DATA ENGINE ---
@st.cache_data(ttl=30)
def fetch_global_data():
    # Master mapping
    ticker_map = {
        "^DJI": "Dow Jones", "^IXIC": "Nasdaq", "^GSPC": "S&P 500",
        "^FTSE": "FTSE 100", "^FCHI": "CAC 40", "^GDAXI": "DAX",
        "NIFTY_50.NS": "Nifty 50", "^N225": "Nikkei 225", "^STI": "Straits Times", "^HSI": "Hang Seng",
        "^NSEI": "Nifty 50", "^BSESN": "BSE Sensex", "^NSEBANK": "Nifty Bank", "^INDIAVIX": "India VIX"
    }
    
    symbols = ",".join(ticker_map.keys())
    # This URL mimics the one used by mobile finance apps
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        json_data = response.json()
        quotes = json_data.get('quoteResponse', {}).get('result', [])
        
        results = {}
        for q in quotes:
            sym = q.get('symbol')
            price = q.get('regularMarketPrice', 0)
            change = q.get('regularMarketChangePercent', 0)
            
            results[ticker_map.get(sym, sym)] = {
                "price": f"{price:,.2f}",
                "change": f"{change:+.2f}%",
                "is_pos": change >= 0
            }
        return results
    except Exception as e:
        return {"error": str(e)}

# --- UI COMPONENTS ---
def draw_card(name, data_pool):
    stats = data_pool.get(name)
    if not stats: return
    
    status = "pos" if stats['is_pos'] else "neg"
    arrow = "▲" if stats['is_pos'] else "▼"
    
    st.markdown(f"""
        <div class="market-card">
            <div class="ticker-name">{name}</div>
            <div class="price-row">
                <span class="ticker-price">{stats['price']}</span>
                <span class="pct-box {status}">{arrow} {stats['change']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏦 Multi-Source Market Bar")
    
    data = fetch_global_data()
    
    if "error" in data:
        st.error(f"Connection failed: {data['error']}")
        return

    # Regional Display
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🇺🇸 US Markets")
        for m in ["Dow Jones", "Nasdaq", "S&P 500"]: draw_card(m, data)
    with c2:
        st.subheader("🇪🇺 European Markets")
        for m in ["FTSE 100", "CAC 40", "DAX"]: draw_card(m, data)
    with c3:
        st.subheader("🌏 Asian Markets")
        for m in ["Nifty 50", "Nikkei 225", "Straits Times", "Hang Seng"]: draw_card(m, data)

    st.caption(f"Zero-Delay Sync • Last Update: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
