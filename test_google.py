import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Test if API key is loaded correctly
api_key = os.getenv("GOOGLE_API_KEY")
print(f"Google API Key loaded: {api_key[:10]}..." if api_key else "No Google API Key found")

if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in environment variables")
    exit(1)

# Test the API key
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("Attempting to call Google Gemini API...")
    response = model.generate_content("Hello, test message")
    print("Google API Key is valid!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Google API Key test failed: {e}")
    import traceback
    traceback.print_exc()
