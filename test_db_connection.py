#!/usr/bin/env python3
"""
Standalone script to test database connection
"""

from database import test_database_connection, get_database_info

if __name__ == "__main__":
    print("Testing database connection...")
    print("-" * 40)
    
    # Test basic connection
    is_connected = test_database_connection()
    
    if is_connected:
        # Get database information
        db_info = get_database_info()
        if db_info:
            print(f"Database Version: {db_info}")
    
    print("-" * 40)
    print(f"Connection Status: {'✅ Connected' if is_connected else '❌ Not Connected'}")
