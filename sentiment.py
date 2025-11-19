import requests
from bs4 import BeautifulSoup

# ============================================================
#                  MÓDULO DE NOTICIAS Y SENTIMIENTO
# ============================================================

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://news.bitcoin.com/feed/",
    "https://cryptonews.com/news/feed"
]

KEYWORDS_BULLISH = [
    "etf", "approval", "spot", "accumulation", "buying",
    "positive", "bullish", "institutional", "integration"
]

KEYWORDS_BEARISH = [
    "hack", "exploit", "rug", "breach", "lawsuit",
    "sell-off", "ban", "penalty", "shutdown", "negative"
]

def fetch_rss(url):
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.content, "xml")
        items = soup.findAll("item")[:5]
        return items
    except:
        return []

def classify_sentiment(text):
    t = text.lower()

    for w in KEYWORDS_BULLISH:
        if w in t:
            return "🟢 Positivo", "Alcista"

    for w in KEYWORDS_BEARISH:
        if w in t:
            return "🔴 Negativo", "Bajista"

    return "⚪ Neutral", "Indefinido"

def analyze_news():
    events = []

    for feed in RSS_FEEDS:
        items = fetch_rss(feed)

        for item in items:
            try:
                title = item.title.text
                desc = item.description.text

                full = f"{title}. {desc}"

                icon, sentiment = classify_sentiment(full)

                events.append({
                    "title": title,
                    "sentiment": sentiment,
                    "icon": icon
                })

            except:
                continue

    return events[:8]

def get_strong_news():
    events = analyze_news()
    filtered = []

    for e in events:
        if e["sentiment"] in ["Alcista", "Bajista"]:
            filtered.append(e)

    return filtered[:5]
