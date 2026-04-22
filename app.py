import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLASSMORPHISM CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-primary: #050810;
    --bg-secondary: #0a0f1e;
    --glass-bg: rgba(255,255,255,0.04);
    --glass-border: rgba(255,255,255,0.08);
    --glass-hover: rgba(255,255,255,0.07);
    --accent-green: #00e676;
    --accent-red: #ff1744;
    --accent-blue: #2979ff;
    --accent-gold: #ffd740;
    --text-primary: #e8eaf6;
    --text-secondary: #7986cb;
    --text-muted: #4a5280;
    --font-mono: 'Space Mono', monospace;
    --font-sans: 'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--font-sans);
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background: radial-gradient(ellipse at 10% 20%, rgba(41,121,255,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 80%, rgba(0,230,118,0.05) 0%, transparent 50%),
                var(--bg-primary);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(10,15,30,0.95) !important;
    border-right: 1px solid var(--glass-border);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p {
    color: var(--text-secondary) !important;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: var(--font-mono);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: var(--text-primary) !important;
}

/* Selectbox & Radio */
.stSelectbox > div > div {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-sans);
}
.stRadio > div {
    gap: 6px;
}
.stRadio > div > label {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 6px;
    padding: 4px 12px;
    transition: all 0.2s ease;
    font-family: var(--font-mono);
    font-size: 0.75rem !important;
}
.stRadio > div > label:hover {
    border-color: var(--accent-blue);
    background: rgba(41,121,255,0.1);
}

/* Header */
.dash-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 24px 0;
    border-bottom: 1px solid var(--glass-border);
    margin-bottom: 28px;
}
.dash-title {
    font-family: var(--font-mono);
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    margin: 0;
}
.dash-title span { color: var(--accent-blue); }
.dash-subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
    letter-spacing: 0.1em;
    margin-top: 4px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,230,118,0.08);
    border: 1px solid rgba(0,230,118,0.2);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.7rem;
    font-family: var(--font-mono);
    color: var(--accent-green);
    letter-spacing: 0.1em;
}
.live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-green);
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(0.8); }
}

/* Sector Tab Headers */
.sector-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 18px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 10px 10px 0 0;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    margin-top: 16px;
    border-bottom: none;
}
.sector-icon { font-size: 1rem; }

/* Market Bars */
.market-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 10px;
    padding: 14px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--glass-border);
    border-radius: 0 0 10px 10px;
    margin-bottom: 6px;
}
.market-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 15px;
    border-radius: 8px;
    border: 1px solid transparent;
    backdrop-filter: blur(10px);
    transition: all 0.2s ease;
    text-decoration: none !important;
    position: relative;
    overflow: hidden;
}
.market-bar::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
}
.market-bar.green {
    background: rgba(0,230,118,0.05);
    border-color: rgba(0,230,118,0.12);
}
.market-bar.green::before { background: var(--accent-green); }
.market-bar.red {
    background: rgba(255,23,68,0.05);
    border-color: rgba(255,23,68,0.12);
}
.market-bar.red::before { background: var(--accent-red); }
.market-bar.neutral {
    background: var(--glass-bg);
    border-color: var(--glass-border);
}
.market-bar.neutral::before { background: var(--text-muted); }
.market-bar:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.market-bar.green:hover { border-color: rgba(0,230,118,0.3); }
.market-bar.red:hover   { border-color: rgba(255,23,68,0.3); }

.bar-left { flex: 1; min-width: 0; }
.bar-name {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: var(--font-sans);
    line-height: 1.3;
}
.bar-ticker {
    font-size: 0.65rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
    letter-spacing: 0.06em;
    margin-top: 2px;
}
.bar-right { text-align: right; flex-shrink: 0; margin-left: 12px; }
.bar-price {
    font-size: 0.88rem;
    font-weight: 700;
    font-family: var(--font-mono);
    color: var(--text-primary);
}
.bar-change {
    font-size: 0.72rem;
    font-family: var(--font-mono);
    font-weight: 700;
    margin-top: 2px;
    padding: 1px 6px;
    border-radius: 4px;
    display: inline-block;
}
.bar-change.green { color: var(--accent-green); background: rgba(0,230,118,0.1); }
.bar-change.red   { color: var(--accent-red);   background: rgba(255,23,68,0.1); }
.bar-change.neutral { color: var(--text-muted); background: rgba(255,255,255,0.05); }

