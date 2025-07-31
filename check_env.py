#!/usr/bin/env python3
"""
Check if environment variables are properly set
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_env_variables():
    """Check if all required environment variables are set"""
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    
    print("Checking environment variables:")
    print("-" * 40)
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Don't print the password for security
            display_value = "*" * len(value) if var == 'DB_PASSWORD' else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    print("-" * 40)
    if missing_vars:
        print(f"Missing variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return False
    else:
        print("All environment variables are set!")
        return True

if __name__ == "__main__":
    check_env_variables()
