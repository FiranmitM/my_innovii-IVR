#!/usr/bin/env python3
# File Location: /var/lib/asterisk/agi-bin/save_question.py
# Purpose: Save user's recorded question to database

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

def save_question(caller_number, service_type, audio_file):
    """Save user's question to database"""
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

        # Insert question
        query = """
            INSERT INTO questions (phone_number, service_type, question_audio_file, asked_date, answered)
            VALUES (%s, %s, %s, %s, 0)
        """
        cursor.execute(query, (caller_number, service_type, audio_file, datetime.now()))
        conn.commit()

        question_id = cursor.lastrowid
        agi.verbose(f"Question saved with ID: {question_id}")
        agi.set_variable('QUESTION_ID', str(question_id))

        cursor.close()
        conn.close()

    except Exception as e:
        agi.verbose(f"Database error: {str(e)}")
        agi.set_variable('QUESTION_ID', '0')

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 3:
        caller_number = sys.argv[1]
        service_type = sys.argv[2]
        audio_file = sys.argv[3]
    else:
        agi = AGI()
        caller_number = agi.env.get('agi_callerid', 'unknown')
        service_type = 'beauty'
        audio_file = '/tmp/question.wav'

    sys.exit(save_question(caller_number, service_type, audio_file))
