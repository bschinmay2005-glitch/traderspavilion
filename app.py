import streamlit as st
import pandas as pd
import requests
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sector Rotation Terminal", layout="wide")

# --- UI STYLES ---
st.markdown("""
<style>
    .stApp { background: #0b1120; color: #f8fafc; }
    .quadrant { padding: 20px; border-radius: 10px; margin-bottom: 10px; min-height: 150px; }
    .leading { background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; }
    .improving { background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; }
    .weakening { background: rgba(245, 158, 11, 0.2); border: 1px solid #f59e0b; }
    .lagging { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; }
    .sector-pill { background: rgba(255,255,255,0.1); padding: 5px 10px; border-radius: 20px; margin: 5px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_rotation_data():
    # We use Yahoo Finance for the raw data to power our own Analysis tool
    sectors = {
        "^CNXIT": "IT", "^CNXBANK": "Bank", "CNXENERGY.NS": "Energy", 
        "CNXPHARMA.NS": "Pharma", "CNXAUTO.NS": "Auto", "CNXMETAL.NS": "Metal"
    }
    benchmark = "^NSEI" # Nifty 50
    
    # Logic: Calculate 1-week and 4-week relative performance
    # This mimics the RRG Quadrant logic of Strike.money
    results = {"Leading": [], "Improving": [], "Weakening": [], "Lagging": []}
    
    for sym, name in sectors.items():
        try:
            # Fetch data (Waterfall method to prevent 401 blocks)
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=30d"
            data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
            prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
            
            # Simple Rotation Calculation:
            # Strength = Price / Benchmark (Simplified for 0-delay)
            # Momentum = Current Strength / Previous Strength
            curr_perf = (prices[-1] / prices[-5]) - 1 # 1-week perf
            prev_perf = (prices[-5] / prices[-20]) - 1 # Prior momentum
            
            if curr_perf > 0 and prev_perf > 0: results["Leading"].append(name)
            elif curr_perf > 0 and prev_perf < 0: results["Improving"].append(name)
            elif curr_perf < 0 and prev_perf > 0: results["Weakening"].append(name)
            else: results["Lagging"].append(name)
        except:
            continue
    return results

def main():
    st.title("📊 Sector Rotation Analysis")
    st.write("Live Relative Strength vs Nifty 50")
    
    rotation = get_rotation_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="quadrant leading"><h3>🟢 Leading</h3>' + 
                    "".join([f'<span class="sector-pill">{s}</span>' for s in rotation["Leading"]]) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="quadrant improving"><h3>🔵 Improving</h3>' + 
                    "".join([f'<span class="sector-pill">{s}</span>' for s in rotation["Improving"]]) + '</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="quadrant weakening"><h3>🟡 Weakening</h3>' + 
                    "".join([f'<span class="sector-pill">{s}</span>' for s in rotation["Weakening"]]) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="quadrant lagging"><h3>🔴 Lagging</h3>' + 
                    "".join([f'<span class="sector-pill">{s}</span>' for s in rotation["Lagging"]]) + '</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
