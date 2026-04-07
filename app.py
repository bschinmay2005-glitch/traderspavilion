import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="TradersPavilion | Sectoral Velocity", layout="wide")

# Custom CSS for Branding
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stApp { color: #f1f5f9; }
    h1 { font-weight: 800; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# Branding Header
st.markdown("# Traders<span style='color:#22c55e'>Pavilion</span>", unsafe_allow_html=True)
st.write("### Sectoral Analysis • Previous Close vs Real-time")
st.divider()

@st.cache_data(ttl=60)  # Refresh data every 60 seconds
def fetch_nse_data():
    url = "https://www.nseindia.com/api/allIndices"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        response = session.get(url, headers=headers)
        data = response.json()['data']
        
        # Filter for key sectoral indices
        target_sectors = [
            "NIFTY BANK", "NIFTY IT", "NIFTY AUTO", "NIFTY FMCG", 
            "NIFTY METAL", "NIFTY PHARMA", "NIFTY REALTY", "NIFTY MEDIA"
        ]
        
        processed_data = []
        for item in data:
            if item['index'] in target_sectors:
                processed_data.append({
                    "Sector": item['index'].replace("NIFTY ", ""),
                    "Change %": item['percentChange'],
                    "LTP": item['last'],
                    "Color": "green" if item['percentChange'] >= 0 else "red"
                })
        
        return pd.DataFrame(processed_data).sort_values("Change %", ascending=True)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Execution
df = fetch_nse_data()

if not df.empty:
    # Summary Metrics
    col1, col2 = st.columns(2)
    top_gainer = df.iloc[-1]
    top_loser = df.iloc[0]
    
    col1.metric("Top Outperformer", top_gainer['Sector'], f"{top_gainer['Change %']}%")
    col2.metric("Top Underperformer", top_loser['Sector'], f"{top_loser['Change %']}%", delta_color="inverse")

    # The Chart
    # Streamlit's st.bar_chart is simple, but for conditional colors, we use st.column_config
    st.write("#### Nifty Sectoral Heatmap (%)")
    
    st.bar_chart(
        data=df,
        x="Sector",
        y="Change %",
        color="Color",  # This highlights the Green/Red logic
        horizontal=True,
        height=500
    )

    # Raw Data Table
    with st.expander("View Detailed Prices"):
        st.dataframe(df[["Sector", "LTP", "Change %"]], use_container_width=True)
else:
    st.warning("Waiting for Market Data... Ensure you are running this during market hours.")

st.caption("Data source: NSE India. Analysis starts from previous day closing.")
