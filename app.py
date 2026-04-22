import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(
    page_title="FinTech Market Bar",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM CSS (GLASSMORPHISM) ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: radial-gradient(circle at top left, #0f172a, #1e293b); color: #f8fafc; }
        .market-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            text-decoration: none !important;
            display: block;
            transition: 0.3s;
        }
        .market-card:hover { background: rgba(255, 255, 255, 0.1); transform: translateY(-3px); }
        .ticker-name { color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
        .ticker-price { color: #ffffff; font-size: 1.5rem; font-weight: 700; }
        .pos { color: #10b981; } .neg { color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- STABLE SCRAPING LOGIC ---
@st.cache_data(ttl=60)
def fetch_market_data():
    """Fetches key indices directly from Moneycontrol's summary page."""
    url = "https://www.moneycontrol.com/markets/global-indices/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This targets the main global indices table
        table = soup.find('table', {'class': 'mctable1'})
        rows = table.find_all('tr')[1:] # Skip header
        
        data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 2:
                name = cols[0].text.strip()
                price = cols[1].text.strip()
                change_pct = cols[3].text.strip()
                data.append({"name": name, "price": price, "change": change_pct})
        return data
    except Exception as e:
        return []

# --- UI COMPONENT ---
def draw_card(item):
    val = item['change'].replace('%', '').replace(',', '')
    try:
        is_pos = float(val) >= 0
    except:
        is_pos = True
    
    color_class = "pos" if is_pos else "neg"
    # Mapping to TradingView Search
    tv_url = f"https://www.tradingview.com/chart/?symbol={item['name'].split()[0]}"
    
    st.markdown(f"""
    <a href="{tv_url}" target="_blank" class="market-card">
        <div class="ticker-name">{item['name']}</div>
        <div class="ticker-price">{item['price']}</div>
        <div class="{color_class}">{"▲" if is_pos else "▼"} {item['change']}</div>
    </a>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏛️ Global Market Terminal")
    
    market_data = fetch_market_data()
    
    if market_data:
        cols = st.columns(4)
        for idx, item in enumerate(market_data[:12]): # Show top 12
            with cols[idx % 4]:
                draw_card(item)
    else:
        st.error("Live data feed currently unavailable. Verify connection.")
    
    st.caption(f"Refreshed at: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
