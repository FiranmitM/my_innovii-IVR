#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/update_language.py
# Purpose: Update user's preferred language

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

def update_language(caller_number, language):
    """Update user's preferred language"""
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

        # Update language preference
        query = """
            UPDATE subscribers
            SET preferred_language = %s
            WHERE phone_number = %s
        """
        cursor.execute(query, (language, caller_number))
        conn.commit()

        agi.verbose(f"User {caller_number} language updated to {language}")

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 2:
        caller_number = sys.argv[1]
        language = sys.argv[2]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')
        language = 'amharic'

    sys.exit(update_language(caller_number, language))
