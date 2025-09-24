from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def score_text(text: str) -> tuple[str, float]:
    scores = sia.polarity_scores(text)
    compound = float(scores["compound"])
    if compound >= 0.05:
        label = "pos"
    elif compound <= -0.05:
        label = "neg"
    else:
        label = "neu"
    return label, compound