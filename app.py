import streamlit as st
from SmartApi import SmartConnect
import pyotp
import pandas as pd

# --- 1. LOGIN CREDENTIALS ---
# PRO-TIP: Put these in Streamlit Secrets, NOT in the code!
API_KEY = "YOUR_API_KEY"
CLIENT_ID = "YOUR_CLIENT_ID"
PASSWORD = "YOUR_PASSWORD"
TOTP_KEY = "YOUR_TOTP_SEED_KEY" # The key you get when enabling TOTP

def get_angel_data():
    try:
        # Initialize Angel One Connection
        obj = SmartConnect(api_key=API_KEY)
        token = pyotp.TOTP(TOTP_KEY).now()
        data = obj.generateSession(CLIENT_ID, PASSWORD, token)
        
        # Fetching Nifty 50 Spot Price
        # Exchange: NSE, Token: 99926000 (Standard for Nifty 50)
        ltp_data = obj.ltpData("NSE", "Nifty 50", "99926000")
        return ltp_data['data']['ltp']
    except Exception as e:
        st.error(f"Angel One Login Failed: {e}")
        return None

# --- 2. UI ---
st.title("⚡ traderspavilion: Angel One Feed")

price = get_angel_data()
if price:
    st.metric(label="NIFTY 50", value=f"₹{price:,.2f}")
