from collections import Counter
from fastapi import FastAPI , Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import models ,crud
from database import engine, SessionLocal ,get_db
from models import StockSymbolRequest, SentimentResponse, Headline
import datetime
from sqlalchemy.orm import Session
import asyncio
import news  # Make sure you have a 'news.py' module with 'fetch_news_for_symbol' defined
import sentiment  # Ensure you have a 'sentiment.py' module with 'analyze_sentiment' defined



# so here defining the model which will be used to validate the request body  and verify that data conform to the format we expect
models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Diversifi News Sentiment Analysis",
    description="API for analyzing stock sentiment",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@app.post("/news-sentiment", response_model=SentimentResponse)
async def get_news_sentiment(request: StockSymbolRequest, db: Session = Depends(get_db)):
   try:
       catched_entry = crud.get_recent_sentiment(db, symbol=request.symbol)
       if catched_entry:
           # Convert SQLAlchemy model to Pydantic model
           headlines = [Headline(title=h["title"], sentiment=h["sentiment"]) for h in catched_entry.headlines]
           return SentimentResponse(
               symbol=catched_entry.symbol,
               timestamp=catched_entry.timestamp,
               headlines=headlines,
               overall_sentiment=catched_entry.overall_sentiment
           )
       

       print(f"Cache miss for {request.symbol}. Fetching new data...")

       articles=news.fetch_news_for_symbol(request.symbol)

       if not articles:
           raise HTTPException(status_code=404, detail=f"No articles found for symbol: {request.symbol}")

       headlines_texts=[article['title'] for article in articles]
       sentiment_task=[sentiment.analyze_sentiment(text) for text in headlines_texts]
       sentiments = await asyncio.gather(*sentiment_task)
       analyzed_headlines = []
       for i, article in enumerate(articles):
             analyzed_headlines.append({
                  "title": article['title'],
                  "sentiment": sentiments[i]
             })
       if sentiments:
           overall_sentiment=Counter(sentiments).most_common(1)[0][0]
       else:
           overall_sentiment = "neutral"

       response_data = {
           "symbol": request.symbol,
           "timestamp": datetime.datetime.now(),
           "headlines": analyzed_headlines,
           "overall_sentiment": overall_sentiment
       }
       created_entry = crud.create_sentiment_entry(db, response_data)
       
       # Convert to proper Pydantic response
       headlines_objects = [Headline(title=h["title"], sentiment=h["sentiment"]) for h in analyzed_headlines]
       return SentimentResponse(
           symbol=request.symbol,
           timestamp=datetime.datetime.now(),
           headlines=headlines_objects,
           overall_sentiment=overall_sentiment
       )
   
   except HTTPException:
       # Re-raise HTTP exceptions
       raise
   except Exception as e:
       # Log the error and return a proper HTTP error
       print(f"Error processing request for symbol {request.symbol}: {str(e)}")
       raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

   

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Diversifi News Sentiment Analysis API. Use /docs for API documentation."}
