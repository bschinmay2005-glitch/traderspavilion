import streamlit as st
import requests
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Market Terminal Pro", layout="wide")

# --- UI STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b0f19; color: #f8fafc; }
        .market-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
        .price-row { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }
        .ticker-price { color: #ffffff; font-size: 1.3rem; font-weight: 700; }
        .pct-box { font-size: 0.85rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
        .pos { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .neg { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- FAST API DATA FETCHING ---
@st.cache_data(ttl=60)
def fetch_market_data():
    # Use your API Key from Secrets or paste here for testing
    api_key = st.secrets.get("TWELVE_DATA_KEY", "DEMO_KEY") 
    
    # Twelve Data supports bulk symbols in one request
    symbols = "DJI,IXIC,SPX,FTSE,FCHI,GDAXI,NIFTY,N225"
    url = f"https://api.twelvedata.com/quote?symbol={symbols}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Twelve Data returns a dict of symbols if multiple are requested
        results = {}
        mapping = {
            "DJI": "Dow Jones", "IXIC": "Nasdaq", "SPX": "S&P 500",
            "FTSE": "FTSE 100", "FCHI": "CAC 40", "GDAXI": "DAX",
            "NIFTY": "Nifty 50", "N225": "Nikkei 225"
        }
        
        for sym, details in data.items():
            if 'close' in details:
                price = float(details['close'])
                change = float(details['percent_change'])
                name = mapping.get(sym, sym)
                results[name] = {
                    "price": f"{price:,.2f}",
                    "change": f"{change:+.2f}%",
                    "is_pos": change >= 0
                }
        return results
    except Exception as e:
        return {}

def draw_card(name, data_pool):
    stats = data_pool.get(name)
    if not stats:
        # Graceful fallback if a specific ticker fails
        st.markdown(f'<div class="market-card"><div class="ticker-name">{name}</div><div class="price-row">Offline</div></div>', unsafe_allow_html=True)
        return
    
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
    st.title("🏛️ Professional Market Terminal")
    
    # Fetch Data
    data = fetch_market_data()
    
    if not data:
        st.error("API Key missing or limit reached. Please check Twelve Data Key.")
        return

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🇺🇸 US Markets")
        for m in ["Dow Jones", "Nasdaq", "S&P 500"]: draw_card(m, data)
    with col2:
        st.subheader("🇪🇺 European Markets")
        for m in ["FTSE 100", "CAC 40", "DAX"]: draw_card(m, data)
    with col3:
        st.subheader("🌏 Asian Markets")
        for m in ["Nifty 50", "Nikkei 225"]: draw_card(m, data)

    st.caption(f"Zero-Delay API Sync • {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
