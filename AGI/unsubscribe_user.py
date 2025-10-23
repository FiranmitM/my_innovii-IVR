#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/unsubscribe_user.py
# Purpose: Unsubscribe a user from INNOVII service

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

def unsubscribe_user(caller_number):
    """Unsubscribe a user from the service"""
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

        # Update subscription status
        query = """
            UPDATE subscribers
            SET subscribed = 0
            WHERE phone_number = %s
        """
        cursor.execute(query, (caller_number,))
        conn.commit()

        agi.verbose(f"User {caller_number} unsubscribed successfully")
        agi.set_variable('UNSUB_RESULT', 'success')

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")
        agi.set_variable('UNSUB_RESULT', 'failed')

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        caller_number = sys.argv[1]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')

    sys.exit(unsubscribe_user(caller_number))
