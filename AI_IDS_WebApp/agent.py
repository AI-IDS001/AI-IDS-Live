import time
import pandas as pd
import requests
import io

# We are aiming at your local Flask server's Mailbox
TARGET_URL = "http://127.0.0.1:5000/api/push-live"
DATA_SOURCE = "nsl_kdd_dataset.csv"

print("🕵️‍♂️ Starting Local AI-IDS Agent...")
print("📡 Connecting to Mission Control...")

try:
    # Load the big dataset to act as our "live" internet stream
    df = pd.read_csv(DATA_SOURCE)
    print(f"✅ Loaded {len(df)} packets for simulation.")
    
    # We will grab 5 packets at a time
    chunk_size = 5
    
    for i in range(0, len(df), chunk_size):
        # Slice out a tiny chunk of data
        chunk = df.iloc[i : i + chunk_size]
        
        # Turn it into a temporary CSV file in the laptop's memory
        csv_buffer = io.StringIO()
        chunk.to_csv(csv_buffer, index=False)
        
        # Package it up and securely POST it to your website
        files = {'file': ('live_stream.csv', csv_buffer.getvalue())}
        
        try:
            response = requests.post(TARGET_URL, files=files)
            if response.status_code == 200:
                print(f"[{time.strftime('%X')}] 🚀 Streamed {len(chunk)} packets to dashboard.")
            else:
                print(f"⚠️ Server rejected data: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect! Is your Flask app.py running?")
        
        # Wait 3 seconds before the next pulse
        time.sleep(3)

except FileNotFoundError:
    print(f"❌ Error: Cannot find '{DATA_SOURCE}'. Is it in this folder?")
except KeyboardInterrupt:
    print("\n🛑 Agent offline.")