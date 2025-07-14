
# 🛒 FeelCart – Shop What You Feel

**An AI-Powered shopping assistant that personalizes Walmart shopping using real-time mood detection and smart cart automation**

FeelCart is an intelligent, dual-module shopping system that enhances user experience by combining two independent yet powerful features:

- 🧠 **MoodCart**: Recommends products based on how you feel using mood classification and sentiment-aware mapping.
- 🤖 **AutoCart**: Automatically fills your cart with frequently bought, trending, or refill-needed items based on past user behavior and smart logic.

Together, these modules redefine shopping personalization — one based on **emotions**, and the other based on **habits**.

---

## 🌟 Key Modules

### 🧠 MoodCart – Shop by Emotion
- Detects the user's mood using Natural Language Processing.
- Maps mood to relevant product categories (e.g., *happy → party supplies*).
- Fetches product recommendations in real time using Walmart’s SerpAPI.
- Stores user mood history and visualizes mood trends over time.

### 🤖 AutoCart – Shop by Behavior
- Analyzes past user purchases and refill patterns.
- Identifies top-used or trending items based on frequency and category.
- Automatically fills a smart cart with personalized essentials.
- Encourages sustainable shopping with refill reminders and item prioritization.

> 💡 Both modules work **independently** and can be used based on user preference.

---

## 💼 Use Cases

- 😌 **Emotion Shopping**: Feeling sad? Get suggestions for comfort items like snacks, candles, or books.
- ⏰ **Routine Shopping**: Low on groceries? AutoCart identifies what you need and adds it to your cart.
- 📈 **Mood Insights**: Visualize how your moods change over time and how they influence your shopping behavior.

---

## 🛠️ Tech Stack

| Component         | Tools / Libraries                               |
|------------------ |-------------------------------------------------|
| Frontend UI       | Streamlit                                       |
| ML/NLP            | Hugging Face Transformers, joblib               |
| Backend           | Python, Pandas, Requests, JSON, MySQL           |
| Data Source       | Walmart Product Search (via SerpAPI)            |
| Visualization     | Plotly Express                                  |
| Deployment Ready  | Local + WebApp with API modularity              |

---

## 📁 Project Structure

```
FeelCart-ShopWhatYouFeel/
├── main_app.py                   # Main Streamlit interface
├── autocart_engine.py            # AutoCart logic engine
├── moodcart_model.py             # NLP-based mood classifier
├── mood_map.json                 # Maps mood to product categories
├── walmart_api.py                # Product data fetcher (Walmart SerpAPI)
├── user_history.json             # User shopping behavior history
├── mood_history.json             # Mood logs
├── requirements.txt              # Dependencies
└── README.md                     # Project documentation
```

---

## 📸 Screenshots (Add Yours)

> *(Add screenshots of MoodCart, AutoCart output, and mood timeline graphs here)*

---

## ⚙️ Installation & Usage

### 🔧 Setup

```bash
git clone https://github.com/Shafia-01/FeelCart-ShopWhatYouFeel.git
cd FeelCart-ShopWhatYouFeel
pip install -r requirements.txt
```

### 🔑 Configure SerpAPI Key

- Get a free API key from [SerpAPI](https://serpapi.com/)
- Set the API key in your environment:

```bash
export SERPAPI_KEY="your_api_key"
```

### ▶️ Run the Application

```bash
streamlit run app.py
```

You will be prompted to choose either:
- **AutoCart** to auto-fill based on past behavior, or
- **MoodCart** to receive mood-based recommendations.

---

## 🧠 How Each Module Works

### MoodCart
1. User enters mood in plain text.
2. NLP model classifies mood → maps it to product categories.
3. Products are fetched using SerpAPI → shown to the user.
4. Mood and timestamp are saved to the database for future insights.

### AutoCart
1. Reads past purchases from `user_history.json` or database.
2. Identifies frequently bought items or those due for refill.
3. Fetches updated product data and auto-generates a personalized cart.

---

## 📊 Mood Timeline Visualization

MoodCart includes a timeline graph that visualizes your past moods, enabling:
- Emotional shopping trend analysis
- Mood-product correlation tracking
- Smart insights for personalized experiences

---

## 📌 Future Enhancements

- 🧾 Smart wishlist creation based on recurring items (AutoCart)
- 💬 GPT-based mood extraction from longer text
- 🛍️ Integration with Flipkart/Amazon APIs
- 📲 Mobile-first UI with persistent logins
- 🌱 Sustainability nudger based on emotion–impact mapping

---

## 🙌 Team & Contributors

- 👩‍💻 **Shafia Ameeruddin** — Core Developer & Designer

_This project was developed for Sparkathon 2025 (Walmart) to promote sustainable, personalized shopping experiences._

---

## 🤝 Contribution Guidelines

Feel free to fork, improve, and open pull requests. Suggestions and feedback are always welcome.

---

## 📃 License

MIT License. See `LICENSE` file for details.

---

> ✨ *"FeelCart brings emotion and efficiency together — shopping that truly understands you."* ✨
