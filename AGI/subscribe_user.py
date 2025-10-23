#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/subscribe_user.py
# Purpose: Subscribe a new user to INNOVII service

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

def subscribe_user(caller_number):
    """Subscribe a new user to the service"""
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

        # Insert or update subscriber
        query = """
            INSERT INTO subscribers (phone_number, subscribed, preferred_language, subscription_date, total_calls)
            VALUES (%s, 1, 'amharic', %s, 1)
            ON DUPLICATE KEY UPDATE
                subscribed = 1,
                subscription_date = %s,
                total_calls = total_calls + 1
        """
        now = datetime.now()
        cursor.execute(query, (caller_number, now, now))
        conn.commit()

        # Initialize lesson progress for new subscriber
        progress_query = """
            INSERT IGNORE INTO lesson_progress (phone_number, service_type, current_lesson)
            VALUES
                (%s, 'beauty', 1),
                (%s, 'mother_health', 1),
                (%s, 'child_health', 1)
        """
        cursor.execute(progress_query, (caller_number, caller_number, caller_number))
        conn.commit()

        agi.verbose(f"User {caller_number} subscribed successfully")
        agi.set_variable('SUB_RESULT', 'success')

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")
        agi.set_variable('SUB_RESULT', 'failed')

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        caller_number = sys.argv[1]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')

    sys.exit(subscribe_user(caller_number))
