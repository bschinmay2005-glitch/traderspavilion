import streamlit as st
from NorenRestApiPy.NorenApi import NorenApi # pip install NorenRestApiPy
from datetime import datetime
import pandas as pd

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="traderspavilion PRO", page_icon="⚡", layout="wide")

# --- 2. THE API CLASS ---
class ShoonyaApi(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWSTree/', 
                         websocket='wss://api.shoonya.com/NorenWSTree/')

# --- 3. CSS (Your original styling) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top left, #1a1c2c, #4a192c); }
    .market-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease;
        text-decoration: none !important;
        display: block;
        margin-bottom: 20px;
    }
    .market-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); border-color: #22c55e; }
    .symbol-name { font-size: 0.8rem; color: #888ea8; font-weight: 600; text-transform: uppercase; }
    .price { font-size: 1.4rem; font-weight: 700; color: white; margin: 5px 0; }
    .change-pos { color: #00ff88; font-size: 0.85rem; font-weight: bold; }
    .change-neg { color: #ff3b3b; font-size: 0.85rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONFIGURATION (Official Exchange Tokens for 0-Delay) ---
# Tokens are how the exchange identifies indices. These never change.
INDIA_SECTORS = {
    "Nifty 50": {"t": "26000", "tv": "NSE:NIFTY"},
    "Bank Nifty": {"t": "26001", "tv": "NSE:BANKNIFTY"},
    "Nifty IT": {"t": "26002", "tv": "NSE:CNXIT"},
    "Nifty Pharma": {"t": "26005", "tv": "NSE:CNXPHARMA"},
    "Nifty Auto": {"t": "26004", "tv": "NSE:CNXAUTO"},
    "Nifty Metal": {"t": "26008", "tv": "NSE:CNXMETAL"},
    "Nifty FMCG": {"t": "26006", "tv": "NSE:CNXFMCG"},
    "Nifty Realty": {"t": "26011", "tv": "NSE:CNXREALTY"},
    "Nifty Energy": {"t": "26009", "tv": "NSE:CNXENERGY"},
    "Nifty Infra": {"t": "26012", "tv": "NSE:CNXINFRA"},
    "Nifty PSU Bank": {"t": "26013", "tv": "NSE:CNXPSUBANK"},
    "Nifty Pvt Bank": {"t": "26014", "tv": "NSE:NIFTY_PVT_BANK"},
    "Nifty Media": {"t": "26010", "tv": "NSE:CNXMEDIA"},
    "Nifty PSE": {"t": "26015", "tv": "NSE:CPSE"},
    "Nifty Fin Service": {"t": "26007", "tv": "NSE:CNXFINANCE"},
    "Nifty Service": {"t": "26017", "tv": "NSE:CNXSERVICE"},
    "Nifty Commodities": {"t": "26018", "tv": "NSE:CNXCOMMODITIES"},
    "Nifty Consumption": {"t": "26019", "tv": "NSE:CNXCONSUMPTION"},
    "Nifty Healthcare": {"t": "26030", "tv": "NSE:CNXHEALTHCARE"},
    "Nifty Oil & Gas": {"t": "26031", "tv": "NSE:CNXOILGAS"},
    "Nifty Mfg": {"t": "26021", "tv": "NSE:CNXMANUFACTURING"},
    "Nifty Defence": {"t": "26040", "tv": "NSE:DEFENCE"}
}

# --- 5. DATA ENGINE ---
def fetch_realtime_data(api_instance):
    data_list = []
    for name, info in INDIA_SECTORS.items():
        try:
            # lp = Last Price, pc = Percentage Change
            quote = api_instance.get_quotes(exch='NSE', token=info['t'])
            if quote and 'lp' in quote:
                data_list.append({
                    "name": name,
                    "price": float(quote['lp']),
                    "change": float(quote['pc']),
                    "tv_id": info['tv']
                })
        except: continue
    return data_list

# --- 6. SIDEBAR & LOGIN ---
with st.sidebar:
    st.markdown("# traders<span style='color:#22c55e'>pavilion</span> ⚡")
    st.caption("REAL-TIME BROKER FEED")
    st.divider()
    
    # In a real app, use st.secrets or environment variables for these
    u_id = st.text_input("Shoonya User ID")
    u_pwd = st.text_input("Password", type="password")
    u_pan = st.text_input("PAN / DOB (YYYYMMDD)")
    u_apikey = st.text_input("API Key")
    u_imei = st.text_input("IMEI / Vendor Code")
    
    login_btn = st.button("🚀 CONNECT LIVE FEED")

# --- 7. MAIN UI ---
if login_btn:
    api = ShoonyaApi()
    login_status = api.login(user=u_id, pwd=u_pwd, dob=u_pan, as_id=u_apikey, api_key=u_apikey, imei=u_imei)
    
    if login_status and login_status.get('stat') == 'Ok':
        st.success(f"Connected to NSE Real-Time Feed at {datetime.now().strftime('%H:%M:%S')}")
        
        # Display Cards
        data = fetch_realtime_data(api)
        cols = st.columns(4)
        for i, item in enumerate(data):
            with cols[i % 4]:
                color = "change-pos" if item['change'] >= 0 else "change-neg"
                arrow = "▲" if item['change'] >= 0 else "▼"
                url = f"https://www.tradingview.com/symbols/{item['tv_id']}"
                
                st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration:none">
                        <div class="market-card">
                            <div class="symbol-name">{item['name']}</div>
                            <div class="price">{item['price']:,.2f}</div>
                            <div class="{color}">{arrow} {abs(item['change']):.2f}%</div>
                        </div>
                    </a>""", unsafe_allow_html=True)
    else:
        st.error("Login Failed. Check your Shoonya Credentials.")
else:
    st.info("Enter your Shoonya credentials in the sidebar to start the 0-delay feed.")
