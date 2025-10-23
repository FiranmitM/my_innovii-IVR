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
        # Use the actual column names: phone_number, subscribed, preferred_language
        cursor.execute("INSERT INTO subscribers (phone_number, subscribed, preferred_language) VALUES ('+251911223344', 1, 'amharic')")
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
