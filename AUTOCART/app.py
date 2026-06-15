import streamlit as st
import json
from pathlib import Path
from AUTOCART.walmart_api import fetch_trending_products
from AUTOCART.autocart_engine import generate_autocart

st.set_page_config(page_title="AutoCart", page_icon="🛒", layout="centered")
st.title("🛒 AutoCart Smart Shopping Assistant")

# --- PRODUCT SEARCH ---
query = st.text_input("Search for products", placeholder="e.g. shampoo, soap, banana")

if st.button("Search"):
    if query.strip():
        st.subheader("🔍 Search Results")
        results = fetch_trending_products(query, num_results=5)
        if results:
            for product in results:
                # Try common name keys
                name = product.get('title') or product.get('name') or product.get('item') or 'Unnamed Product'
                st.markdown(f"**{name}**")
                link = product.get('link', '#')
                st.markdown(f"[View Product]({link})")
                st.markdown("---")
        else:
            st.warning("No products found.")
    else:
        st.error("Please enter a valid search query.")

# --- LOAD USER DATA ---
try:
    with open(Path(__file__).parent / "user_history.json", "r") as f:
        user_data = json.load(f)
except FileNotFoundError:
    st.error("❌ user_history.json not found!")
    st.stop()

# --- USER SELECTOR ---
user_ids = list(user_data.keys())
selected_user = st.selectbox("👤 Select User", user_ids)

# --- SHOW RECOMMENDATIONS ON BUTTON CLICK ---
if st.button("Generate Recommendations"):
    st.subheader(f"✨ Recommended for: {selected_user}")
    recommendations = generate_autocart(user_data[selected_user])
    
    if recommendations:
        for rec in recommendations:
            name = rec.get('item', 'Unnamed')
            st.markdown(f"**{name}**")
            st.markdown(f"- Category: {rec.get('category', 'N/A')}")
            suggested = rec.get("suggested", {})
            title = suggested.get("title", "Unnamed Product")
            link = suggested.get("link", "#")
            st.markdown(f"- Recommended Product: [{title}]({link})")
            st.markdown("---")
    else:
        st.info("No recommendations available.")
