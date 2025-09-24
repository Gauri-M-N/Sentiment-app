import os
import nltk

# Ensure VADER lexicon exists on Render
NLTK_DIR = os.getenv("NLTK_DATA", "/opt/render/nltk_data")
nltk.data.path.append(NLTK_DIR)
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", download_dir=NLTK_DIR, quiet=True)

from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def score_text(text: str) -> tuple[str, float]:
    s = sia.polarity_scores(text)
    c = float(s["compound"])
    label = "pos" if c >= 0.05 else "neg" if c <= -0.05 else "neu"
    return label, c
