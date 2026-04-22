import streamlit as st
import pandas as pd
import requests
import numpy as np
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="RRG Sector Rotation Pro", layout="wide")

# --- UI THEME (Institutional Dark) ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #080c14; color: #e2e8f0; }
        .q-card { 
            padding: 20px; border-radius: 12px; margin-bottom: 20px; 
            min-height: 220px; border: 1px solid rgba(255,255,255,0.05);
        }
        .leading { background: rgba(0, 255, 127, 0.05); border-top: 4px solid #00ff7f; }
        .improving { background: rgba(0, 191, 255, 0.05); border-top: 4px solid #00bfff; }
        .weakening { background: rgba(255, 215, 0, 0.05); border-top: 4px solid #ffd700; }
        .lagging { background: rgba(255, 69, 0, 0.05); border-top: 4px solid #ff4500; }
        
        .sector-tag {
            display: inline-block; background: #1e293b; color: white;
            padding: 6px 12px; border-radius: 6px; margin: 4px;
            font-size: 0.85rem; font-weight: 600; border: 1px solid #334155;
        }
        .header-title { font-size: 1.5rem; font-weight: 800; color: #f8fafc; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- THE RRG MATH ENGINE ---
@st.cache_data(ttl=300)
def get_rrg_data():
    sectors = {
        "^CNXIT": "IT", "^CNXBANK": "Bank", "CNXAUTO.NS": "Auto",
        "CNXPHARMA.NS": "Pharma", "CNXMETAL.NS": "Metal", "CNXFMCG.NS": "FMCG",
        "CNXREALTY.NS": "Realty", "CNXENERGY.NS": "Energy", "CNXINFRA.NS": "Infra"
    }
    benchmark = "^NSEI" # Nifty 50
    
    results = {"Leading": [], "Improving": [], "Lagging": [], "Weakening": []}
    headers = {"User-Agent": "Mozilla/5.0"}

    def fetch_series(ticker):
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=100d"
        data = requests.get(url, headers=headers, timeout=10).json()
        return np.array(data['chart']['result'][0]['indicators']['quote'][0]['close'])

    try:
        bench_close = fetch_series(benchmark)
        
        for sym, name in sectors.items():
            try:
                sec_close = fetch_series(sym)
                
                # 1. Calculate Relative Strength (RS)
                rs = (sec_close / bench_close) * 100
                
                # 2. RS-Ratio (Trend of RS) - Simplified JDK 
                # Comparing 10-day moving average to 40-day
                rs_ratio = (pd.Series(rs).rolling(10).mean() / pd.Series(rs).rolling(40).mean()).iloc[-1] * 100
                
                # 3. RS-Momentum (Rate of change of RS-Ratio)
                rs_momentum = (rs_ratio / (pd.Series(rs).rolling(10).mean() / pd.Series(rs).rolling(40).mean()).iloc[-5]) * 100

                # 4. Quadrant Logic (RRG Standard)
                if rs_ratio > 100 and rs_momentum > 100: results["Leading"].append(name)
                elif rs_ratio < 100 and rs_momentum > 100: results["Improving"].append(name)
                elif rs_ratio < 100 and rs_momentum < 100: results["Lagging"].append(name)
                elif rs_ratio > 100 and rs_momentum < 100: results["Weakening"].append(name)
            except: continue
    except: pass
    return results

def main():
    apply_styles()
    st.markdown('<div class="header-title">📊 Sector Rotation (RRG) Independent Replica</div>', unsafe_allow_html=True)
    st.write("Relative Strength & Momentum vs Nifty 50")

    data = get_rrg_data()

    # RRG Grid Layout
    col1, col2 = st.columns(2)

    with col1:
        # Improving (Top Left)
        st.markdown('<div class="q-card improving"><h4>🔵 IMPROVING</h4>' + 
                    "".join([f'<div class="sector-tag">{s}</div>' for s in data["Improving"]]) + '</div>', unsafe_allow_html=True)
        # Leading (Top Right)
        st.markdown('<div class="q-card leading"><h4>🟢 LEADING</h4>' + 
                    "".join([f'<div class="sector-tag">{s}</div>' for s in data["Leading"]]) + '</div>', unsafe_allow_html=True)

    with col2:
        # Lagging (Bottom Left)
        st.markdown('<div class="q-card lagging"><h4>🔴 LAGGING</h4>' + 
                    "".join([f'<div class="sector-tag">{s}</div>' for s in data["Lagging"]]) + '</div>', unsafe_allow_html=True)
        # Weakening (Bottom Right)
        st.markdown('<div class="q-card weakening"><h4>🟡 WEAKENING</h4>' + 
                    "".join([f'<div class="sector-tag">{s}</div>' for s in data["Weakening"]]) + '</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
