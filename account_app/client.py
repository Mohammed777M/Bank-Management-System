'''
FastAPI application for Account management with SQLite.

This module implements a RESTful API to perform CRUD operations on
accounts stored in a SQLite database. Each account has the following
fields:
    - id (int): Primary key.
    - name (str): Account holder's name.
    - number (str): Unique account number.
    - balance (float): Current account balance.

Features:
    • Create, read, update, and delete accounts.
    • Compute total balance across all accounts using:
        - Multithreading (ThreadPoolExecutor)
        - Multiprocessing (ProcessPoolExecutor)
        - Asynchronous coroutines (asyncio)
    • Centralized logging and exception handling.
    • PEP 8–compliant code style and type hints.'''

# client_app.py
import streamlit as st
import requests
from request_helpers import safe_json_response
from logger import setup_logging

setup_logging()

API_BASE = "http://127.0.0.1:5000"  # Flask server address

st.set_page_config(page_title="Account Client", page_icon="💳", layout="centered")
st.title("💳 Account Management Client")

menu = ["Create Account", "Read Account", "Update Account", "Delete Account"]
choice = st.sidebar.radio("Navigation", menu)

# ---------------- Create ----------------
if choice == "Create Account":
    st.header("Create Account")
    name = st.text_input("Name")
    number = st.text_input("Account Number")
    balance = st.number_input("Balance", min_value=0.0, step=100.0)

    if st.button("Create"):
        resp = requests.post(f"{API_BASE}/create", json={
            "name": name, "number": number, "balance": balance
        })
        st.write(safe_json_response(resp))

# ---------------- Read ----------------
elif choice == "Read Account":
    st.header("Read Account")
    number = st.text_input("Account Number")
    if st.button("Read"):
        resp = requests.get(f"{API_BASE}/read/{number}")
        st.write(safe_json_response(resp))

# ---------------- Update ----------------
elif choice == "Update Account":
    st.header("Update Account")
    number = st.text_input("Account Number")
    new_name = st.text_input("New Name (optional)")
    new_balance = st.number_input("New Balance", min_value=0.0, step=100.0)

    if st.button("Update"):
        payload = {}
        if new_name:
            payload["name"] = new_name
        if new_balance:
            payload["balance"] = new_balance
        resp = requests.put(f"{API_BASE}/update/{number}", json=payload)
        st.write(safe_json_response(resp))

# ---------------- Delete ----------------
elif choice == "Delete Account":
    st.header("Delete Account")
    number = st.text_input("Account Number")
    if st.button("Delete"):
        resp = requests.delete(f"{API_BASE}/delete/{number}")
        st.write(safe_json_response(resp))

