#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/get_lesson_progress.py
# Purpose: Get user's current lesson number for a service

import sys
import mysql.connector

class AGI:
    def __init__(self):
        self.env = {}
        self._get_agi_env()

    def _get_agi_env(self):
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            key, value = line.split(':', 1)
            self.env[key.strip()] = value.strip()

    def get_variable(self, name):
        sys.stdout.write(f'GET VARIABLE {name}\n')
        sys.stdout.flush()
        result = sys.stdin.readline().strip()
        return result

    def set_variable(self, name, value):
        sys.stdout.write(f'SET VARIABLE {name} "{value}"\n')
        sys.stdout.flush()
        sys.stdin.readline()

    def verbose(self, message, level=1):
        sys.stdout.write(f'VERBOSE "{message}" {level}\n')
        sys.stdout.flush()
        sys.stdin.readline()

def get_lesson_progress(caller_number, service_type):
    """Get current lesson number for the user and service"""
    agi = AGI()

    try:
        # Connect to database
        conn = mysql.connector.connect(
            host='localhost',
            user='innovii',
            password='Innovii@123',
            database='innovii'
        )
        cursor = conn.cursor(dictionary=True)

        # Get current lesson
        query = """
            SELECT current_lesson
            FROM lesson_progress
            WHERE phone_number = %s AND service_type = %s
        """
        cursor.execute(query, (caller_number, service_type))
        result = cursor.fetchone()

        if result:
            current_lesson = result['current_lesson']
        else:
            # Create new progress entry
            insert_query = """
                INSERT INTO lesson_progress (phone_number, service_type, current_lesson)
                VALUES (%s, %s, 1)
            """
            cursor.execute(insert_query, (caller_number, service_type))
            conn.commit()
            current_lesson = 1

        agi.set_variable('CURRENT_LESSON', str(current_lesson))
        agi.verbose(f"User {caller_number} - {service_type}: Lesson {current_lesson}")

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")
        agi.set_variable('CURRENT_LESSON', '1')

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 2:
        caller_number = sys.argv[1]
        service_type = sys.argv[2]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')
        service_type = 'beauty'

    sys.exit(get_lesson_progress(caller_number, service_type))

# ========================================================
# INNOVII Asterisk IVR System
# Copyright (c) 2025 Firanmit Megersa Feyisa
# Email: megersafiranmit@gmail.com
# All rights reserved.
# Owner: Firanmit Megersa Feyisa
# ========================================================
