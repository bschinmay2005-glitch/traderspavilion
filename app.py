import streamlit as st
from SmartApi import SmartConnect
import pyotp
import pandas as pd
from datetime import datetime

# --- CONFIGURATION (Use st.secrets in production!) ---
# For now, you can fill these in to test, but don't commit them to a public GitHub!
API_KEY = "YOUR_API_KEY"
CLIENT_ID = "YOUR_CLIENT_ID"
PASSWORD = "YOUR_PIN"
TOTP_KEY = "YOUR_26_DIGIT_SEED_KEY" # Get this from Angel One 'Enable TOTP' page

# --- 1. ANGEL ONE SESSION ENGINE ---
@st.cache_resource
def get_angel_session():
    try:
        obj = SmartConnect(api_key=API_KEY)
        # Generate current TOTP code
        token = pyotp.TOTP(TOTP_KEY.replace(" ", "")).now()
        session = obj.generateSession(CLIENT_ID, PASSWORD, token)
        
        if session['status']:
            return obj
        else:
            st.error(f"Login failed: {session['message']}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- 2. THE DATA FETCH ENGINE ---
def get_market_data(obj):
    # Mapping for common Nifty Indices (Exchange: NSE, Token is unique to Angel One)
    # Note: Tokens can change, but these are standard for Spot Indices
    indices = {
        "Nifty 50": {"symbol": "Nifty 50", "token": "99926000"},
        "Nifty Bank": {"symbol": "Nifty Bank", "token": "99926037"},
        "Nifty IT": {"symbol": "Nifty IT", "token": "99926017"},
        "Nifty Pharma": {"symbol": "Nifty Pharma", "token": "99926018"}
    }
    
    results = []
    for name, info in indices.items():
        try:
            # Fetch Last Traded Price (LTP)
            data = obj.ltpData("NSE", info['symbol'], info['token'])
            if data['status']:
                ltp = data['data']['ltp']
                # Calculate change (Angel One doesn't always give % in ltpData, 
                # you'd normally fetch 'Open' to calculate this)
                results.append({"name": name, "price": ltp})
        except:
            continue
    return results

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="traderspavilion", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .card {
        background: #1e222d; border: 1px solid #363c4e;
        border-radius: 10px; padding: 20px; text-align: center;
    }
    .price { font-size: 1.8rem; font-weight: bold; color: #00ff88; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# traders<span style='color:#22c55e'>pavilion</span> ⚡", unsafe_allow_html=True)
st.title("⚡ Angel One Live Dashboard")

# Initialize Session
smart_api = get_angel_session()

if smart_api:
    market_data = get_market_data(smart_api)
    
    if market_data:
        cols = st.columns(len(market_data))
        for i, item in enumerate(market_data):
            with cols[i]:
                st.markdown(f"""
                    <div class="card">
                        <div style="color:gray; font-size:0.8rem;">{item['name']}</div>
                        <div class="price">₹{item['price']:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Connected to Angel One, but failed to fetch prices.")
    
    if st.button("Manual Refresh"):
        st.rerun()
else:
    st.info("Waiting for API Connection... Check your Credentials and TOTP Key.")

st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")
