import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Global Market Terminal", layout="wide")

# --- UI STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0f172a; color: #f8fafc; }
        .market-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            text-decoration: none !important;
            display: block;
        }
        .ticker-name { color: #94a3b8; font-size: 0.8rem; font-weight: 700; }
        .ticker-price { color: #ffffff; font-size: 1.5rem; font-weight: 700; margin: 5px 0; }
        .pos { color: #10b981; } .neg { color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- SCRAPER (REWRITTEN FOR RELIABILITY) ---
@st.cache_data(ttl=60)
def fetch_market_data():
    # Using a different reliable source: Yahoo Finance Indices
    url = "https://finance.yahoo.com/world-indices/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Yahoo Finance specific table selector
        table = soup.find('table')
        rows = table.find_all('tr')[1:] # Skip header
        
        data = []
        for row in rows[:12]: # Get top 12 major world indices
            cols = row.find_all('td')
            if len(cols) > 3:
                name = cols[1].text.strip()
                price = cols[2].text.strip()
                change_val = cols[4].text.strip() # The percentage change column
                
                data.append({
                    "name": name,
                    "price": price,
                    "change": change_val
                })
        return data
    except Exception as e:
        return str(e) # Return error string for debugging

def main():
    apply_styles()
    st.title("🏛️ Global Market Terminal")
    
    data = fetch_market_data()
    
    if isinstance(data, list) and len(data) > 0:
        cols = st.columns(4)
        for idx, item in enumerate(data):
            with cols[idx % 4]:
                is_pos = "-" not in item['change']
                color = "pos" if is_pos else "neg"
                arrow = "▲" if is_pos else "▼"
                
                # TradingView Link
                symbol = item['name'].split()[0].replace("^", "")
                tv_url = f"https://www.tradingview.com/chart/?symbol={symbol}"
                
                st.markdown(f"""
                <a href="{tv_url}" target="_blank" class="market-card">
                    <div class="ticker-name">{item['name']}</div>
                    <div class="ticker-price">{item['price']}</div>
                    <div class="{color}">{arrow} {item['change']}</div>
                </a>
                """, unsafe_allow_html=True)
    else:
        st.error("Live data feed currently unavailable.")
        if st.checkbox("Show Debug Info"):
            st.write(data) # This will show the actual error message

    st.caption(f"Refreshed at: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
