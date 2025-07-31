import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the Google AI client
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuration for the model call
generation_config = {
    "temperature": 0,
    "max_output_tokens": 5
}

model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

PROMPT_TEMPLATE = """
Analyze the sentiment of the following financial news headline.
Respond with only a single word: 'positive', 'negative', or 'neutral'.

Headline: "{headline}"
Sentiment:
"""

POSITIVE_WORDS = [
    "profit", "growth", "gain", "surge", "rally", "boost", "rise", "up", "bullish",
    "positive", "strong", "beat", "exceed", "outperform", "success", "win", "increase",
    "soar", "climb", "advance", "optimistic", "confident", "breakthrough", "improved"
]

NEGATIVE_WORDS = [
    "loss", "decline", "fall", "drop", "crash", "bear", "down", "weak", "miss",
    "underperform", "fail", "decrease", "plunge", "tumble", "sink", "negative",
    "recession", "crisis", "concern", "worry", "fear", "risk", "warning", "cut"
]

def fallback_sentiment_analysis(headline: str) -> str:
    if not headline:
        return "neutral"
    
    headline_lower = headline.lower()
    positive_count = sum(1 for word in POSITIVE_WORDS if word in headline_lower)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in headline_lower)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

async def analyze_sentiment(headline: str) -> str:
    if not headline:
        return "neutral"

    try:
        prompt = PROMPT_TEMPLATE.format(headline=headline)
        response = await model.generate_content_async(prompt)
        sentiment = response.text.strip().lower()

        if sentiment in ["positive", "negative", "neutral"]:
            return sentiment
        else:
            print("API returned invalid sentiment, using fallback.")
            return fallback_sentiment_analysis(headline)
    except Exception as e:
        print(f"An error occurred with Google Gemini API: {e}. Using fallback.")
        return fallback_sentiment_analysis(headline)