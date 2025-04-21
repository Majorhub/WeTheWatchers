import os
import requests

def fetch_rep_from_google(zip_code):
    api_key = os.getenv("GOOGLE_API_KEY") or "AIzaSyAMKsM6axOeVHRqIqy8QYT4ccPAstAFuGQ"

    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ No valid API key found. Set GOOGLE_API_KEY in environment or replace the placeholder.")
        return {"name": "NA", "party": "NA", "state": "NA"}

    url = f"https://www.googleapis.com/civicinfo/v2/representatives?address={zip_code}&key={api_key}"

    try:
        response = requests.get(url)
        print(f"📡 API Response Status: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ API call failed: {response.text}")
            return {"name": "NA", "party": "NA", "state": "NA"}

        data = response.json()
        print("📦 Full API Response:")
        print(data)

        offices = data.get("offices", [])
        officials = data.get("officials", [])

        for office in offices:
            if "legislatorLowerBody" in office.get("roles", []):
                indices = office.get("officialIndices", [])
                if indices:
                    rep = officials[indices[0]]
                    return {
                        "name": rep.get("name", "NA"),
                        "party": rep.get("party", "NA"),
                        "state": data.get("normalizedInput", {}).get("state", "NA")
                    }

        print("⚠️ No U.S. House Representative found in API data.")
        return {"name": "NA", "party": "NA", "state": "NA"}

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return {"name": "NA", "party": "NA", "state": "NA"}


# 🧪 Manual Test
if __name__ == "__main__":
    test_zip = "92646"
    print(f"🔍 Testing Google Civic API for ZIP: {test_zip}")
    result = fetch_rep_from_google(test_zip)
    print("✅ Parsed Result:")
    print(result)