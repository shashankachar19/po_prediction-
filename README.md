# PO Category Classifier (Multi‑Purpose Streamlit App)

A modern Streamlit app that includes:
- **PO Classification** (L1/L2/L3 using Groq)
- **Taxonomy Browser**
- **Quick KPI Tracker**
- **Text Toolkit**
- **Assistant Chat** (asks questions based on session history)

## Features
- Clean, animated dark UI
- Session‑only storage (no database needed)
- Groq‑powered classification + assistant chat
- Mobile‑friendly layout

---

## Getting Started

## 1. Install dependencies
pip install -r requirements.txt

## 2. create the file using terminal
.streamlit/secrets.toml

## 3. Add this into the file 
GROQ_API_KEY = "your_groq_key_here"

## 4. To run the project use this command 
streamlit run app.py


#### project structure 
.
├── app.py                # Streamlit UI + logic
├── classifier.py         # Groq API calls
├── prompts.py            # System prompt
├── taxonomy.py           # L1/L2/L3 taxonomy
├── requirements.txt
├── runtime.txt           # Python version for Streamlit Cloud
└── .streamlit/
    └── config.toml

    
## Notes
Data is session-only (not saved after refresh)
Chat assistant uses your session history for context


