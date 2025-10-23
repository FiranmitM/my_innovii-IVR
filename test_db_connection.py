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
    
    # Test inserting a sample subscriber
    try:
        cursor.execute("INSERT INTO subscribers (phone_number, language, is_active) VALUES ('+251911223344', 'amharic', 1)")
        db.commit()
        print("✅ Subscriber insertion test: PASSED")
    except Exception as insert_error:
        print("❌ Subscriber insertion test: FAILED -", insert_error)
    
    cursor.close()
    db.close()
    
except Exception as e:
    print("❌ Database connection failed:", e)
