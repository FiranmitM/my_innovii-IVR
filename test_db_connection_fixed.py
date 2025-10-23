#!/usr/bin/env python3
import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="innovii",
        passwd="Innovii@123",
        database="innovii"
    )
    print("✅ Database connection successful!")
    
    # Test if we can execute queries
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("✅ Tables in database:", [table[0] for table in tables])
    
    # Check the structure of subscribers table
    print("\n📊 Checking subscribers table structure:")
    cursor.execute("DESCRIBE subscribers")
    columns = cursor.fetchall()
    for column in columns:
        print(f"  - {column[0]} ({column[1]})")
    
    # Test inserting a sample subscriber with correct columns
    try:
        # First, let's see what columns actually exist
        cursor.execute("SELECT * FROM subscribers LIMIT 1")
        print("\n🔍 Sample row from subscribers:", cursor.fetchall())
        
        # Try a simple insert with minimal columns
        cursor.execute("INSERT INTO subscribers (phone_number, is_active) VALUES ('+251911223344', 1)")
        db.commit()
        print("✅ Subscriber insertion test: PASSED")
        
        # Clean up
        cursor.execute("DELETE FROM subscribers WHERE phone_number = '+251911223344'")
        db.commit()
        
    except Exception as insert_error:
        print("❌ Subscriber insertion test: FAILED -", insert_error)
    
    cursor.close()
    db.close()
    
except Exception as e:
    print("❌ Database connection failed:", e)