/* Stat Cards */
.stat-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 10px;
    padding: 16px 20px;
    backdrop-filter: blur(10px);
}
.stat-label {
    font-size: 0.68rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.stat-value {
    font-size: 1.4rem;
    font-weight: 700;
    font-family: var(--font-mono);
    color: var(--text-primary);
}
.stat-sub {
    font-size: 0.72rem;
    font-family: var(--font-mono);
    margin-top: 4px;
}

/* Loading */
.loading-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 20px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.8rem;
}
.spinner {
    width: 16px; height: 16px;
    border: 2px solid var(--glass-border);
    border-top-color: var(--accent-blue);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Divider */
.glass-divider {
    border: none;
    border-top: 1px solid var(--glass-border);
    margin: 20px 0;
}

/* Stagger animation */
.market-bar { animation: fadeUp 0.3s ease both; }
@keyframes fadeUp {
    from { opacity:0; transform: translateY(8px); }
    to   { opacity:1; transform: translateY(0); }
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 2px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--glass-bg);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--glass-border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: var(--text-secondary) !important;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    padding: 6px 14px;
}
.stTabs [aria-selected="true"] {
    background: rgba(41,121,255,0.15) !important;
    color: var(--accent-blue) !important;
    border-color: rgba(41,121,255,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 16px;
}

/* No data message */
.no-data {
    padding: 30px;
    text-align: center;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.8rem;
    border: 1px dashed var(--glass-border);
    border-radius: 8px;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─── MARKET DATA DEFINITIONS ─────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def get_market_universe():
    return {
        "Asia": {
            "🇮🇳 India": {
                "Banking": [
                    ("HDFC Bank", "HDFCBANK.NS"), ("ICICI Bank", "ICICIBANK.NS"),
                    ("State Bank", "SBIN.NS"), ("Kotak Bank", "KOTAKBANK.NS"),
                    ("Axis Bank", "AXISBANK.NS"), ("IndusInd Bank", "INDUSINDBK.NS"),
                ],
                "Technology": [
                    ("TCS", "TCS.NS"), ("Infosys", "INFY.NS"),
                    ("Wipro", "WIPRO.NS"), ("HCL Tech", "HCLTECH.NS"),
                    ("Tech Mahindra", "TECHM.NS"), ("LTIMindtree", "LTIM.NS"),
                ],
                "Energy": [
                    ("Reliance", "RELIANCE.NS"), ("ONGC", "ONGC.NS"),
                    ("NTPC", "NTPC.NS"), ("Power Grid", "POWERGRID.NS"),
                    ("Adani Power", "ADANIPOWER.NS"),
                ],
                "Auto": [
                    ("Maruti Suzuki", "MARUTI.NS"), ("Tata Motors", "TATAMOTORS.NS"),
                    ("M&M", "M&M.NS"), ("Bajaj Auto", "BAJAJ-AUTO.NS"),
                ],
                "FMCG": [
                    ("HUL", "HINDUNILVR.NS"), ("ITC", "ITC.NS"),
                    ("Nestle India", "NESTLEIND.NS"), ("Dabur", "DABUR.NS"),
                ],
                "Healthcare": [
                    ("Sun Pharma", "SUNPHARMA.NS"), ("Dr Reddy's", "DRREDDY.NS"),
                    ("Cipla", "CIPLA.NS"), ("Divi's Lab", "DIVISLAB.NS"),
                ],
            },
            "🇯🇵 Japan": {
                "Technology": [
                    ("Sony Group", "6758.T"), ("Toyota Motor", "7203.T"),
                    ("SoftBank", "9984.T"), ("Keyence", "6861.T"),
                ],
                "Banking": [
                    ("Mitsubishi UFJ", "8306.T"), ("Sumitomo Mitsui", "8316.T"),
                    ("Mizuho Financial", "8411.T"),
                ],
                "Industry": [
                    ("Panasonic", "6752.T"), ("Hitachi", "6501.T"),
                    ("Fanuc", "6954.T"),
                ],
            },
            "🇨🇳 China": {
                "Technology": [
                    ("Alibaba", "BABA"), ("Tencent (ADR)", "TCEHY"),
                    ("JD.com", "JD"), ("Baidu", "BIDU"),
                    ("NetEase", "NTES"),
                ],
                "Banking": [
                    ("ICBC (ADR)", "IDCBY"), ("China Construction (ADR)", "CICHY"),
                ],
                "EV / Auto": [
                    ("NIO", "NIO"), ("Li Auto", "LI"),
                    ("XPeng", "XPEV"),
                ],
            },
            "🇰🇷 South Korea": {
                "Technology": [
                    ("Samsung (ADR)", "SSNLF"), ("SK Hynix (ADR)", "HXSCL"),
                    ("LG Electronics (ADR)", "LGFRY"),
                ],
                "Auto": [
                    ("Hyundai Motor (ADR)", "HYMTF"), ("Kia Corp (ADR)", "KIMTF"),
                ],
            },
            "🇸🇬 Singapore": {
                "Banking": [
                    ("DBS Group (ADR)", "DBSDY"), ("OCBC (ADR)", "OVCHY"),
                    ("UOB (ADR)", "UOVEY"),
                ],
                "Real Estate": [
                    ("CapitaLand (ADR)", "CLLDY"),
                ],
            },
            "🇭🇰 Hong Kong": {
                "Finance": [
                    ("HSBC", "HSBC"), ("AIA Group (ADR)", "AAGIY"),
                ],
                "Property": [
                    ("Sun Hung Kai (ADR)", "SUHJY"), ("CK Hutchison (ADR)", "CKHUY"),
                ],
            },
        },
        "Europe": {
            "🇬🇧 UK": {
                "Finance": [
                    ("HSBC", "HSBC"), ("Barclays (ADR)", "BCS"),
                    ("Lloyds (ADR)", "LYG"), ("Standard Chartered (ADR)", "SCBFF"),
                ],
                "Energy": [
                    ("Shell", "SHEL"), ("BP", "BP"),
                ],
                "Consumer": [
                    ("Unilever", "UL"), ("GSK", "GSK"),
                    ("AstraZeneca", "AZN"),
                ],
            },
            "🇩🇪 Germany": {
                "Auto": [
                    ("Volkswagen (ADR)", "VWAGY"), ("BMW (ADR)", "BMWYY"),
                    ("Mercedes-Benz (ADR)", "MBGYY"),
                ],
                "Industry": [
                    ("Siemens (ADR)", "SIEGY"), ("BASF (ADR)", "BASFY"),
                    ("SAP", "SAP"),
                ],
                "Finance": [
                    ("Deutsche Bank", "DB"), ("Allianz (ADR)", "ALIZY"),
                ],
            },
            "🇫🇷 France": {
                "Luxury": [
                    ("LVMH (ADR)", "LVMHF"), ("Hermès (ADR)", "HESAY"),
                    ("L'Oréal (ADR)", "LRLCY"), ("Kering (ADR)", "PPRUY"),
                ],
                "Energy": [
                    ("TotalEnergies", "TTE"),
                ],
                "Finance": [
                    ("BNP Paribas (ADR)", "BNPQY"), ("AXA (ADR)", "AXAHY"),
                ],
            },
            "🇨🇭 Switzerland": {
                "Healthcare": [
                    ("Novartis", "NVS"), ("Roche (ADR)", "RHHBY"),
                    ("Nestlé (ADR)", "NSRGY"),
                ],
                "Finance": [
                    ("UBS Group", "UBS"),
                ],
            },
            "🇳🇱 Netherlands": {
                "Technology": [
                    ("ASML", "ASML"),
                ],
                "Energy": [
                    ("Shell", "SHEL"),
                ],
            },
            "🇸🇪 Sweden": {
                "Telecom": [
                    ("Ericsson (ADR)", "ERIC"),
                ],
                "Finance": [
                    ("Nordea (ADR)", "NRDBY"),
                ],
            },
        },
        "Americas": {
            "🇺🇸 USA": {
                "Technology": [
                    ("Apple", "AAPL"), ("Microsoft", "MSFT"),
                    ("NVIDIA", "NVDA"), ("Alphabet", "GOOGL"),
                    ("Meta", "META"), ("Amazon", "AMZN"),
                    ("Tesla", "TSLA"), ("AMD", "AMD"),
                    ("Broadcom", "AVGO"), ("Oracle", "ORCL"),
                    ("Salesforce", "CRM"), ("Palantir", "PLTR"),
                ],
                "Finance": [
                    ("JPMorgan Chase", "JPM"), ("Goldman Sachs", "GS"),
                    ("Visa", "V"), ("Mastercard", "MA"),
                    ("Bank of America", "BAC"), ("Morgan Stanley", "MS"),
                    ("Berkshire B", "BRK-B"), ("Citigroup", "C"),
                ],
                "Healthcare": [
                    ("Johnson & Johnson", "JNJ"), ("Eli Lilly", "LLY"),
                    ("UnitedHealth", "UNH"), ("Pfizer", "PFE"),
                    ("AbbVie", "ABBV"), ("Merck", "MRK"),
                ],
                "Energy": [
                    ("ExxonMobil", "XOM"), ("Chevron", "CVX"),
                    ("ConocoPhillips", "COP"), ("EOG Resources", "EOG"),
                ],
                "Consumer": [
                    ("Walmart", "WMT"), ("Costco", "COST"),
                    ("McDonald's", "MCD"), ("Nike", "NKE"),
                    ("Starbucks", "SBUX"), ("Coca-Cola", "KO"),
                    ("PepsiCo", "PEP"), ("Procter & Gamble", "PG"),
                ],
                "Telecom & Media": [
                    ("Netflix", "NFLX"), ("Comcast", "CMCSA"),
                    ("AT&T", "T"), ("Verizon", "VZ"),
                ],
            },
            "🇨🇦 Canada": {
                "Finance": [
                    ("Royal Bank (ADR)", "RY"), ("TD Bank (ADR)", "TD"),
                    ("Brookfield (ADR)", "BAM"),
                ],
                "Energy": [
                    ("Suncor Energy", "SU"), ("Canadian Natural", "CNQ"),
                ],
            },
            "🇧🇷 Brazil": {
                "Finance": [
                    ("Itaú Unibanco (ADR)", "ITUB"), ("Banco Bradesco (ADR)", "BBD"),
                    ("Nu Holdings", "NU"),
                ],
                "Energy": [
                    ("Petrobras (ADR)", "PBR"),
                ],
                "Materials": [
                    ("Vale (ADR)", "VALE"),
                ],
            },
            "🇲🇽 Mexico": {
                "Telecom": [
                    ("América Móvil (ADR)", "AMX"),
                ],
                "Finance": [
                    ("Grupo Financiero Banorte (ADR)", "GBOOY"),
                ],
            },
        },
        "Middle East & Africa": {
            "🇸🇦 Saudi Arabia": {
                "Energy": [
                    ("Saudi Aramco (ADR)", "ARAMCO.SR"),
                ],
                "Finance": [
                    ("Al Rajhi Bank (ADR)", "RJHI.SR"),
                ],
            },
            "🇿🇦 South Africa": {
                "Finance": [
                    ("Naspers (ADR)", "NPSNY"), ("Standard Bank (ADR)", "SGBLY"),
                ],
                "Mining": [
                    ("Anglo American (ADR)", "NGLOY"),
                ],
            },
            "🇮🇱 Israel": {
                "Technology": [
                    ("Check Point", "CHKP"), ("CyberArk", "CYBR"),
                    ("Nice Systems", "NICE"),
                ],
            },
            "🇦🇪 UAE": {
                "Finance": [
                    ("Emirates NBD (ADR)", "ENBD.AE"),
                ],
            },
        },
        "Pacific": {
            "🇦🇺 Australia": {
                "Mining": [
                    ("BHP Group (ADR)", "BHP"), ("Rio Tinto (ADR)", "RIO"),
                    ("Fortescue (ADR)", "FSUGY"),
                ],
                "Finance": [
                    ("Commonwealth Bank (ADR)", "CMWAY"), ("ANZ (ADR)", "ANZBY"),
                    ("Westpac (ADR)", "WBK"),
                ],
            },
            "🇳🇿 New Zealand": {
                "Telecom": [
                    ("Spark NZ (ADR)", "NZTCY"),
                ],
            },
        },
    }


@st.cache_data(ttl=86400)
def get_commodities():
    return {
        "Energy": [
            ("Crude Oil (WTI)", "CL=F"), ("Brent Crude", "BZ=F"),
            ("Natural Gas", "NG=F"), ("Gasoline RBOB", "RB=F"),
            ("Heating Oil", "HO=F"),
        ],
        "Precious Metals": [
            ("Gold", "GC=F"), ("Silver", "SI=F"),
            ("Platinum", "PL=F"), ("Palladium", "PA=F"),
        ],
        "Base Metals": [
            ("Copper", "HG=F"), ("Aluminum (LME)", "ALI=F"),
            ("Zinc (ADR)", "ZNC=F"),
        ],
        "Agriculture": [
            ("Corn", "ZC=F"), ("Wheat", "ZW=F"),
            ("Soybeans", "ZS=F"), ("Coffee", "KC=F"),
            ("Sugar", "SB=F"), ("Cotton", "CT=F"),
        ],
    }


@st.cache_data(ttl=86400)
def get_crypto():
    return {
        "Large Cap": [
            ("Bitcoin", "BTC-USD"), ("Ethereum", "ETH-USD"),
            ("BNB", "BNB-USD"), ("Solana", "SOL-USD"),
            ("XRP", "XRP-USD"),
        ],
        "Mid Cap": [
            ("Cardano", "ADA-USD"), ("Avalanche", "AVAX-USD"),
            ("Polkadot", "DOT-USD"), ("Chainlink", "LINK-USD"),
            ("Polygon", "MATIC-USD"), ("NEAR Protocol", "NEAR-USD"),
        ],
        "DeFi": [
            ("Uniswap", "UNI-USD"), ("Aave", "AAVE-USD"),
            ("Compound", "COMP-USD"), ("Maker", "MKR-USD"),
        ],
        "Meme & Other": [
            ("Dogecoin", "DOGE-USD"), ("Shiba Inu", "SHIB-USD"),
            ("Pepe", "PEPE-USD"),
        ],
    }


# ─── PRICE FETCHING ──────────────────────────────────────────────────────────
TIMEFRAME_MAP = {
    "Day":   ("1d",  "1m"),
    "Week":  ("5d",  "5m"),
    "Month": ("1mo", "1h"),
    "Year":  ("1y",  "1d"),
}

def fetch_prices(tickers: list[str], timeframe: str) -> dict:
    period, interval = TIMEFRAME_MAP[timeframe]
    results = {}
    if not tickers:
        return results
    try:
        data = yf.download(
            tickers, period=period, interval=interval,
            group_by="ticker", auto_adjust=True,
            progress=False, threads=True
        )
        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    df = data
                else:
                    df = data[ticker] if ticker in data.columns.get_level_values(0) else pd.DataFrame()
                if df.empty or "Close" not in df.columns:
                    results[ticker] = None
                    continue
                closes = df["Close"].dropna()
                if len(closes) < 2:
                    results[ticker] = None
                    continue
                current = float(closes.iloc[-1])
                open_price = float(closes.iloc[0])
                pct_change = ((current - open_price) / open_price) * 100
                results[ticker] = {
                    "price": current,
                    "change_pct": pct_change,
                    "open": open_price,
                }
            except Exception:
                results[ticker] = None
    except Exception:
        for t in tickers:
            results[t] = None
    return results


def format_price(price: float, ticker: str) -> str:
    """Smart price formatting."""
    if price is None:
        return "N/A"
    if price < 0.001:
        return f"${price:.8f}"
    elif price < 1:
        return f"${price:.4f}"
    elif price < 1000:
        return f"${price:,.2f}"
    else:
        return f"${price:,.2f}"


def tradingview_url(ticker: str) -> str:
    """Build a TradingView chart URL for the ticker."""
    clean = ticker.replace(".NS", "").replace(".T", "").replace(".SR", "")
    clean = clean.replace("=F", "").replace("-USD", "").replace("-", "")
    # Commodity mapping
    commodity_map = {
        "CL": "NYMEX:CL1!", "BZ": "TVC:UKOIL", "NG": "NYMEX:NG1!",
        "GC": "COMEX:GC1!", "SI": "COMEX:SI1!", "PL": "NYMEX:PL1!",
        "HG": "COMEX:HG1!", "ZC": "CBOT:ZC1!", "ZW": "CBOT:ZW1!",
        "ZS": "CBOT:ZS1!", "KC": "ICEUS:KC1!",
    }
    for key, val in commodity_map.items():
        if clean.startswith(key):
            return f"https://www.tradingview.com/chart/?symbol={val}"
    # Crypto
    if "-USD" in ticker or ticker in ["BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "AVAX", "DOT", "LINK", "MATIC", "NEAR", "UNI", "AAVE", "COMP", "MKR", "DOGE", "SHIB", "PEPE"]:
        return f"https://www.tradingview.com/chart/?symbol=BINANCE:{clean}USDT"
    # Indian stocks
    if ".NS" in ticker:
        return f"https://www.tradingview.com/chart/?symbol=NSE:{clean}"
    # Japanese
    if ".T" in ticker:
        return f"https://www.tradingview.com/chart/?symbol=TSE:{clean}"
    return f"https://www.tradingview.com/chart/?symbol={clean}"


# ─── RENDER MARKET BARS ───────────────────────────────────────────────────────
def render_sector_bars(sector_name: str, stocks: list, timeframe: str, icon: str = "📊"):
    tickers = [s[1] for s in stocks]
    prices = fetch_prices(tickers, timeframe)

    bars_html = ""
    for i, (name, ticker) in enumerate(stocks):
        info = prices.get(ticker)
        url = tradingview_url(ticker)
        delay = i * 0.03

        if info:
            price_str = format_price(info["price"], ticker)
            pct = info["change_pct"]
            sign = "+" if pct >= 0 else ""
            cls = "green" if pct > 0 else ("red" if pct < 0 else "neutral")
            change_html = f'<span class="bar-change {cls}">{sign}{pct:.2f}%</span>'
        else:
            price_str = "—"
            cls = "neutral"
            change_html = '<span class="bar-change neutral">N/A</span>'

        bars_html += f"""
        <a href="{url}" target="_blank" class="market-bar {cls}" style="animation-delay:{delay}s">
          <div class="bar-left">
            <div class="bar-name">{name}</div>
            <div class="bar-ticker">{ticker}</div>
          </div>
          <div class="bar-right">
            <div class="bar-price">{price_str}</div>
            {change_html}
          </div>
        </a>"""

    st.markdown(f"""
    <div class="sector-header">
        <span class="sector-icon">{icon}</span>
        <span>{sector_name}</span>
        <span style="margin-left:auto;color:var(--text-muted);font-size:0.7rem">{len(stocks)} instruments</span>
    </div>
    <div class="market-grid">{bars_html}</div>
    """, unsafe_allow_html=True)


# ─── SIDEBAR NAVIGATION ───────────────────────────────────────────────────────
CONTINENT_ICONS = {
    "Asia": "🌏", "Europe": "🌍", "Americas": "🌎",
    "Middle East & Africa": "🌍", "Pacific": "🌊",
}
SECTOR_ICONS = {
    "Banking": "🏦", "Finance": "💰", "Technology": "💻",
    "Energy": "⚡", "Auto": "🚗", "EV / Auto": "⚡🚗",
    "FMCG": "🛒", "Healthcare": "💊", "Industry": "🏭",
    "Luxury": "💎", "Consumer": "🛍", "Telecom & Media": "📡",
    "Telecom": "📡", "Real Estate": "🏢", "Property": "🏘",
    "Mining": "⛏", "Materials": "🔩", "DeFi": "🔗",
    "Large Cap": "🔵", "Mid Cap": "🟡", "Meme & Other": "🐕",
    "Precious Metals": "🥇", "Base Metals": "🔧", "Agriculture": "🌾",
}

with st.sidebar:
    st.markdown("""
    <div style="padding:10px 0 20px 0">
        <div style="font-family:var(--font-mono);font-size:0.9rem;font-weight:700;color:var(--text-primary);letter-spacing:-0.02em">
            GLOBAL<span style="color:#2979ff">MKTS</span>
        </div>
        <div style="font-size:0.65rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:0.12em;margin-top:3px">
            LIVE MARKET DASHBOARD
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Timeframe
    st.markdown('<p style="color:var(--text-muted);font-size:0.7rem;font-family:var(--font-mono);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px">Timeframe</p>', unsafe_allow_html=True)
    timeframe = st.radio(
        "Timeframe", ["Day", "Week", "Month", "Year"],
        horizontal=True, label_visibility="collapsed"
    )

    st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

    # Top-Level Navigation
    top_level = st.selectbox(
        "MARKET UNIVERSE",
        ["Asia", "Europe", "Americas", "Middle East & Africa", "Pacific",
         "🌐 Global Commodities", "₿ Crypto"],
        label_visibility="visible"
    )

    market_universe = get_market_universe()

    if top_level in market_universe:
        continent_data = market_universe[top_level]
        countries = list(continent_data.keys())
        selected_country = st.selectbox("COUNTRY / EXCHANGE", countries)
        sectors = list(continent_data[selected_country].keys())
        selected_sectors = st.multiselect(
            "SECTORS", sectors, default=sectors[:3] if len(sectors) > 3 else sectors
        )
        mode = "stocks"

    elif top_level == "🌐 Global Commodities":
        commodities_data = get_commodities()
        sectors = list(commodities_data.keys())
        selected_sectors = st.multiselect(
            "COMMODITY GROUPS", sectors, default=sectors
        )
        mode = "commodities"

    else:  # Crypto
        crypto_data = get_crypto()
        sectors = list(crypto_data.keys())
        selected_sectors = st.multiselect(
            "CRYPTO GROUPS", sectors, default=sectors
        )
        mode = "crypto"

    st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

    # Auto refresh
    auto_refresh = st.checkbox("⟳ Auto-Refresh (60s)", value=False)
    if auto_refresh:
        st.markdown("""
        <div style="font-size:0.68rem;color:var(--accent-green);font-family:var(--font-mono);margin-top:4px">
            ● Live refresh active
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.65rem;color:var(--text-muted);font-family:var(--font-mono)">
        Data via yfinance<br>
        <span style="color:var(--text-secondary)">{datetime.now().strftime('%H:%M:%S %Z')}</span>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN DASHBOARD AREA ──────────────────────────────────────────────────────

# Header
now_str = datetime.now().strftime("%a, %d %b %Y · %H:%M:%S")
st.markdown(f"""
<div class="dash-header">
    <div>
        <div class="dash-title">GLOBAL <span>MARKET</span> DASHBOARD</div>
        <div class="dash-subtitle">REAL-TIME · {now_str}</div>
    </div>
    <div class="live-badge"><div class="live-dot"></div>LIVE</div>
</div>
""", unsafe_allow_html=True)

# ─── AUTO REFRESH LOGIC ───────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(60)
    st.rerun()

# ─── QUICK MARKET OVERVIEW STATS ─────────────────────────────────────────────
with st.spinner(""):
    overview_tickers = {
        "S&P 500": "^GSPC", "NASDAQ": "^IXIC",
        "Nikkei 225": "^N225", "Gold": "GC=F",
        "Bitcoin": "BTC-USD", "Crude Oil": "CL=F",
    }
    ov_data = fetch_prices(list(overview_tickers.values()), "Day")

cols = st.columns(len(overview_tickers))
for col, (label, ticker) in zip(cols, overview_tickers.items()):
    info = ov_data.get(ticker)
    with col:
        if info:
            pct = info["change_pct"]
            sign = "+" if pct >= 0 else ""
            color = "var(--accent-green)" if pct > 0 else ("var(--accent-red)" if pct < 0 else "var(--text-muted)")
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{label}</div>
                <div class="stat-value" style="font-size:1.05rem">{format_price(info['price'], ticker)}</div>
                <div class="stat-sub" style="color:{color}">{sign}{pct:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{label}</div>
                <div class="stat-value" style="font-size:1rem;color:var(--text-muted)">—</div>
                <div class="stat-sub" style="color:var(--text-muted)">No data</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# ─── MAIN CONTENT AREA ───────────────────────────────────────────────────────
if mode == "stocks" and selected_sectors:
    country_data = market_universe[top_level][selected_country]

    # Page title
    st.markdown(f"""
    <div style="margin-bottom:16px">
        <div style="font-family:var(--font-mono);font-size:1rem;color:var(--text-primary)">
            {CONTINENT_ICONS.get(top_level,'🌐')} {top_level} &nbsp;›&nbsp;
            <span style="color:var(--accent-blue)">{selected_country}</span>
        </div>
        <div style="font-size:0.7rem;color:var(--text-muted);font-family:var(--font-mono);margin-top:4px">
            {timeframe.upper()} VIEW · {len(selected_sectors)} SECTORS SELECTED
        </div>
    </div>
    """, unsafe_allow_html=True)

    if len(selected_sectors) > 1:
        tab_labels = [f"{SECTOR_ICONS.get(s,'📊')} {s}" for s in selected_sectors]
        tabs = st.tabs(tab_labels)
        for tab, sector in zip(tabs, selected_sectors):
            with tab:
                stocks = country_data.get(sector, [])
                render_sector_bars(sector, stocks, timeframe, SECTOR_ICONS.get(sector, "📊"))
    else:
        sector = selected_sectors[0]
        stocks = country_data.get(sector, [])
        render_sector_bars(sector, stocks, timeframe, SECTOR_ICONS.get(sector, "📊"))

elif mode == "commodities" and selected_sectors:
    commodities_data = get_commodities()
    st.markdown("""
    <div style="margin-bottom:16px">
        <div style="font-family:var(--font-mono);font-size:1rem;color:var(--text-primary)">
            🌐 <span style="color:var(--accent-gold)">Global Commodities</span>
        </div>
        <div style="font-size:0.7rem;color:var(--text-muted);font-family:var(--font-mono);margin-top:4px">
            REAL-TIME SPOT & FUTURES
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_labels = [f"{SECTOR_ICONS.get(s,'📊')} {s}" for s in selected_sectors]
    if len(selected_sectors) > 1:
        tabs = st.tabs(tab_labels)
        for tab, sector in zip(tabs, selected_sectors):
            with tab:
                items = commodities_data.get(sector, [])
                render_sector_bars(sector, items, timeframe, SECTOR_ICONS.get(sector, "📊"))
    elif selected_sectors:
        sector = selected_sectors[0]
        items = commodities_data.get(sector, [])
        render_sector_bars(sector, items, timeframe, SECTOR_ICONS.get(sector, "📊"))

elif mode == "crypto" and selected_sectors:
    crypto_data = get_crypto()
    st.markdown("""
    <div style="margin-bottom:16px">
        <div style="font-family:var(--font-mono);font-size:1rem;color:var(--text-primary)">
            ₿ <span style="color:var(--accent-gold)">Cryptocurrency Markets</span>
        </div>
        <div style="font-size:0.7rem;color:var(--text-muted);font-family:var(--font-mono);margin-top:4px">
            LIVE CRYPTO PRICES VIA YFINANCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_labels = [f"{SECTOR_ICONS.get(s,'🔵')} {s}" for s in selected_sectors]
    if len(selected_sectors) > 1:
        tabs = st.tabs(tab_labels)
        for tab, sector in zip(tabs, selected_sectors):
            with tab:
                items = crypto_data.get(sector, [])
                render_sector_bars(sector, items, timeframe, SECTOR_ICONS.get(sector, "🔵"))
    elif selected_sectors:
        sector = selected_sectors[0]
        items = crypto_data.get(sector, [])
        render_sector_bars(sector, items, timeframe, SECTOR_ICONS.get(sector, "🔵"))

else:
    st.markdown("""
    <div class="no-data">
        <div style="font-size:1.5rem;margin-bottom:8px">📊</div>
        Select at least one sector from the sidebar to display market data.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<hr class="glass-divider">
<div style="text-align:center;font-family:var(--font-mono);font-size:0.65rem;color:var(--text-muted);padding:10px 0">
    GLOBALMKTS DASHBOARD · Data via yfinance · Charts via TradingView · 
    For informational purposes only. Not financial advice.
</div>
""", unsafe_allow_html=True)
