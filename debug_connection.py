#!/usr/bin/env python3
"""
Debug script to test database connection and identify issues
"""

import os
import traceback
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def test_connection():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database credentials
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        
        print(f"DB_USER: {db_user}")
        print(f"DB_HOST: {db_host}")
        print(f"DB_PORT: {db_port}")
        print(f"DB_NAME: {db_name}")
        print(f"DB_PASSWORD: {'***' if db_password else 'None'}")
        
        # Build connection string
        DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print(f"\nConnection string: {DATABASE_URL.replace(db_password, '***')}")
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"\n✅ Database connection successful!")
            print(f"PostgreSQL version: {version}")
            
            # Test if the table exists
            result = connection.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'news_sentiment')"))
            table_exists = result.fetchone()[0]
            print(f"Table 'news_sentiment' exists: {table_exists}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection failed!")
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    print("-" * 50)
    test_connection()
