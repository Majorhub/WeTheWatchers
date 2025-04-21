import os
import requests

# You can hardcode your API key here for testing purposes
# or set it via environment variable beforehand
GOOGLE_API_KEY = os.getenv("AIzaSyAMKsM6axOeVHRqIqy8QYT4ccPAstAFuGQ") or "AIzaSyAMKsM6axOeVHRqIqy8QYT4ccPAstAFuGQ"

def fetch_rep_from_google(zip_code):
    if not GOOGLE_API_KEY:
        print("❌ No API key provided.")
        return

    url = f"https://www.googleapis.com/civicinfo/v2/representatives?address={zip_code}&key={GOOGLE_API_KEY}"
    try:
        response = requests.get(url)
        print(f"📡 Response Code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return

        data = response.json()
        print("📦 Full JSON Response:")
        print(data)

        # Optionally print just rep info
        offices = data.get("offices", [])
        officials = data.get("officials", [])
        for office in offices:
            if "United States House of Representatives" in office.get("name", ""):
                idx = office.get("officialIndices", [])[0]
                rep = officials[idx]
                print(f"\n🧑 Rep Found: {rep.get('name')} ({rep.get('party')})")
                return

        print("⚠️ No House rep found.")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    # 🔧 Change this ZIP to test different areas
    fetch_rep_from_google("92646")