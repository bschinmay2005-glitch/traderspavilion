import streamlit as st
import requests
import pandas as pd
import datetime
import random
from bs4 import BeautifulSoup

# --- PAGE CONFIG ---
st.set_page_config(page_title="Universal Market Terminal", layout="wide")

# --- CUSTOM TERMINAL STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b0f19; color: #f8fafc; }
        .market-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
        .ticker-price { color: #ffffff; font-size: 1.4rem; font-weight: 700; display: block; margin-top: 5px;}
        .pos { color: #10b981; font-weight: 700; }
        .neg { color: #ef4444; font-weight: 700; }
        .source-tag { font-size: 0.6rem; color: #475569; text-transform: uppercase; margin-top: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- SOURCE 1: YAHOO MOBILE CLUSTER (STABLE) ---
def fetch_yahoo(tickers):
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"}
    symbols = ",".join(tickers.keys())
    try:
        url = f"https://query2.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
        resp = requests.get(url, headers=headers, timeout=5).json()
        data = resp.get('quoteResponse', {}).get('result', [])
        return {itm['symbol']: {"price": itm['regularMarketPrice'], "pct": itm['regularMarketChangePercent'], "src": "Yahoo"} for itm in data}
    except: return {}

# --- SOURCE 2: GOOGLE FINANCE (RELIABLE BACKUP) ---
def fetch_google(symbol):
    try:
        url = f"https://www.google.com/finance/quote/{symbol.replace('^', '.')}"
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        price = soup.find('div', {'class': 'YMlKbe'}).text
        pct = soup.find('div', {'class': 'Jw7C6b'}).text
        return {"price": price, "pct": pct, "src": "Google"}
    except: return None

# --- UNIFIED DATA ENGINE ---
@st.cache_data(ttl=30)
def get_market_data():
    master_list = {
        "^DJI": "Dow Jones", "^IXIC": "Nasdaq", "^GSPC": "S&P 500",
        "^FTSE": "FTSE 100", "^GDAXI": "DAX 40", "^FCHI": "CAC 40",
        "^NSEI": "Nifty 50", "^BSESN": "BSE Sensex", "^N225": "Nikkei 225"
    }
    
    # Try Source 1 (Yahoo)
    final_data = fetch_yahoo(master_list)
    
    # Check for missing data and try Source 2 (Google)
    for sym, name in master_list.items():
        if sym not in final_data:
            g_data = fetch_google(sym)
            if g_data:
                final_data[sym] = g_data
                
    return final_data, master_list

def draw_card(symbol, display_name, data_pool):
    stats = data_pool.get(symbol, {"price": "Offline", "pct": "0.00", "src": "None"})
    
    # Handle different data types from different sources
    try:
        p = stats['price']
        change = stats['pct']
        is_pos = "+" in str(change) or (isinstance(change, (int, float)) and change >= 0)
        color = "pos" if is_pos else "neg"
        arrow = "▲" if is_pos else "▼"
    except:
        p, change, color, arrow = "N/A", "0.00%", "pos", "•"

    st.markdown(f"""
        <div class="market-card">
            <div class="ticker-name">{display_name}</div>
            <span class="ticker-price">{p}</span>
            <span class="{color}">{arrow} {change}%</span>
            <div class="source-tag">Source: {stats['src']}</div>
        </div>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏛️ Multi-Platform Global Terminal")
    
    data, mapping = get_market_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🇺🇸 US MARKETS")
        for s in ["^DJI", "^IXIC", "^GSPC"]: draw_card(s, mapping[s], data)
        
    with col2:
        st.subheader("🇪🇺 EUROPEAN MARKETS")
        for s in ["^FTSE", "^GDAXI", "^FCHI"]: draw_card(s, mapping[s], data)
        
    with col3:
        st.subheader("🌏 ASIAN MARKETS")
        for s in ["^NSEI", "^BSESN", "^N225"]: draw_card(s, mapping[s], data)

if __name__ == "__main__":
    main()
