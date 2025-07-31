from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models


def get_recent_sentiment(db:Session,symbol:str):
    """
    Fetch the most recent sentiment for a given stock symbol.
    """
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)

    return db.query(models.NewsSentiment).filter(
        models.NewsSentiment.symbol == symbol,
        models.NewsSentiment.timestamp >= ten_minutes_ago
    ).first()

def create_sentiment_entry(db:Session,response_data:dict):
    db_entry=models.NewsSentiment(
        symbol=response_data['symbol'],
        timestamp=datetime.now(),
        headlines=response_data['headlines'],
        overall_sentiment=response_data.get('overall_sentiment', 'neutral')
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_sentiment_history(db:Session, symbol:str, days:int=30):
    """
    Fetch sentiment history for a given stock symbol over the last 'days' days.
    """
    start_date = datetime.now() - timedelta(days=days)
    return db.query(models.NewsSentiment).filter(
        models.NewsSentiment.symbol == symbol,
        models.NewsSentiment.timestamp >= start_date
    ).order_by(models.NewsSentiment.timestamp.desc()).all()

def delete_old_sentiments(db:Session,days:int=30):
    """
    Delete sentiments older than 'days' days.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    db.query(models.NewsSentiment).filter(
        models.NewsSentiment.timestamp<=cutoff_date
    ).delete(synchronize_session=False)
    db.commit()

def get_all_symbols(db:Session):
    """
    Fetch all unique stock symbols from the database.
    """
    return db.query(models.NewsSentiment.symbol).distinct().all()

def get_sentiment_bysymbol(db:Session,symbol:str):
    """
    Fetch all sentiments for a given stock symbol.
    """
    return db.query(models.NewsSentiment).filter(
        models.NewsSentiment.symbol == symbol
    ).order_by(models.NewsSentiment.timestamp.desc()).all()