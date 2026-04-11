import pyotp
from SmartApi import SmartConnect

# 1. This must be the 26-digit SEED KEY from the portal
TOTP_KEY = "YOUR_26_DIGIT_SEED_HERE" 

def get_session():
    try:
        # 2. Clean the key (remove spaces if any)
        clean_key = TOTP_KEY.replace(" ", "")
        
        # 3. Generate the 6-digit code for THIS exact moment
        totp_code = pyotp.TOTP(clean_key).now()
        
        # 4. Login using that code
        obj = SmartConnect(api_key="YOUR_API_KEY")
        data = obj.generateSession("YOUR_CLIENT_ID", "YOUR_PASSWORD", totp_code)
        
        return data
    except Exception as e:
        return f"Error: {e}"
