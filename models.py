import datetime
from sqlalchemy import Column,Integer,String,DateTime,JSON
from pydantic import BaseModel,Field
from typing import List ,Optional
from database import Base

class NewsSentiment(Base):
    __tablename__ = "news_sentiment"

    id = Column(Integer, primary_key=True, index=True)
    symbol=Column(String, index=True,nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    headlines=Column(JSON, nullable=False)
    overall_sentiment=Column(String, nullable=True)

# Pydantic model for request validation
class Headline(BaseModel):
    title:str
    sentiment:str
class SentimentResponse(BaseModel):
    symbol:str
    timestamp:datetime.datetime
    headlines:List[Headline]
    overall_sentiment:Optional[str] = None

class StockSymbolRequest(BaseModel):
    symbol:str=Field(...,max_length=10)