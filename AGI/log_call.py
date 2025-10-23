#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/log_call.py
# Purpose: Log call menu navigation and activities

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

def log_call(caller_number, menu_location, language):
    """Log the call activity"""
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

        # Check if there's an active call log for this number
        check_query = """
            SELECT id, menu_path FROM call_logs
            WHERE phone_number = %s
            AND call_start >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
            ORDER BY call_start DESC
            LIMIT 1
        """
        cursor.execute(check_query, (caller_number,))
        result = cursor.fetchone()

        if result:
            # Update existing call log
            call_id = result[0]
            menu_path = result[1] if result[1] else ''
            new_menu_path = f"{menu_path} > {menu_location}" if menu_path else menu_location

            update_query = """
                UPDATE call_logs
                SET menu_path = %s, language_used = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (new_menu_path, language, call_id))
        else:
            # Create new call log
            insert_query = """
                INSERT INTO call_logs (phone_number, call_start, service_accessed, language_used, menu_path)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (caller_number, datetime.now(), menu_location, language, menu_location))
            call_id = cursor.lastrowid

        conn.commit()
        agi.set_variable('CALL_LOG_ID', str(call_id))
        agi.verbose(f"Call activity logged: {menu_location}")

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 3:
        caller_number = sys.argv[1]
        menu_location = sys.argv[2]
        language = sys.argv[3]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')
        menu_location = 'unknown'
        language = 'amharic'

    sys.exit(log_call(caller_number, menu_location, language))
