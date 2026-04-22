import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Market Terminal", layout="wide")

# --- UI STYLES (GLASSMORPHISM) ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0f172a; color: #f8fafc; }
        .market-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            text-decoration: none !important;
            display: block;
            transition: transform 0.2s;
        }
        .market-card:hover { transform: translateY(-3px); background: rgba(255, 255, 255, 0.08); }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
        
        /* Flexbox for Price and Percentage Side-by-Side */
        .price-row { display: flex; align-items: baseline; gap: 10px; }
        .ticker-price { color: #ffffff; font-size: 1.4rem; font-weight: 700; }
        .pct-box { font-size: 0.9rem; font-weight: 600; padding: 2px 6px; border-radius: 4px; }
        
        .pos { color: #10b981; } 
        .neg { color: #ef4444; }
        .pos-bg { background: rgba(16, 185, 129, 0.15); color: #10b981; }
        .neg-bg { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA FETCHING ---
@st.cache_data(ttl=60)
def fetch_data():
    url = "https://finance.yahoo.com/world-indices/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]
        
        results = []
        for row in rows[:12]:
            cols = row.find_all('td')
            if len(cols) >= 5:
                results.append({
                    "name": cols[1].text.strip(),
                    "price": cols[2].text.strip(),
                    "change": cols[4].text.strip()
                })
        return results
    except Exception as e:
        return []

def main():
    apply_styles()
    st.title("🏛️ Global Market Terminal")
    
    data = fetch_data()
    
    if data:
        cols = st.columns(4)
        for idx, item in enumerate(data):
            with cols[idx % 4]:
                # Logic for colors
                is_pos = "+" in item['change'] or "-" not in item['change']
                status_class = "pos" if is_pos else "neg"
                bg_status = "pos-bg" if is_pos else "neg-bg"
                arrow = "▲" if is_pos else "▼"
                
                # Dynamic Link
                clean_symbol = item['name'].split()[0].replace("^", "")
                tv_url = f"https://www.tradingview.com/chart/?symbol={clean_symbol}"
                
                # HTML Output
                st.markdown(f"""
                <a href="{tv_url}" target="_blank" class="market-card">
                    <div class="ticker-name">{item['name']}</div>
                    <div class="price-row">
                        <span class="ticker-price">{item['price']}</span>
                        <span class="pct-box {bg_status}">{arrow} {item['change']}</span>
                    </div>
                </a>
                """, unsafe_allow_html=True)
    else:
        st.error("Data source unreachable. Please wait 60 seconds and refresh.")

    st.caption(f"Last sync: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
