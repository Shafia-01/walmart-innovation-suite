
# FeelCart – Shop What You Feel

FeelCart is a Streamlit-powered shopping assistant that personalizes Walmart product discovery in two ways:
- 🧠 **MoodCart**: turns what you feel into product categories and recommends items that fit your mood.
- 🤖 **AutoCart**: mines past shopping behavior to suggest refills and trending alternatives automatically.

Both modules can run on their own or through the combined `main_app.py` experience.

---

## What’s inside

```
├── main_app.py                 # Unified UI for MoodCart + AutoCart with theming
├── mood_history.json           # Local cache of mood entries (also saved to MySQL if available)
├── MOODCART/
│   ├── app.py                  # Standalone MoodCart UI
│   ├── mood_map.json           # Mood → category mapping
│   └── moodcart_model.py       # Emotion classifier + TextBlob fallback
├── AUTOCART/
│   ├── app.py                  # Standalone AutoCart UI
│   ├── autocart_engine.py      # Cart generation pipeline
│   ├── autocart_rules.py       # Frequency, refill placeholder, category mapping
│   ├── walmart_api.py          # Walmart search via SerpAPI
│   └── user_history.json       # Sample past purchases per user
├── requirements.txt
└── README.md
```

Key data files:
- `MOODCART/mood_map.json` maps emotions (e.g., joy, sadness) to categories.
- `AUTOCART/user_history.json` stores prior purchases used to rank and refill items.
- `mood_history.json` locally persists mood interactions; MySQL persistence is optional.

---

## Features

- **Mood understanding**: Hugging Face emotion classifier (`bhadresh-savani/distilbert-base-uncased-emotion`) with a TextBlob sentiment fallback and direct keyword lookup.
- **Personalized category adjustment**: age/interest/gender-aware category tweaks (e.g., toys → educational kits for kids).
- **Product search**: SerpAPI Walmart search for real-time results with retry handling.
- **Behavioral carting**: frequency-based item ranking, category tagging, and trending-product suggestions.
- **History and insights**: optional MySQL storage plus local JSON cache, with a timeline view filtered by 7/30/all-time windows.
- **Polished UI**: custom Walmart-inspired theming, dual tabs for MoodCart and AutoCart, and two-column product layouts.

---

## Quickstart

1) Clone and install
```bash
pip install -r requirements.txt
```

2) Set your SerpAPI key (required for both modules)
```bash
export SERPAPI_KEY="your_api_key"   # PowerShell: $Env:SERPAPI_KEY="your_api_key"
```

3) (Optional) MySQL setup for mood history  
Create a `moodcart_db` database with a `mood_history` table and user matching the hardcoded credentials in `main_app.py`/`MOODCART/app.py` (`root` / `Shafo@05`). If MySQL is unavailable, the app still runs using local `mood_history.json`.

4) Run the combined experience
```bash
streamlit run main_app.py
```

5) Or run modules individually
```bash
streamlit run MOODCART/app.py   # mood-based shopping
streamlit run AUTOCART/app.py   # behavior-based carting
```

---

## How it works

### MoodCart flow
1. User enters free-form text about their mood.
2. `predict_mood_category` classifies emotion (Hugging Face) or falls back to keyword/TextBlob.
3. Mood is mapped to a category via `mood_map.json`, then adjusted using age, interest, and gender.
4. A concise Walmart search term is built; SerpAPI fetches products with retry handling.
5. Mood events are saved locally and (optionally) to MySQL, with a Plotly timeline for insights.

### AutoCart flow
1. Past purchases load from `AUTOCART/user_history.json`.
2. `get_top_n_items` ranks frequent items; `needs_refill` (currently a placeholder that always refills) decides inclusion.
3. Each item is labeled with a coarse category via `CATEGORY_MAPPING`.
4. SerpAPI pulls trending options per item; the top suggestion is attached to the generated cart.

---

## Configuration reference

- **Environment**: `SERPAPI_KEY` must be set.
- **Data**: `user_history.json` drives AutoCart; edit it to mirror your users.  
  Example entry:
  ```json
  {
    "user_001": [
      {"item": "milk"}, {"item": "banana"}, {"item": "coffee"}
    ]
  }
  ```
- **MySQL**: credentials and DB/table names are defined in `get_db_connection()` inside the Streamlit apps.

---

## Known gaps & next steps

- `needs_refill` is stubbed to always return `True`; add real refill logic based on recency or quantity.
- Credentials are hardcoded in code for demo purposes; move them to `.env` in production.
- SerpAPI errors are surfaced in the UI; consider broader rate-limit backoff and logging.
- Add tests around mood mapping, refill logic, and SerpAPI parsing as the logic evolves.

---

## License

MIT License. See `LICENSE` for details.
