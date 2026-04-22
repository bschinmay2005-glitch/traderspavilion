Act as a Senior UI/UX and Fintech Developer. Create a Streamlit dashboard that replicates the 'Sector Rotation' layout but uses the 'TradingView Mini Chart' widget for maximum reliability.

1. The Strategy: > Instead of using Python to fetch data (which causes 401/rate-limit errors), use streamlit.components.v1.html to embed TradingView widgets. This ensures the data is always live and never blocked.

2. The Indices (Grouped by your list):
Arrange the following tickers into a professional 3-column grid layout:

Key/Sectoral: NSE:NIFTY (Benchmark), NSE:CNXAUTO, NSE:CNXIT, NSE:CNXPSUBANK, NSE:CNXPHARMA, NSE:CNXMETAL, NSE:CNXREALTY, NSE:CNXENERGY, NSE:CNXINFRA.

Financials/Thematic: NSE:NIFTY_FIN_SERVICE, NSE:CNXFMCG, NSE:CNXMEDIA, NSE:CNXCONSUMP, NSE:CNXPSE, NSE:CNXSERVICE.

New/Specific: NSE:NIFTY_OIL_AND_GAS, NSE:NIFTY_HEALTHCARE, NSE:NIFTY_INDIA_MANUFACTURING, NSE:NIFTY_INDIA_DEFENCE.

3. Widget Config:

Use the embed-widget-mini-symbol-overview.js.

Settings: colorTheme: "dark", isTransparent: true, width: "100%", height: 150.

4. Visual Polish:

Set page to layout="wide".

Use custom CSS to create a "Terminal" feel with a dark #080c14 background.

Group indices under headers: "Key Sectoral", "Thematic & Finance", and "Emerging & Others".

Output the complete app.py.
