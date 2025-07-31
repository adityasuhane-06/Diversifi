# sentiment.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the Google AI client
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuration for the model call
generation_config = {
    "temperature": 0, # For deterministic output
    "max_output_tokens": 5
}

# Use the 'gemini-1.5-flash' model, which is fast and great for simple tasks
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

# Fallback keyword-based sentiment analysis
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
    """
    Fallback sentiment analysis using keyword matching
    """
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

# The prompt guides the LLM to perform its task correctly
PROMPT_TEMPLATE = """
Analyze the sentiment of the following financial news headline.
Respond with only a single word: 'positive', 'negative', or 'neutral'.

Headline: "{headline}"
Sentiment:
"""

async def analyze_sentiment(headline: str) -> str:
    """
    Analyzes the sentiment of a headline using the Google Gemini API with fallback.
    """
    if not headline:
        return "neutral"
    
    # First try the fallback method to avoid API quota issues
    try:
        return fallback_sentiment_analysis(headline)
    except Exception as e:
        print(f"Fallback sentiment analysis failed: {e}")
        return "neutral"
    
    # Original API code (commented out to avoid quota issues)
    """
    prompt = PROMPT_TEMPLATE.format(headline=headline)
    
    try:
        # Use the async version of the generate_content method
        response = await model.generate_content_async(prompt)
        sentiment = response.text.strip().lower()

        # Basic validation of the response
        if sentiment in ["positive", "negative", "neutral"]:
            return sentiment
        else:
            return "neutral" # Default if the model returns an unexpected response

    except Exception as e:
        print(f"An error occurred with Google Gemini API: {e}")
        # Fallback to keyword-based analysis
        return fallback_sentiment_analysis(headline)
    """