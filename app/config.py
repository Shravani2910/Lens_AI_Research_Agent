import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


# Local development: read from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")


# Streamlit Cloud: read from Secrets
if not GROQ_API_KEY:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not GROQ_MODEL:
    GROQ_MODEL = st.secrets.get(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    )


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to Streamlit Cloud Secrets."
    )


llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0,
)