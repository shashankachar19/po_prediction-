📦 PO Category Classifier (L1–L2–L3)

A Streamlit-based AI application that classifies Purchase Order (PO) descriptions into L1, L2, and L3 categories using a fixed enterprise taxonomy and a large language model (LLM) powered by Groq.

🚀 Features

Classifies PO descriptions into L1 / L2 / L3

Uses a strict, predefined taxonomy

Returns structured JSON output

Prevents hallucinated or invalid categories

Optional supplier input for better accuracy

Simple and clean Streamlit UI

🧠 How It Works

User enters a PO description (and optional supplier name)

The app sends the input to an LLM via Groq API

The model follows a strict system prompt:

Uses only the provided taxonomy

Outputs only valid JSON

Returns "Not sure" if classification is unclear

The result is displayed in JSON format

🗂️ Project Structure . ├── app.py # Streamlit UI ├── classifier.py # LLM interaction & classification logic ├── prompts.py # System prompt and few-shot examples ├── taxonomy.py # Fixed L1–L2–L3 taxonomy └── README.md # Project documentation

🛠️ Tech Stack

Python

Streamlit

Groq API

LLaMA 3.1 (8B Instant)

JSON-based structured output

🔐 Prerequisites

Python 3.9+

A Groq API Key

⚙️ Installation & Setup 1️⃣ Clone the repository git clone https://github.com/your-username/po-category-classifier.git cd po-category-classifier

2️⃣ Install dependencies pip install streamlit groq

3️⃣ Configure secrets

Create a .streamlit/secrets.toml file:

GROQ_API_KEY = "your_groq_api_key_here"

▶️ Run the Application streamlit run app.py

Open your browser at:

http://localhost:8501

🧪 Example Input

PO Description

DocuSign Inc - eSignature Enterprise Pro Subscription

Supplier

DocuSign Inc

Output

{ "po_description": "DocuSign Inc - eSignature Enterprise Pro Subscription", "L1": "IT", "L2": "Software", "L3": "Subscription" }

📌 Key Design Rules

✅ Uses only predefined taxonomy

❌ No category invention

❌ No cross-row category mixing

✅ Strict JSON-only output

✅ Deterministic results (temperature = 0.0)

📄 License

This project is provided for educational and internal enterprise use. Add a license file if you plan to open-source it.

✨ Future Enhancements

Bulk PO upload (CSV / Excel)

Confidence scoring

Taxonomy editor UI

Database storage of classifications

API endpoint support
