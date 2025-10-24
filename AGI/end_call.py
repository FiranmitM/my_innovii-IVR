#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/end_call.py
# Purpose: Log call end time and calculate duration

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

def end_call(caller_number):
    """Update call log with end time and duration"""
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

        # Get the most recent call log
        query = """
            SELECT id, call_start FROM call_logs
            WHERE phone_number = %s
            ORDER BY call_start DESC
            LIMIT 1
        """
        cursor.execute(query, (caller_number,))
        result = cursor.fetchone()

        if result:
            call_id = result['id']
            call_start = result['call_start']
            call_end = datetime.now()
            duration = int((call_end - call_start).total_seconds())

            # Update call duration
            update_query = """
                UPDATE call_logs
                SET call_duration = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (duration, call_id))
            conn.commit()

            agi.verbose(f"Call ended. Duration: {duration} seconds")
        else:
            agi.verbose(f"No call log found for {caller_number}")

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        caller_number = sys.argv[1]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')

    sys.exit(end_call(caller_number))

# ========================================================
# INNOVII Asterisk IVR System
# Copyright (c) 2025 Firanmit Megersa Feyisa
# Email: megersafiranmit@gmail.com
# All rights reserved.
# Owner: Firanmit Megersa Feyisa
# ========================================================
