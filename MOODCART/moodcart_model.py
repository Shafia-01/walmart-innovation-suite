import json
import re
from pathlib import Path
from transformers import pipeline
from textblob import TextBlob

# Module-level lazy singleton variable
_emotion_classifier = None

def get_emotion_classifier():
    global _emotion_classifier
    if _emotion_classifier is None:
        _emotion_classifier = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            device=-1
        )
    return _emotion_classifier

with open(Path(__file__).parent / "mood_map.json", "r") as f:
    mood_map = json.load(f)

def direct_mood_lookup(text):
    """
    Check if user text contains an explicit mood word from mood_map.json.
    If found, return it immediately with mapped category.
    """
    text_lower = text.lower()
    for mood_word in mood_map.keys():
        if re.search(r'\b' + re.escape(mood_word) + r'\b', text_lower):
            return mood_word, mood_map[mood_word]
    return None, None

def predict_mood_category(text):
    mood_direct, category_direct = direct_mood_lookup(text)
    if mood_direct:
        return mood_direct, category_direct, 1.0
    try:
        classifier = get_emotion_classifier()
        prediction = classifier(text)[0]
        mood = prediction["label"].lower()
        score = prediction["score"]
    except Exception as e:
        print(f"Hugging Face model failed: {e}")
        mood, score = fallback_sentiment(text)

    category = mood_map.get(mood, "essentials")
    return mood, category, score

def fallback_sentiment(text):
    """
    Backup: Use TextBlob if the Hugging Face model fails.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        mood = "joy"
    elif polarity < -0.1:
        mood = "sadness"
    else:
        mood = "neutral"
    return mood, abs(polarity)