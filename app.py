import streamlit as st
from SmartApi import SmartConnect
import pyotp
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# --- CONFIGURATION ---
# It is better to use st.sidebar for keys so they aren't hardcoded
st.sidebar.title("🔑 API Authentication")
API_KEY = st.sidebar.text_input("Angel One API Key", type="password")
CLIENT_ID = st.sidebar.text_input("Client ID (e.g. S12345)")
PASSWORD = st.sidebar.text_input("Login PIN", type="password")
TOTP_KEY = st.sidebar.text_input("26-Digit TOTP Seed", type="password")

BULLISH_WORDS = ["SURGE", "JUMP", "PROFIT", "RECORDS", "GROWTH", "BULLISH", "UP", "GAINS"]
BEARISH_WORDS = ["CRASH", "PLUNGE", "LOSS", "DEBT", "FALL", "SLUMP", "DOWN", "WAR"]

# --- 1. ANGEL ONE ENGINE ---
@st.cache_resource
def get_angel_session(_api_key, _client_id, _password, _totp_key):
    if not all([_api_key, _client_id, _password, _totp_key]):
        return None
    try:
        obj = SmartConnect(api_key=_api_key)
        # Generate TOTP on the fly
        token = pyotp.TOTP(_totp_key.replace(" ", "")).now()
        session = obj.generateSession(_client_id, _password, token)
        if session.get('status'):
            return obj
        return None
    except Exception as e:
        st.sidebar.error(f"Login Error: {e}")
        return None

# --- 2. NEWS SCRAPER (MONEYCONTROL SITEMAP) ---
def fetch_news():
    url = "https://www.moneycontrol.com/news/news-sitemap.xml"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.content, 'xml')
        news_data = []
        # Pulling latest 20 headlines
        for entry in soup.find_all('url')[:20]:
            title = entry.find('news:title').text
            link = entry.find('loc').text
            
            # Impact Sentiment
            title_up = title.upper()
            impact = "bullish" if any(w in title_up for w in BULLISH_WORDS) else \
                     "bearish" if any(w in title_up for w in BEARISH_WORDS) else "neutral"
            
            news_data.append({"title": title, "link": link, "impact": impact})
        return news_data
    except:
        return []

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Market Shaker 2026", layout="wide")
st.title("🏛️ Market Shaker: Rebuilt 2026")

# TOP ROW: LIVE PRICES
smart_api = get_angel_session(API_KEY, CLIENT_ID, PASSWORD, TOTP_KEY)

if smart_api:
    st.subheader("⚡ Live Sector Watch")
    cols = st.columns(4)
    # Using official Angel One tokens for Nifty Indices
    indices = [
        ("Nifty 50", "99926000"), ("Bank Nifty", "99926037"), 
        ("Nifty IT", "99926017"), ("Nifty Pharma", "99926018")
    ]
    
    for i, (name, token) in enumerate(indices):
        res = smart_api.ltpData("NSE", name, token)
        if res.get('status'):
            price = res['data']['ltp']
            cols[i].metric(label=name, value=f"₹{price:,.2f}")
else:
    st.warning("Please enter your Angel One API details in the sidebar to load live prices.")

st.divider()

# BOTTOM SECTION: NEWS UPDATES
st.subheader("📰 Sentiment Archive (Auto-Refresh)")

@st.fragment(run_every=60)
def news_ui():
    news_items = fetch_news()
    if not news_items:
        st.info("Searching for fresh market updates...")
    
    for item in news_items:
        # Dynamic Styling based on Impact
        border_color = "#28a745" if item['impact'] == "bullish" else "#dc3545" if item['impact'] == "bearish" else "#444c56"
        badge_text = "🟢 POSITIVE" if item['impact'] == "bullish" else "🔴 NEGATIVE" if item['impact'] == "bearish" else "⚪ NEUTRAL"
        
        st.markdown(f"""
            <div style="border-left: 6px solid {border_color}; background-color: #161b22; padding: 15px; margin-bottom: 12px; border-radius: 8px;">
                <small style="color: {border_color}; font-weight: bold;">{badge_text}</small>
                <h4 style="margin: 5px 0; color: white;">{item['title']}</h4>
                <a href="{item['link']}" target="_blank" style="text-decoration: none; color: #58a6ff; font-size: 0.85rem;">Read Investigation →</a>
            </div>
        """, unsafe_allow_html=True)

news_ui()
