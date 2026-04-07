import requests
import json

def get_nifty_data():
    # URL for NSE Sectoral Indices
    url = "https://www.nseindia.com/api/allIndices"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }
    
    # We use a session to handle NSE's cookies automatically
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    data = response.json()['data']
    
    # Filter for main sectoral indices
    sectors = ["NIFTY BANK", "NIFTY IT", "NIFTY AUTO", "NIFTY FMCG", "NIFTY METAL"]
    result = []
    
    for item in data:
        if item['index'] in sectors:
            result.append({
                "name": item['index'],
                "perc": item['percentChange'],
                "color": "#22C55E" if item['percentChange'] >= 0 else "#EF4444"
            })
            
    with open('data.json', 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    get_nifty_data()
