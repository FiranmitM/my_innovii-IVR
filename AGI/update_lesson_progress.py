#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/update_lesson_progress.py
# Purpose: Update user's lesson progress

import sys
import mysql.connector
from datetime import datetime

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

def update_lesson_progress(caller_number, service_type, lesson_number):
    """Update user's current lesson number"""
    agi = AGI()

    try:
        # Connect to database
        conn = mysql.connector.connect(
            host='localhost',
            user='innovii',
            password='Innovii@123',
            database='innovii'
        )
        cursor = conn.cursor()

        # Update lesson progress
        query = """
            INSERT INTO lesson_progress (phone_number, service_type, current_lesson, last_accessed)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                current_lesson = %s,
                last_accessed = %s
        """
        now = datetime.now()
        cursor.execute(query, (caller_number, service_type, lesson_number, now, lesson_number, now))
        conn.commit()

        agi.verbose(f"User {caller_number} - {service_type}: Updated to lesson {lesson_number}")

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 3:
        caller_number = sys.argv[1]
        service_type = sys.argv[2]
        lesson_number = sys.argv[3]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')
        service_type = 'beauty'
        lesson_number = '1'

    sys.exit(update_lesson_progress(caller_number, service_type, lesson_number))
