
# 🔍 Social Profile Finder

**Social Profile Finder** is a Streamlit-based web app that helps users search for social media profiles (LinkedIn, Facebook, Twitter, Instagram) based on names, cities, and emails using the Google Search SerpAPI.

## 🚀 Features

- 🔎 **Single Search**: Look up a person by name, with optional city and email to improve accuracy.
- 📁 **Bulk Search**: Upload a CSV file of people to find their social media profiles in batch.
- 📊 **Result Dashboard**: View metrics, filter results, and download the final dataset.
- 🔗 **Clickable Links**: Display profile URLs directly as hyperlinks for quick access.
- 📉 **Progress Bar**: Real-time tracking during bulk searches.

---

## 📂 Folder Structure

```bash
.
├── app.py             # Main Streamlit application file
├── README.md          # This file
└── requirements.txt   # Python dependencies (not included, see below)
```

---

## 📋 Prerequisites

- Python 3.7+
- A valid [SerpAPI](https://serpapi.com/) API key

---

## 🛠️ Installation

1. **Clone this repository:**

```bash
git clone https://github.com/yourusername/social-profile-finder.git
cd social-profile-finder
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

> Make sure your `requirements.txt` includes:
```text
streamlit
pandas
requests
```

3. **Set your SerpAPI key:**

The API key is hardcoded in `app.py`:
```python
SERPAPI_KEY = "your_serpapi_key_here"
```

> You can improve security by loading it from a `.env` file or Streamlit secrets instead.

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📄 CSV Upload Format

Your CSV should have the following structure:

| Name            | City     | Email               |
|-----------------|----------|---------------------|
| John Doe        | Mumbai   | johndoe@email.com   |
| Jane Smith      | Delhi    |                     |

- **Name**: (Required)
- **City**: (Optional)
- **Email**: (Optional)

---

## 📌 Notes

- This app uses SerpAPI’s Google Search API to extract social links.
- Avoid rapid bulk searches to prevent hitting API rate limits.
- The app supports exporting results in CSV format with all found profiles.

---

## 📸 Screenshots

> _Coming soon — or add your own!_

---

## 📜 License

MIT License. See `LICENSE` for details.

---

## 🙋‍♂️ Author

Utkarsh Narayan Pandey  
> [LinkedIn](https://linkedin.com/in/utkarshnarayanpandey) | [GitHub](https://github.com/utkarshnpatel)
