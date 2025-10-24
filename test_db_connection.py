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


# INNOVII IVR System – Copyright & Ownership

**Owner:** Firanmit Megersa Feyisa  
**Email:** megersafiranmit@gmail.com  

**Project:** INNOVII IVR System – Complete Asterisk IVR with MySQL Integration  
**Version:** 1.0  
**Date:** October 2025  

---

## Copyright Notice

© 2025 Firanmit Megersa Feyisa. All rights reserved.  

This project, including all configuration files, AGI scripts, automation scripts, documentation, and audio files, is the intellectual property of Firanmit Megersa Feyisa.  

You may **not** copy, distribute, or modify this project without explicit permission from the owner.  

---

## Attribution in Code and Config Files

It is recommended to add the following header to all major files:

```text
# ========================================================
# INNOVII IVR System
# Copyright (c) 2025 Firanmit Megersa Feyisa
# Email: megersafiranmit@gmail.com
# All rights reserved.
# ========================================================
