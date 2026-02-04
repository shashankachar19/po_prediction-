import streamlit as st
import json
from datetime import datetime
import pandas as pd
from classifier import classify_po, chat_with_context
from taxonomy import TAXONOMY

st.set_page_config(page_title="PO Category Classifier", layout="wide")

st.markdown(
    """
    <style>
      :root {
        --accent: #60a5fa;
        --accent-2: #34d399;
        --ink: #e2e8f0;
        --muted: #94a3b8;
        --panel: #0f172a;
        --bg: #0b1220;
        --border: #1e293b;
        --maxw: 1200px;
      }
      .block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; max-width: var(--maxw); }
      [data-testid="stAppViewContainer"] { background: var(--bg); }
      [data-testid="stHeader"] { background: transparent; }

      .hero-wrap {
        background:
          radial-gradient(600px 120px at 12% -25%, rgba(96,165,250,0.35), transparent 70%),
          linear-gradient(135deg, #0f172a 0%, #0b1220 60%, #111827 100%);
        border: 1px solid var(--border);
        padding: 20px 22px 22px 22px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        animation: fade-in 500ms ease-out;
        position: relative;
        overflow: hidden;
      }
      .hero-wrap::after {
        content: "";
        position: absolute;
        inset: -40% 10% auto 10%;
        height: 180px;
        background: radial-gradient(closest-side, rgba(96,165,250,0.25), transparent 70%);
        opacity: 0.6;
        filter: blur(4px);
        animation: glow-pulse 4s ease-in-out infinite;
        pointer-events: none;
      }
      .hero-wrap h1 { margin: 0; color: var(--ink); font-size: 30px; letter-spacing: -0.3px; }
      .hero-wrap p { margin: 6px 0 0 0; color: #cbd5f5; }
      .pill {
        display: inline-block; padding: 4px 10px; margin-right: 6px;
        border-radius: 999px; font-size: 12px;
        background: rgba(96,165,250,0.16); color: #dbeafe;
      }
      .muted { color: var(--muted); font-size: 12px; }
      .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        background: rgba(52, 211, 153, 0.18);
        color: #a7f3d0;
        border: 1px solid rgba(52, 211, 153, 0.35);
      }

      /* Card styling for Streamlit containers */
      div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 16px 18px;
        background: var(--panel);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        animation: float-in 420ms ease-out;
      }
      div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]:hover {
        border-color: rgba(96,165,250,0.45);
        box-shadow: 0 14px 26px rgba(0, 0, 0, 0.35);
        transform: translateY(-2px);
        transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
      }

      /* Inputs */
      textarea, input {
        border-radius: 12px !important;
        background: #0b1220 !important;
        color: #e2e8f0 !important;
        border: 1px solid #1f2937 !important;
        transition: box-shadow 160ms ease, border-color 160ms ease;
      }
      textarea:focus, input:focus {
        border-color: rgba(96,165,250,0.6) !important;
        box-shadow: 0 0 0 3px rgba(96,165,250,0.15);
      }

      /* Buttons */
      div.stButton > button {
        border-radius: 12px;
        border: 1px solid #1f2937;
        background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
        color: #e2e8f0;
        font-weight: 600;
        padding: 0.65rem 1rem;
        min-height: 44px;
        transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
      }
      div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 24px rgba(0, 0, 0, 0.35);
        border-color: rgba(96,165,250,0.5);
      }
      div.stButton > button:active { transform: translateY(0) scale(0.99); }
      div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #0ea5e9 0%, #2563eb 100%);
        border-color: rgba(14,165,233,0.6);
      }

      /* Sidebar */
      section[data-testid="stSidebar"] { background: #0f172a; }
      section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        border-radius: 14px;
      }
      label { transition: color 160ms ease; }
      label:hover { color: #cbd5f5; }

      /* Assistant panel (right column) */
      .assistant-panel {
        margin-top: 12px;
      }
      .assistant-panel div.stButton > button,
      .assistant-panel div.stFormSubmitButton > button {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-color: rgba(96,165,250,0.35);
      }
      .assistant-panel div.stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(180deg, #0ea5e9 0%, #2563eb 100%);
        border-color: rgba(14,165,233,0.6);
      }
      .assistant-panel [data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 1px solid #1f2937;
        background: #0b1220;
        padding: 10px 12px;
      }

      /* Responsive layout */
      @media (max-width: 900px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .hero-wrap { padding: 16px 16px 18px 16px; }
        .hero-wrap h1 { font-size: 24px; }
      }
      @media (max-width: 640px) {
        .hero-wrap h1 { font-size: 22px; }
        .hero-wrap p { font-size: 13px; }
      }
      @media (min-width: 1600px) {
        :root { --maxw: 1400px; }
        .hero-wrap h1 { font-size: 34px; }
      }
      /* Expanders */
      div[data-testid="stExpander"] {
        border-radius: 12px;
        transition: border-color 160ms ease, box-shadow 160ms ease;
      }
      div[data-testid="stExpander"]:hover {
        border-color: rgba(96,165,250,0.45);
        box-shadow: 0 10px 18px rgba(0, 0, 0, 0.3);
      }

      /* Animations */
      @keyframes fade-in {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes glow-pulse {
        0%, 100% { opacity: 0.35; transform: translateY(0); }
        50% { opacity: 0.75; transform: translateY(6px); }
      }
      @keyframes float-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes pulse-in {
        0% { opacity: 0; transform: translateY(6px) scale(0.99); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
      }
      @keyframes slide-up {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .taxonomy-panel { animation: pulse-in 360ms ease-out; }
      .taxonomy-panel:hover {
        box-shadow: 0 16px 28px rgba(0, 0, 0, 0.35);
        transform: translateY(-2px);
        transition: transform 160ms ease, box-shadow 160ms ease;
      }
      div[data-testid="stDataFrame"] tbody tr:hover {
        background-color: rgba(96,165,250,0.08) !important;
      }

      .card {
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 16px 18px;
        background: var(--panel);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
        min-height: 150px;
        display: flex;
        flex-direction: column;
      }
      .card h3 { margin: 0 0 6px 0; font-size: 18px; }
      .card p { margin: 0 0 12px 0; color: var(--muted); min-height: 44px; }
      .module-wrap { animation: slide-up 420ms ease-out; }
      .card-anim { animation: float-in 420ms ease-out; }
      .card-anim:nth-child(1) { animation-delay: 40ms; }
      .card-anim:nth-child(2) { animation-delay: 90ms; }
      .card-anim:nth-child(3) { animation-delay: 140ms; }
      .card:hover {
        transform: translateY(-3px);
        border-color: rgba(96,165,250,0.45);
        box-shadow: 0 16px 28px rgba(0, 0, 0, 0.35);
      }
      .card:active { transform: translateY(-1px) scale(0.995); }
      /* Typing indicator */
      .typing {
        display: inline-flex;
        gap: 6px;
        align-items: center;
        padding: 8px 10px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #1f2937;
        margin: 6px 0 10px 0;
      }
      .typing span {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #94a3b8;
        animation: dot 1.2s infinite ease-in-out;
      }
      .typing span:nth-child(2) { animation-delay: 0.2s; }
      .typing span:nth-child(3) { animation-delay: 0.4s; }
      @keyframes dot {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
        40% { transform: translateY(-3px); opacity: 1; }
      }
      @keyframes panel-in {
        from { opacity: 0; transform: translateY(8px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-wrap">
      <span class="pill">L1</span><span class="pill">L2</span><span class="pill">L3</span>
      <h1>PO Category Classifier</h1>
      <p>Classify purchase orders into a consistent taxonomy with a clean JSON output.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "po_description" not in st.session_state:
    st.session_state.po_description = ""
if "supplier" not in st.session_state:
    st.session_state.supplier = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "active_module" not in st.session_state:
    st.session_state.active_module = "Home"
if "kpi_rows" not in st.session_state:
    st.session_state.kpi_rows = []
if "taxonomy_rows" not in st.session_state:
    rows = []
    for line in TAXONOMY.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("L1 |") or set(line) == {"-"}:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 3:
            rows.append({"L1": parts[0], "L2": parts[1], "L3": parts[2]})
    st.session_state.taxonomy_rows = rows
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_prefill" not in st.session_state:
    st.session_state.chat_prefill = ""
examples = [
    {
        "label": "Office supplies - printer paper",
        "po_description": "Purchase 10 cases of A4 printer paper, 80gsm, white.",
        "supplier": "Staples",
    },
    {
        "label": "IT hardware - laptops",
        "po_description": "Procure 15 Dell Latitude laptops with 16GB RAM and 512GB SSD.",
        "supplier": "Dell",
    },
    {
        "label": "Facilities - cleaning services",
        "po_description": "Monthly janitorial services for HQ, includes nightly cleaning and waste removal.",
        "supplier": "CleanCo",
    },
]

with st.sidebar:
    st.subheader("Quick Start")
    st.caption("Load a sample and run the classifier in seconds.")
    example_labels = ["Select an example..."] + [e["label"] for e in examples]
    selected_example = st.selectbox("Examples", example_labels, index=0)
    if st.button("Use example"):
        if selected_example != "Select an example...":
            chosen = next(e for e in examples if e["label"] == selected_example)
            st.session_state.po_description = chosen["po_description"]
            st.session_state.supplier = chosen["supplier"]
    st.markdown("---")
    st.subheader("Tips")
    st.markdown("- Include product/service type and quantity.")
    st.markdown("- Add supplier name when known.")
    st.markdown("- Use plain language for best results.")

def render_home():
    st.markdown("<div class='module-wrap'>", unsafe_allow_html=True)
    st.subheader("Choose a Module")
    st.caption("This app is multi-purpose. Pick what you want to do next.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="card card-anim">
              <h3>PO Classification</h3>
              <p>Classify purchase orders into L1/L2/L3 categories.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open PO Classifier", use_container_width=True):
            st.session_state.active_module = "PO"
    with c2:
        st.markdown(
            """
            <div class="card card-anim">
              <h3>Quick KPI Tracker</h3>
              <p>Track a few KPIs manually and visualize trends.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open KPI Tracker", use_container_width=True):
            st.session_state.active_module = "KPI"
    with c3:
        st.markdown(
            """
            <div class="card card-anim">
              <h3>Text Toolkit</h3>
              <p>Clean, shorten, or bulletize text quickly.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Text Toolkit", use_container_width=True):
            st.session_state.active_module = "Text"
    st.markdown("</div>", unsafe_allow_html=True)


def render_po_classifier():
    st.markdown("<div class='module-wrap'>", unsafe_allow_html=True)
    if st.button("Back to Home", use_container_width=True):
        st.session_state.active_module = "Home"

    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            st.subheader("Input")
            po_description = st.text_area(
                "PO Description",
                height=160,
                key="po_description",
                placeholder="e.g., Procure 15 Dell Latitude laptops with 16GB RAM and 512GB SSD.",
            )
            st.markdown(
                "<span class='muted'>Tip: include item type, quantity, and service context.</span>",
                unsafe_allow_html=True,
            )
            st.caption(f"Characters: {len(po_description.strip())}")
            supplier = st.text_input(
                "Supplier (optional)",
                key="supplier",
                placeholder="e.g., Dell",
            )
            st.markdown(
                "<span class='muted'>We only store history in your current session.</span>",
                unsafe_allow_html=True,
            )

    with right:
        with st.container(border=True):
            st.subheader("Actions")
            st.caption("One click to classify and download.")
            classify_clicked = st.button("Classify", use_container_width=True, type="primary")
            st.markdown(
                "<span class='muted'>Results appear below with a downloadable JSON file.</span>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.subheader("Taxonomy Browser")
    st.markdown("<div class='taxonomy-panel'>", unsafe_allow_html=True)
    browser_left, browser_right = st.columns([1, 2])
    with browser_left:
        search_term = st.text_input("Search", placeholder="Search by keyword...")
        l1_options = ["All"] + sorted({r["L1"] for r in st.session_state.taxonomy_rows})
        l1_filter = st.selectbox("L1 Filter", l1_options, index=0)
        l2_options = ["All"] + sorted(
            {r["L2"] for r in st.session_state.taxonomy_rows if l1_filter == "All" or r["L1"] == l1_filter}
        )
        l2_filter = st.selectbox("L2 Filter", l2_options, index=0)

    filtered_rows = []
    query = search_term.strip().lower()
    for r in st.session_state.taxonomy_rows:
        if l1_filter != "All" and r["L1"] != l1_filter:
            continue
        if l2_filter != "All" and r["L2"] != l2_filter:
            continue
        if query and query not in " ".join([r["L1"], r["L2"], r["L3"]]).lower():
            continue
        filtered_rows.append(r)

    with browser_right:
        st.caption(f"Matches: {len(filtered_rows)}")
        st.dataframe(filtered_rows, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    if classify_clicked:
        if not po_description.strip():
            st.warning("Please enter a PO Description to classify.")
        elif len(po_description.strip()) < 5:
            st.warning("PO Description is too short. Please add a bit more detail.")
        else:
            with st.spinner("Classifying..."):
                try:
                    result = classify_po(po_description, supplier)
                except Exception as exc:
                    st.error("Classification failed. Please check your API key and try again.")
                    st.text(str(exc))
                    st.stop()

            parsed = None
            try:
                parsed = json.loads(result)
            except Exception:
                st.error("Model response was not valid JSON. Showing raw output below.")
                st.text(result)
                st.stop()

            if isinstance(parsed, dict):
                l1 = _extract_key(parsed, {"l1", "level1", "category_l1"})
                l2 = _extract_key(parsed, {"l2", "level2", "category_l2"})
                l3 = _extract_key(parsed, {"l3", "level3", "category_l3"})
                confidence = _extract_key(parsed, {"confidence", "score", "probability"})

                st.subheader("Summary")
                cols = st.columns(4)
                cols[0].metric("L1", l1 if l1 else "-")
                cols[1].metric("L2", l2 if l2 else "-")
                cols[2].metric("L3", l3 if l3 else "-")
                if confidence is not None:
                    cols[3].markdown(
                        f"<span class='badge'>Confidence: {confidence}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    cols[3].metric("Confidence", "-")

                st.subheader("Raw JSON")
                st.json(parsed)
                st.caption("Copy the JSON below if you need to paste it elsewhere.")
                st.code(json.dumps(parsed, indent=2), language="json")
            else:
                st.subheader("Raw Output")
                st.text(result)

            st.download_button(
                label="Download result as JSON",
                data=json.dumps(parsed, indent=2),
                file_name="po_classification.json",
                mime="application/json",
            )

            st.session_state.history.insert(
                0,
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "po_description": po_description.strip(),
                    "supplier": supplier.strip() if supplier else "",
                    "result": parsed,
                },
            )

    st.markdown("</div>", unsafe_allow_html=True)


def _extract_key(data, keys):
    for k in data.keys():
        if k.lower() in keys:
            return data[k]
    return None


def render_kpi_tracker():
    st.markdown("<div class='module-wrap'>", unsafe_allow_html=True)
    if st.button("Back to Home", use_container_width=True):
        st.session_state.active_module = "Home"
    st.subheader("Quick KPI Tracker")
    st.caption("Session-only tracking for a few KPIs. Add rows and see trends.")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            kpi_name = st.text_input("KPI Name", placeholder="e.g., Monthly Spend")
        with c2:
            kpi_value = st.number_input("Value", step=1.0)
        with c3:
            kpi_period = st.text_input("Period", placeholder="e.g., 2026-02")
        if st.button("Add KPI", use_container_width=True):
            if kpi_name and kpi_period:
                st.session_state.kpi_rows.append(
                    {"KPI": kpi_name.strip(), "Value": float(kpi_value), "Period": kpi_period.strip()}
                )
            else:
                st.warning("Please provide KPI Name and Period.")

    if st.session_state.kpi_rows:
        df = pd.DataFrame(st.session_state.kpi_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.subheader("Trend View")
        st.line_chart(df.pivot_table(index="Period", columns="KPI", values="Value", aggfunc="mean"))
    else:
        st.info("No KPI rows yet. Add one above to see a chart.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_text_toolkit():
    st.markdown("<div class='module-wrap'>", unsafe_allow_html=True)
    if st.button("Back to Home", use_container_width=True):
        st.session_state.active_module = "Home"
    st.subheader("Text Toolkit")
    st.caption("Lightweight tools without external APIs. Session-only.")
    text = st.text_area("Input Text", height=160, placeholder="Paste any text here...")
    mode = st.selectbox("Action", ["Clean", "Shorten", "Bulletize"])
    if st.button("Run Tool", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            if mode == "Clean":
                output = " ".join(text.split())
            elif mode == "Shorten":
                words = text.split()
                output = " ".join(words[:50]) + ("..." if len(words) > 50 else "")
            else:
                sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
                output = "\n".join([f"- {s}" for s in sentences[:8]])
            st.subheader("Output")
            st.code(output, language="text")
    st.markdown("</div>", unsafe_allow_html=True)



def render_global_chat():
    st.markdown("<div class='assistant-panel'>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Assistant")
        st.caption("Ask about your session history and taxonomy.")
        if not st.session_state.history:
            st.info("Run a classification first to build context for chat.")
        else:
            if st.button("Summarize all classifications", use_container_width=True, key="chat_summary"):
                st.session_state.chat_prefill = "Summarize all classifications in this session."
            if st.button("Clear chat", use_container_width=True, key="chat_clear"):
                st.session_state.chat_messages = []

            for msg in st.session_state.chat_messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Message", placeholder="Ask about your session history...", label_visibility="collapsed")
            send = st.form_submit_button("Send", type="primary")
        if not user_msg and st.session_state.chat_prefill:
            user_msg = st.session_state.chat_prefill
            st.session_state.chat_prefill = ""
            send = True
        if send and user_msg:
            st.session_state.chat_messages.append({"role": "user", "content": user_msg})
            with st.chat_message("user"):
                st.write(user_msg)
            with st.chat_message("assistant"):
                st.markdown("<div class='typing'><span></span><span></span><span></span></div>", unsafe_allow_html=True)
                with st.spinner("Thinking..."):
                    reply = chat_with_context(
                        st.session_state.chat_messages,
                        st.session_state.history,
                        TAXONOMY,
                    )
                st.write(reply)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
    st.markdown("</div>", unsafe_allow_html=True)


def render_main():
    if st.session_state.active_module == "Home":
        render_home()
    elif st.session_state.active_module == "PO":
        render_po_classifier()
        if st.session_state.history:
            st.subheader("History")
            if st.button("Clear history"):
                st.session_state.history = []
            else:
                for item in st.session_state.history[:10]:
                    with st.expander(f"{item['timestamp']} - {item['po_description'][:60]}"):
                        st.text(f"Supplier: {item['supplier'] or 'Not provided'}")
                        st.json(item["result"])
    elif st.session_state.active_module == "KPI":
        render_kpi_tracker()
    elif st.session_state.active_module == "Text":
        render_text_toolkit()


render_main()
st.markdown("---")
render_global_chat()
