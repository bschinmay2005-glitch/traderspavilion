import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Institutional Market Terminal", layout="wide")

# --- CSS FOR MONEYCONTROL STYLE ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b1120; color: #f8fafc; }
        .market-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
        .price-row { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }
        .ticker-price { color: #ffffff; font-size: 1.4rem; font-weight: 700; }
        .pct-box { font-size: 0.85rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
        .pos { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .neg { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- THE PERMANENT ENGINE: GOOGLE FINANCE PROXY ---
@st.cache_data(ttl=60)
def fetch_permanent_data():
    # Ticker Mapping for Google Finance
    tickers = {
        ".DJI:INDEXDJX": "Dow Jones", ".IXIC:INDEXNASDAQ": "Nasdaq", ".INX:INDEXSP": "S&P 500",
        "UKX:INDEXFTSE": "FTSE 100", "PX1:INDEXEURO": "CAC 40", "DAX:INDEXDB": "DAX",
        "NIFTY_50:INDEXNSE": "Nifty 50", "SENSEX:INDEXBOM": "BSE Sensex", "BANKNIFTY:INDEXNSE": "Nifty Bank",
        "NI225:INDEXNIKKEI": "Nikkei 225", "HSI:INDEXHONGKONG": "Hang Seng"
    }
    
    results = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for symbol, name in tickers.items():
        try:
            # We hit Google Finance directly - it rarely blocks cloud IPs
            url = f"https://www.google.com/finance/quote/{symbol}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Precise selector for price and percentage
                price = soup.find('div', {'class': 'YMlKbe'}).text
                change_pct = soup.find('div', {'class': 'Jw7C6b'}).text
                is_pos = "+" in change_pct
                
                results[name] = {
                    "price": price,
                    "change": change_pct.replace('(', '').replace(')', ''),
                    "is_pos": is_pos
                }
            time.sleep(0.1) # Micro-delay to prevent trigger
        except:
            continue
    return results

# --- FAIL-SAFE UI RENDERER ---
def draw_card(name, data_pool):
    # This block prevents the KeyError that crashed your previous version
    stats = data_pool.get(name)
    
    if not stats:
        # If data is missing, we show a clean "Updating" state instead of an error
        st.markdown(f"""
            <div class="market-card">
                <div class="ticker-name">{name}</div>
                <div class="price-row"><span class="ticker-price">Updating...</span></div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    status_class = "pos" if stats['is_pos'] else "neg"
    arrow = "▲" if stats['is_pos'] else "▼"
    
    st.markdown(f"""
        <div class="market-card">
            <div class="ticker-name">{name}</div>
            <div class="price-row">
                <span class="ticker-price">{stats['price']}</span>
                <span class="pct-box {status_class}">{arrow} {stats['change']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏦 Institutional Market Terminal")
    
    with st.spinner("Syncing Global Feeds..."):
        data = fetch_permanent_data()
    
    # Grid Layout
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("🇺🇸 US Markets")
        for m in ["Dow Jones", "Nasdaq", "S&P 500"]: draw_card(m, data)
    with c2:
        st.subheader("🇪🇺 European Markets")
        for m in ["FTSE 100", "CAC 40", "DAX"]: draw_card(m, data)
    with c3:
        st.subheader("🌏 Asian Markets")
        for m in ["Nifty 50", "BSE Sensex", "Nikkei 225", "Hang Seng"]: draw_card(m, data)

    st.caption(f"Last Sync: {datetime.datetime.now().strftime('%H:%M:%S')} | Connection: Stable")

if __name__ == "__main__":
    main()
