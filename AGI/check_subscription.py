#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/check_subscription.py
# Purpose: Check if caller is subscribed to INNOVII service

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

def check_subscription(caller_number):
    """Check if the caller is subscribed"""
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

        # Check subscription
        query = """
            SELECT subscribed, preferred_language, total_calls
            FROM subscribers
            WHERE phone_number = %s
        """
        cursor.execute(query, (caller_number,))
        result = cursor.fetchone()

        if result and result['subscribed'] == 1:
            # User is subscribed
            agi.set_variable('SUB_STATUS', 'subscribed')
            agi.set_variable('PREF_LANG', result['preferred_language'])
            agi.verbose(f"User {caller_number} is subscribed")

            # Update last call date and total calls
            update_query = """
                UPDATE subscribers
                SET last_call_date = %s, total_calls = total_calls + 1
                WHERE phone_number = %s
            """
            cursor.execute(update_query, (datetime.now(), caller_number))
            conn.commit()
        else:
            # User not subscribed or doesn't exist
            agi.set_variable('SUB_STATUS', 'not_subscribed')
            agi.set_variable('PREF_LANG', 'amharic')
            agi.verbose(f"User {caller_number} is not subscribed")

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")
        agi.set_variable('SUB_STATUS', 'not_subscribed')
        agi.set_variable('PREF_LANG', 'amharic')

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        caller_number = sys.argv[1]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')

    sys.exit(check_subscription(caller_number))
    # ========================================================
# INNOVII Asterisk IVR System
# Copyright (c) 2025 Firanmit Megersa Feyisa
# Email: megersafiranmit@gmail.com
# All rights reserved.
# Owner: Firanmit Megersa Feyisa
# ========================================================
