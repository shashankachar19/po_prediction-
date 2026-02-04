import os
import json
import streamlit as st
from groq import Groq
from prompts import SYSTEM_PROMPT

MODEL = "llama-3.1-8b-instant"

def _get_client():
  api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
  if not api_key:
    raise RuntimeError(
      "GROQ_API_KEY is not set. Add it to Streamlit secrets or environment."
    )
  return Groq(api_key=api_key)

def classify_po(po_description:str,Supplier:str="Not provided"):
  user_prompt = f"""
  PO Description: {po_description}
  Supplier: {Supplier}
  """
  client = _get_client()
  Response = client.chat.completions.create(
    model=MODEL,
    temperature=0.0,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

  )
  return Response.choices[0].message.content


CHAT_SYSTEM_PROMPT = """
You are a procurement assistant. Answer questions using ONLY the provided session history
and taxonomy context. If the answer cannot be derived from the context, say so clearly.
Be concise and practical.
"""

def chat_with_context(messages, history, taxonomy):
  client = _get_client()
  context = {
    "history": history,
    "taxonomy": taxonomy,
  }
  chat_messages = [
    {"role": "system", "content": CHAT_SYSTEM_PROMPT.strip()},
    {"role": "user", "content": "Context:\n" + json.dumps(context, ensure_ascii=False)}
  ] + messages
  Response = client.chat.completions.create(
    model=MODEL,
    temperature=0.2,
    messages=chat_messages
  )
  return Response.choices[0].message.content
