import streamlit as st
import requests
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Professional Market Terminal", layout="wide")

# --- STYLES ---
def apply_styles():
    st.markdown("""
    <style>
        .stApp { background: #0b1120; color: #f8fafc; }
        .market-card {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 12px;
        }
        .ticker-name { color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
        .ticker-price { color: #ffffff; font-size: 1.4rem; font-weight: 700; margin-top: 8px; display: block; }
        .pos { color: #10b981; font-weight: 700; }
        .neg { color: #ef4444; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATED DATA FETCHING ---
@st.cache_data(ttl=60)
def fetch_finnhub_data():
    api_key = st.secrets.get("FINNHUB_KEY")
    if not api_key:
        return {"error": "API Key Missing in Secrets"}

    # Tickers: Dow, Nasdaq, S&P, FTSE, DAX, CAC, Nifty (via ETF), Nikkei
    tickers = {
        "DIA": "Dow Jones", "QQQ": "Nasdaq", "SPY": "S&P 500",
        "VGK": "European Mkts", "EPI": "India (Nifty)", "EWJ": "Nikkei 225"
    }
    
    results = {}
    for sym, name in tickers.items():
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={sym}&token={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                d = response.json()
                # d['c'] is current price, d['dp'] is percent change
                results[name] = {
                    "price": f"${d['c']:,.2f}",
                    "change": f"{d['dp']:+.2f}%",
                    "is_pos": d['dp'] >= 0
                }
        except:
            continue
    return results

def draw_card(name, data):
    stats = data.get(name, {"price": "N/A", "change": "0.00%", "is_pos": True})
    color_class = "pos" if stats['is_pos'] else "neg"
    
    st.markdown(f"""
        <div class="market-card">
            <div class="ticker-name">{name}</div>
            <span class="ticker-price">{stats['price']}</span>
            <span class="{color_class}">{stats['change']}</span>
        </div>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.title("🏦 Institutional Market Terminal")
    
    data = fetch_finnhub_data()
    
    if "error" in data:
        st.error(data["error"])
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🇺🇸 US Markets")
        for m in ["Dow Jones", "Nasdaq", "S&P 500"]: draw_card(m, data)
    with c2:
        st.subheader("🇪🇺 European Markets")
        draw_card("European Mkts", data)
    with c3:
        st.subheader("🌏 Asian Markets")
        for m in ["India (Nifty)", "Nikkei 225"]: draw_card(m, data)

if __name__ == "__main__":
    main()
