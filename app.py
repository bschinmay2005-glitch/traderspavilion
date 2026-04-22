import streamlit as st
import pandas as pd
from moneycontrol import moneycontrol_api  # Note the _api suffix
import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(
    page_title="FinTech Market Bar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (SaaS Dark Mode & Glassmorphism) ---
def apply_custom_styles():
    st.markdown("""
    <style>
        /* Main Container */
        .stApp {
            background: radial-gradient(circle at top left, #1e293b, #0f172a);
            color: #e2e8f0;
        }

        /* Glassmorphism Card Logic */
        .market-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 120px;
        }

        .market-card:hover {
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.25);
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }

        /* Text Styles */
        .ticker-name { color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
        .ticker-price { color: #ffffff; font-size: 1.6rem; font-weight: 700; margin-top: 0.2rem; }
        .change-pos { color: #10b981; font-size: 0.95rem; font-weight: 600; }
        .change-neg { color: #ef4444; font-size: 0.95rem; font-weight: 600; }
        
        /* Hide Streamlit Header/Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATA WRAPPER ---
@st.cache_data(ttl=30) # Cache for 30 seconds for "real-time" feel
def get_live_data(category):
    mc = moneycontrol()
    try:
        if category == "Global":
            return mc.get_global_indices()
        elif category == "Forex":
            return mc.get_currencies()
        elif category == "Commodities":
            return mc.get_commodities()
    except Exception as e:
        return pd.DataFrame()

# --- HELPER: CARD GENERATOR ---
def draw_market_card(name, current_price, prev_close):
    # Logic for % Change based on Timeframe
    # Note: For true Day/Week/Month logic, historical data arrays are required.
    # Here we implement the 'Day' logic based on Previous Close.
    try:
        curr = float(str(current_price).replace(',', ''))
        prev = float(str(prev_close).replace(',', ''))
        pct_change = ((curr - prev) / prev) * 100
    except (ValueError, ZeroDivisionError):
        pct_change = 0.0

    change_class = "change-pos" if pct_change >= 0 else "change-neg"
    change_arrow = "▲" if pct_change >= 0 else "▼"
    
    # Dynamic TradingView Link (Basic Ticker mapping)
    clean_name = name.split()[0].replace('/', '')
    tv_url = f"https://www.tradingview.com/chart/?symbol={clean_name}"

    card_html = f"""
    <a href="{tv_url}" target="_blank" class="market-card">
        <div class="ticker-name">{name}</div>
        <div class="ticker-price">{current_price}</div>
        <div class="{change_class}">{change_arrow} {abs(pct_change):.2f}%</div>
    </a>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
def main():
    apply_custom_styles()
    
    # Top Bar
    col_title, col_time = st.columns([2, 1])
    with col_title:
        st.title("Market Terminal")
    with col_time:
        timeframe = st.selectbox(
            "Timeframe", 
            ["Intraday (Real-time)", "Weekly", "Monthly", "Yearly"],
            label_visibility="collapsed"
        )

    # Categories Logic
    tabs = st.tabs(["🌎 Global Indices", "📦 Commodities", "💱 Forex"])
    
    categories = ["Global", "Commodities", "Forex"]
    
    for i, tab in enumerate(tabs):
        with tab:
            df = get_live_data(categories[i])
            if not df.empty:
                # Grid system: 4 cards per row
                cols = st.columns(4)
                for index, row in df.iterrows():
                    with cols[index % 4]:
                        draw_market_card(
                            name=row.get('name', 'N/A'),
                            current_price=row.get('last_price', '0.00'),
                            prev_close=row.get('prev_close', row.get('last_price', '0.00'))
                        )
            else:
                st.warning(f"No live data available for {categories[i]}. Check API connection.")

    # Auto-refresh helper
    st.caption(f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
