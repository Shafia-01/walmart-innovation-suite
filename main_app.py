import os
import nest_asyncio
import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import mysql.connector
from MOODCART.moodcart_model import predict_mood_category
import time
from datetime import datetime, timedelta
from pathlib import Path
from AUTOCART.walmart_api import fetch_trending_products
from AUTOCART.autocart_engine import generate_autocart
from dotenv import load_dotenv
load_dotenv()

nest_asyncio.apply()
st.set_page_config(
    page_title="CartVerse: Walmart Innovation Suite",
    page_icon="🛍️",
    layout="centered"
)

# ------------------ Walmart UI THEME CSS (Final Polished Version) ------------------ 
st.markdown("""
<style>
/* Global Font */
html, body, [class*="css"]  {
    font-family: Cambria, serif !important;
}

/* App background */
.stApp {
    background-color: #FFFFFF;
}

/* Title Only */
h1 {
    color: #001F5B !important;  /* Navy Blue */
    font-family: Cambria, serif !important;
}

/* Other Headings */
h2, h3 {
    color: #0071CE !important;  /* Walmart Blue */
    font-family: Cambria, serif !important;
}

/* Buttons */
.stButton > button {
    background-color: #0071CE;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-family: Cambria, serif !important;
}
.stButton > button:hover {
    background-color: #005A9C;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFC220 !important;
    color: #1A1A1A !important;
}
section[data-testid="stSidebar"] label {
    color: #1A1A1A !important;
    font-weight: 600;
    font-family: Cambria, serif !important;
}
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stSelectbox div[role="combobox"] {
    background-color: white !important;
    color: #1A1A1A !important;
    border-radius: 8px;
    border: 1px solid #C6C6C6;
    font-family: Cambria, serif !important;
}
section[data-testid="stSidebar"] svg {
    fill: #1A1A1A !important;
}

/* Centered Tabs Container */
div[data-testid="stTabs"] {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
}

/* Tab Buttons */
[data-testid="stTabs"] button {
    background-color: #E6F1FB;
    border-radius: 10px 10px 0 0;
    padding: 0.5rem 1rem;
    font-weight: bold;
    font-size: 16px;
    font-family: Cambria, serif !important;
    color: #1A1A1A;
    margin: 0 5px;
    border: none;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    background-color: #001F5B;
    color: white;
    border-bottom: 3px solid #FFA500;
}

/* Centered Content Block */
.block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Input Fields */
input, textarea, select {
    border-radius: 6px;
    border: 1px solid #C6C6C6;
    font-family: Cambria, serif !important;
}

/* Streamlit TextArea (Pure Yellow) */
section[data-testid="stTextArea"] textarea {
    background-color: #FFD700 !important;
    color: #1A1A1A !important;
    border-radius: 8px;
    border: 1px solid #C6C6C6;
    font-family: Cambria, serif !important;
    padding: 10px;
}

/* Image Styling */
img {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Link Styling */
a {
    color: #0071CE;
    text-decoration: none;
    font-family: Cambria, serif !important;
}
a:hover {
    text-decoration: underline;
}

/* Markdown Containers */
[data-testid="stMarkdownContainer"] > div {
    background-color: #E6F1FB;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
    font-family: Cambria, serif !important;
}

/* Highlight Boxes */
.highlight-box {
    background-color: #FCEADE;
    padding: 1rem;
    border-radius: 10px;
    font-weight: bold;
    color: #1A1A1A;
    font-family: Cambria, serif !important;
}

/* Footer */
footer {
    visibility: hidden;
}
            
/* Center the tab selector (MoodCart & AutoCart buttons) */
div[data-testid="stTabs"] {
    display: flex;
    justify-content: center !important;
    align-items: center;
    margin-top: 1rem;
    margin-bottom: 2rem;
}

/* Optional: make the tab container itself centered */
section[data-testid="stTabbedContent"] {
    display: flex;
    flex-direction: column;
    align-items: center;
}
            
/* Center the entire tabs section */
[data-testid="stTabs"] {
    display: flex;
    justify-content: center !important;
    margin-top: 1rem;
}

/* Optional: Center the tab contents */
section[data-testid="stTabbedContent"] > div {
    display: flex;
    flex-direction: column;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 42px; font-weight: bold; color: #001F5B; font-family: Cambria, serif;'>
🛍️ CartVerse
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; font-style: italic; font-weight: bold; color: #0071CE; font-size: 18px;'>Walmart Innovation Suite</p>",
    unsafe_allow_html=True
)

# --- Database Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MOODCART_DB_HOST"),
        user=os.getenv("MOODCART_DB_USER"),
        password=os.getenv("MOODCART_DB_PASSWORD"),
        database=os.getenv("MOODCART_DB_NAME")
    )

# --- Load Mood History ---
def load_mood_history(user_id="user_001"):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT timestamp, mood, category, adjusted_category, interest, age, gender 
            FROM mood_history 
            WHERE user_id = %s 
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"❌ Failed to load mood history: {e}")
        return []

# --- Load JSON State ---
mood_file = Path(__file__).parent / "mood_history.json"
if "mood_memory" not in st.session_state:
    if mood_file.exists():
        with mood_file.open("r") as f:
            st.session_state.mood_memory = json.load(f)
    else:
        st.session_state.mood_memory = []
if "mood_memory" not in st.session_state:
    st.session_state.mood_memory = []

# --- Fallback Keywords ---
fallback_keywords = {
    "collectibles or hobby kits for adults": {
        "Technology": "arduino kit",
        "Fashion": "diy jewelry kit",
        "Sports": "sports memorabilia",
        "Books & Learning": "adult puzzle book",
        "Gaming": "mini gaming collectibles",
        "General": "hobby kits"
    },
    "educational toys for kids": {
        "Gaming": "learning tablet",
        "Technology": "robotics kit for kids",
        "Books & Learning": "story book box",
        "General": "lego set"
    },
    "wellness products for fitness & wellness": {
        "General": "essential oils",
        "Fitness & Wellness": "yoga mat",
        "Books & Learning": "wellness journal"
    },
    "trendy apparel": {
        "Fashion": "trendy dresses",
        "Gaming": "anime tshirts",
        "Sports": "sports jerseys",
    },
}

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
if not SERPAPI_KEY:
    st.error("🔐 SERPAPI_KEY not found. Set it as an environment variable.")


def build_search_term(category, interest):
    stopwords = {"or", "for", "and", "of", "kits", "adults", "teens", "kids", "collectibles", "products", "items"}
    merged = f"{category} {interest}".lower().split()
    filtered = []
    for word in merged:
        if word not in stopwords and word not in filtered:
            filtered.append(word)
    return " ".join(filtered[:3])

def _fetch_products_raw(search_query):
    if not SERPAPI_KEY:
        raise ValueError("SerpApi key is missing!")

    params = {
        "engine": "walmart",
        "api_key": SERPAPI_KEY,
        "query": search_query,
        "num": 5
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=60)
        if response.status_code == 429:
            raise requests.exceptions.HTTPError("429 Too Many Requests", response=response)
        response.raise_for_status()
        results = response.json()

        raw_items = results.get("shopping_results", []) or results.get("organic_results", [])

        if not raw_items:
            return []

        products = []
        for item in raw_items:
            name = item.get("title") or item.get("name") or "No title"
            link = item.get("link") or item.get("product_link") or item.get("url") or "#"
            image = item.get("thumbnail") or item.get("image") or None

            if not link.startswith("http"):
                link = "https://www.walmart.com" + link

            products.append({
                "name": name,
                "link": link,
                "image": image
            })

        return products

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            raise e
        if "429" in str(e):
            raise e
        st.error(f"Network error: {e}")
        return []
    except requests.exceptions.RequestException as e:
        if e.response is not None and e.response.status_code == 429:
            raise requests.exceptions.HTTPError("429 Too Many Requests", response=e.response)
        if "429" in str(e):
            raise requests.exceptions.HTTPError("429 Too Many Requests", response=e.response)
        st.error(f"Network error: {e}")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return []

@st.cache_data(ttl=3600)
def fetch_products(search_query):
    products = _fetch_products_raw(search_query)
    if not products:
        raise ValueError("No products found")
    return products

def fetch_products_with_retry(query, serpapi_key=SERPAPI_KEY, max_retries=2, delay=3):
    for attempt in range(max_retries):
        try:
            products = fetch_products(query)
            return products
        except requests.exceptions.HTTPError as e:
            if (e.response is not None and e.response.status_code == 429) or "429" in str(e):
                st.warning(f"Rate limit hit. Retry {attempt + 1} of {max_retries}")
                time.sleep(delay)
            else:
                return []
        except ValueError as e:
            if str(e) == "SerpApi key is missing!":
                st.error("SerpApi key is missing!")
            return []
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return []
    return []

# --- TABS ---
tab1, tab2 = st.tabs(["🧠 MoodCart", "🔍 AutoCart"])

# --- MoodCart Tab ---
with tab1:
    st.markdown("""
<div style='
    font-size: 32px;
    font-weight: bold;
    color: #1A1A1A;
    background-color: #E6F1FB;
    padding: 12px 24px;
    border-radius: 12px;
    text-align: center;
    font-family: Cambria, serif;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
'>
🧠 MoodCart: Shop by Mood
</div>
""", unsafe_allow_html=True) 

    age = st.sidebar.number_input("Your age", min_value=1, max_value=120, value=25)
    interest = st.sidebar.selectbox("Select your interest", ["General", "Technology", "Fashion", "Sports", "Home Decor", "Books & Learning", "Fitness & Wellness", "Gaming"])
    gender = st.sidebar.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
    user_text = st.text_area("Tell us how you feel today:", placeholder="e.g., I'm feeling a bit down...")

    if st.button("Get Recommendations"):
        if user_text.strip():
            mood, _, confidence = predict_mood_category(user_text)
            BASE_DIR = Path(__file__).parent.resolve()
            MOOD_MAP_PATH = BASE_DIR / "MOODCART" / "mood_map.json"
            with open(MOOD_MAP_PATH, "r") as f:
                mood_map = json.load(f)
            mapped_category = mood_map.get(mood.lower(), "essentials")

            def adjust_category(category, age, interest, gender):
                category = category.lower()
                if age < 13:
                    age_group = "child"
                elif 13 <= age <= 19:
                    age_group = "teen"
                else:
                    age_group = "adult"
                # ... same as before ...
                if category == "toys":
                    return "educational toys for kids" if age_group == "child" else (
                        "fun gadgets for teens" if age_group == "teen" else "collectibles or hobby kits for adults"
                    )
                elif category in ["books", "motivational books", "self-help books", "educational kits"]:
                    if age < 18:
                        return "young adult books"
                    elif interest == "Technology":
                        return "technology learning books"
                    elif interest == "Fitness & Wellness":
                        return "mindfulness and wellness books"
                    else:
                        return "inspirational books"
                elif category in ["party supplies", "romantic gifts", "thank-you gifts", "gifts"]:
                    return "fun gift sets for teens" if age < 16 else f"{category} for {interest.lower()}"
                elif category == "electronics":
                    return "gaming gadgets" if interest == "Gaming" else (
                        "latest tech gadgets" if interest == "Technology" else "affordable electronics"
                    )
                elif category == "sports equipment":
                    if age < 18:
                        return "sports gear for teens"
                    elif gender == "Female":
                        return "sports gear for women"
                    elif gender == "Male":
                        return "sports gear for men"
                    else:
                        return "unisex sports gear"
                elif category == "stress relief toys":
                    return "fidget and stress toys"
                elif category == "wellness products":
                    if gender == "Female":
                        return "wellness products for women"
                    elif gender == "Male":
                        return "wellness products for men"
                    else:
                        return "unisex wellness products"
                elif category == "candles":
                    return "aromatherapy candles"
                elif category == "home decor":
                    return f"cozy home decor for {interest.lower()}"
                elif category == "fitness gear":
                    return "home workout fitness gear"
                elif category == "tea and coffees":
                    return "gourmet tea and coffee sets"
                elif category == "retro items":
                    return "nostalgic collectibles"
                elif category == "security gadgets":
                    return "smart home security devices"
                elif category == "stationery":
                    return "motivational stationery kits"
                elif category == "essentials":
                    return f"daily essentials for {interest.lower()}"
                elif category == "fashion":
                    if gender == "Male":
                        return "men's fashion"
                    elif gender == "Female":
                        return "women's fashion"
                    else:
                        return "unisex fashion"
                elif category == "games":
                    return "educational games for kids" if age_group == "child" else (
                        "party board games for teens" if age_group == "teen" else "strategy board games for adults"
                    )
                elif category == "boxing gloves":
                    if age < 18:
                        return "boxing gloves for youth"
                    elif gender == "Female":
                        return "boxing gloves for women"
                    elif gender == "Male":
                        return "boxing gloves for men"
                    else:
                        return "unisex boxing gloves"
                elif category == "romantic gifts":
                    return "romantic gifts for couples" if gender != "Prefer not to say" else category
                return category
             
            adjusted_category = adjust_category(mapped_category, age, interest, gender)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.mood_memory.append({
                "timestamp": timestamp,
                "mood": mood,
                "category": mapped_category,
                "adjusted_category": adjusted_category,
                "interest": interest,
                "age": age,
                "gender": gender
            })
            
            timestamp = datetime.now()
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                insert_query = """
                INSERT INTO mood_history (
                user_id, timestamp, mood, category, adjusted_category, interest, age, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
                values = (
                    "user_001",         
                    timestamp,          
                    mood,
                    mapped_category,
                    adjusted_category,
                    interest,
                    age,
                    gender
                )
                cursor.execute(insert_query, values)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                st.error(f"❌ Failed to save to database: {e}") 
            
            with st.expander("🧠 View Your Mood History"):
                if st.session_state.mood_memory:
                    for record in reversed(st.session_state.mood_memory[-5:]):
                        st.markdown(f"""
                                    - 🕓 `{record['timestamp']}`
                                    - Mood: **{record['mood'].capitalize()}**
                                    - Adjusted Category: `{record['adjusted_category']}`
                                    - Age: {record['age']} | Gender: {record['gender']} | Interest: {record['interest']}
                                    ---
                                """)
                else:
                    st.write("No mood history yet.")
            
            with st.expander("📈 Mood Timeline Tracker"):
                mood_rows = load_mood_history()
                if mood_rows:
                    mood_df = pd.DataFrame(mood_rows)
                    mood_df["timestamp"] = pd.to_datetime(mood_df["timestamp"])
                    filter_option = st.radio("Filter by:", ["All time", "Last 7 days", "Last 30 days"], horizontal=True)
                    now = datetime.now()
                    
                    if filter_option == "Last 7 days":
                        mood_df = mood_df[mood_df["timestamp"] >= now - timedelta(days=7)]
                    elif filter_option == "Last 30 days":
                        mood_df = mood_df[mood_df["timestamp"] >= now - timedelta(days=30)]
                    if not mood_df.empty:
                        fig = px.line(
                            mood_df,
                            x="timestamp",
                            y="mood",
                            title=f"Mood Tracker ({filter_option})",
                            markers=True,
                            labels={"timestamp": "Date/Time", "mood": "Mood"},
                            color_discrete_sequence=["#36a2eb"]
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No mood data found for selected range.")
                else:
                    st.info("No mood data available yet.")

            st.success(f"**Detected Mood:** {mood.capitalize()} (confidence: {confidence:.2f})")
            st.caption(f"🎯 Mapped from mood → category: `{mapped_category}` → Final adjusted: `{adjusted_category}`")

            search_term = fallback_keywords.get(adjusted_category.lower(), {}).get(interest, None)
            if not search_term:
                search_term = build_search_term(adjusted_category, interest)
            st.write(f"🔎 Search query being used: '{search_term}'")

            products = fetch_products_with_retry(search_term)
            if not products:
                st.warning(f"No products found for: '{search_term}'. Trying fallback with interest only...")
                fallback_search = interest
                products = fetch_products_with_retry(fallback_search)
                if not products:
                    st.error("Still no products found. Try another mood or check your API quota.")

            st.write("### 🛍️ Suggested Products:")
            for i in range(0, len(products), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(products):
                        item = products[i + j]
                        search_url = f"https://www.walmart.com/search?q={item['name'].replace(' ', '+')}"
                        with cols[j]:
                            if item.get("image"):
                                st.image(item["image"], width=200)
                            st.markdown(f"**[{item['name']}]({search_url})**", unsafe_allow_html=True)
                            st.markdown("---")

# --- AutoCart Tab ---
with tab2:
    st.markdown("""
<div style='
    font-size: 32px;
    font-weight: bold;
    color: #1A1A1A;
    background-color: #E6F1FB;
    padding: 12px 24px;
    border-radius: 12px;
    text-align: center;
    font-family: Cambria, serif;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
'>
🔎 AutoCart: Smart Shopping Assistant
</div>
""", unsafe_allow_html=True) 

    query = st.text_input("Search for products", placeholder="e.g. shampoo, soap, banana")

    if st.button("Search"):
        if query.strip():
            st.subheader("🔍 Search Results")
            results = fetch_trending_products(query, num_results=5)
            if results:
                for product in results:
                    name = product.get('title') or product.get('name') or product.get('item') or 'Unnamed Product'
                    link = product.get('link', '#')
                    st.markdown(f"**{name}**")
                    st.markdown(f"[View Product]({link})")
                    st.markdown("---")
            else:
                st.warning("No products found.")
        else:
            st.error("Please enter a valid search query.")

    history_exists = True
    user_data = {}
    try:
        BASE_DIR = Path(__file__).parent.resolve()
        USER_HISTORY_PATH = BASE_DIR / "AUTOCART" / "user_history.json"
        with open(USER_HISTORY_PATH, "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        st.error("❌ user_history.json not found!")
        history_exists = False

    if history_exists:
        user_ids = list(user_data.keys())
        selected_user = st.selectbox("👤 Select User", user_ids)

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

# --- Save Mood History ---
if st.session_state.get("mood_memory"):
    with mood_file.open("w") as f:
        json.dump(st.session_state.mood_memory, f, indent=4)

st.markdown(
    """
    <hr style="border-top: 1px solid #ccc;">
    <center>
        <span style="color: #0071CE;">Inspired by Walmart</span> | 
        <span style="color: #FFC220;">CartVerse</span> © 2025
    </center>
    """,
    unsafe_allow_html=True
)
