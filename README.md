# 👁️ We The Watchers

**Track Your Elected Officials – Know What They Vote, Trade, and Hide**

---

## 📖 Overview

We The Watchers is a civic accountability platform designed to bring transparency to U.S. government representatives. By aggregating publicly available data on voting records, stock trades, financial disclosures, and committee roles, our goal is to empower citizens with the tools they need to hold their elected officials accountable.

---

## 🚀 Features

- 🔍 **Representative Lookup by Zip Code or Name**
- 📊 **Voting History & Bill Tracking**
- 💼 **Stock Trades & Financial Disclosures**
- 🧩 **Conflict of Interest Alerts**
- 📚 **Education Hub on Political Behavior**

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **APIs Used**:
  - Google Civic Information API
  - OpenSecrets (planned)
  - House & Senate Financial Disclosure Archives (planned)

---

## 🧩 How It Works

1. Users enter a **zip code** or **representative's name**.
2. The app fetches details from a local database or the Civic API.
3. If the rep isn't in the database, a fetch script pulls data and adds it.
4. Voting records, financial trades, and potential conflicts are displayed.

---

## 🏁 Getting Started

### 📦 Installation

Clone the repo:
```bash
git clone https://github.com/Majorhub/WeTheWatchers.git
cd WeTheWatchers
```

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Add your API key in `services/civic_lookup.py`:
```python
API_KEY = "your_google_civic_api_key"
```

### ▶️ Run the App

```bash
streamlit run app/main.py
```

---

## 🧪 Development Status

| Feature                          | Status       |
|----------------------------------|--------------|
| Zip Code / Name Rep Lookup       | ✅ Completed |
| Civic API Integration            | ✅ Completed |
| Stock Trade Watch                | 🔄 In Progress |
| Vote Tracking & History          | 🔄 In Progress |
| Alerts and Subscriptions         | 🧩 Planned |
| Congressional Profiles           | ✅ MVP Ready |

---

## 📁 Project Structure

```
WeTheWatchers/
├── app/
│   └── main.py
├── database/
│   └── db.py
│   └── we_watchers.db
├── services/
│   └── civic_lookup.py
│   └── fetch_reps.py
├── assets/
│   └── (images, icons, etc.)
├── README.md
└── requirements.txt
```

---

## 🛡️ License

This project is licensed under the **MIT License** – see the LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 💬 Contact

For questions, ideas, or to get involved:

📫 [Majorhub GitHub](https://github.com/Majorhub)

---

> "Sunlight is the best disinfectant." — Justice Louis Brandeis  
> Let’s make government transparent again.
