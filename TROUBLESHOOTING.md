Troubleshooting Guide - INNOVII IVR System
Quick Diagnostic Commands
Check Asterisk Status
# Check if Asterisk is running

sudo systemctl status asterisk


# View Asterisk logs in real-time

sudo tail -f /var/log/asterisk/full


# Access Asterisk CLI

sudo asterisk -rvvv


# Restart Asterisk

sudo systemctl restart asterisk
Check MySQL Database
# Login to MySQL

mysql -u innovii -p'innovii@1234' innovii


# Check tables

mysql -u innovii -p'innovii@1234' innovii -e "SHOW TABLES;"


# View subscribers

mysql -u innovii -p'innovii@1234' innovii -e "SELECT * FROM subscribers;"


# View call logs

mysql -u innovii -p'innovii@1234' innovii -e "SELECT * FROM call_logs ORDER BY call_start DESC LIMIT 10;"
Check Network
# Check if Asterisk is listening on SIP port

sudo netstat -tuln | grep 5060


# Check firewall

sudo ufw status
Common Issues and Solutions
Issue 1: Cannot Register SIP Client
Symptoms:

Linphone/Zoiper shows "Registration Failed"
Error: "Forbidden" or "Unauthorized"
Solutions:

Check pjsip.conf is properly loaded:

sudo asterisk -rx "pjsip show endpoints"
Verify user credentials in pjsip.conf:

grep -A5 "1001" /etc/asterisk/pjsip.conf
Check Asterisk is listening:

sudo netstat -tuln | grep 5060
Restart Asterisk:

sudo systemctl restart asterisk
Check firewall allows port 5060:

sudo ufw allow 5060/udp

sudo ufw allow 5060/tcp

sudo ufw allow 10000:20000/udp  # RTP ports
Issue 2: No Audio During Call
Symptoms:

Call connects but no audio plays
Silence when prompts should play
Solutions:

Verify audio files exist:

ls -lh /var/lib/asterisk/sounds/custom/amharic/
Check audio file format:

file /var/lib/asterisk/sounds/custom/amharic/welcome.wav

# Should show: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz
Check file permissions:

sudo chown -R asterisk:asterisk /var/lib/asterisk/sounds/custom

sudo chmod -R 644 /var/lib/asterisk/sounds/custom/*.wav
Test audio playback in Asterisk CLI:

sudo asterisk -rvvv

CLI> originate Local/1001@innovii-ivr application Playback custom/amharic/welcome
Convert audio to correct format:

sox input.wav -r 8000 -c 1 -b 16 output.wav
Issue 3: Database Connection Failed
Symptoms:

AGI scripts fail
Error in logs: "Database connection failed"
Solutions:

Check MySQL is running:

sudo systemctl status mysql

sudo systemctl start mysql
Test database connection:

mysql -u innovii -p'innovii@1234' innovii -e "SELECT 1;"
Verify database exists:

mysql -u root -p -e "SHOW DATABASES;" | grep innovii
Recreate user if needed:

sudo mysql -u root -p

DROP USER 'innovii'@'localhost';

CREATE USER 'innovii'@'localhost' IDENTIFIED BY 'innovii@1234';

GRANT ALL PRIVILEGES ON innovii.* TO 'innovii'@'localhost';

FLUSH PRIVILEGES;

EXIT;
Check Python MySQL connector:

python3 -c "import mysql.connector; print('OK')"

# If error, install: pip3 install mysql-connector-python
Issue 4: AGI Script Errors
Symptoms:

Errors in Asterisk logs about AGI scripts
Scripts not executing
Solutions:

Check script permissions:

ls -lh /var/lib/asterisk/agi-bin/

# All .py files should be executable (rwxr-xr-x)
Make scripts executable:

sudo chmod +x /var/lib/asterisk/agi-bin/*.py
Check script ownership:

sudo chown asterisk:asterisk /var/lib/asterisk/agi-bin/*.py
Test script manually:

sudo -u asterisk python3 /var/lib/asterisk/agi-bin/check_subscription.py 1001
Check Python path in scripts:

which python3

# Make sure first line of scripts matches: #!/usr/bin/env python3
Issue 5: Extension 5000 Not Found
Symptoms:

Error: "Extension not found"
Cannot dial 5000
Solutions:

Check extensions.conf is loaded:

sudo asterisk -rx "dialplan reload"

sudo asterisk -rx "dialplan show innovii-ivr"
Verify extensions.conf syntax:

sudo asterisk -rx "dialplan show 5000@innovii-ivr"
Check for syntax errors:

sudo asterisk -rx "core reload"
Review Asterisk startup errors:

sudo grep ERROR /var/log/asterisk/messages
Issue 6: DTMF Not Working
Symptoms:

Cannot select menu options
Key presses not detected
Solutions:

Check DTMF mode in pjsip.conf:

grep dtmf_mode /etc/asterisk/pjsip.conf

# Should show: dtmf_mode=rfc4733
In SIP client, ensure DTMF is set to RFC2833/RTP

Add debug logging in extensions.conf:

same => n,NoOp(DTMF pressed: ${EXTEN})
Test DTMF in Asterisk CLI:

CLI> core set verbose 10

# Then make a call and press keys
Issue 7: Language Not Switching
Symptoms:

Language selection doesn't work
Always plays same language
Solutions:

Check both language directories exist:

ls -ld /var/lib/asterisk/sounds/custom/amharic

ls -ld /var/lib/asterisk/sounds/custom/oromo
Verify audio files in both directories:

diff /var/lib/asterisk/sounds/custom/amharic/ /var/lib/asterisk/sounds/custom/oromo/
Check variable setting in dialplan:

grep SOUND_DIR /etc/asterisk/extensions.conf
Add debug logging:

same => n,NoOp(Current language: ${USER_LANG})
same => n,NoOp(Sound directory: ${SOUND_DIR})
Issue 8: Subscription Check Not Working
Symptoms:

Always asks to subscribe
Database not checked
Solutions:

Check AGI script is being called:

sudo tail -f /var/log/asterisk/full | grep check_subscription
Manually test subscription check:

mysql -u innovii -p'innovii@1234' innovii -e "SELECT * FROM subscribers WHERE phone_number='1001';"
Add subscriber manually:

mysql -u innovii -p'innovii@1234' innovii -e "INSERT INTO subscribers (phone_number, subscribed) VALUES ('1001', 1);"
Check AGI script output:

sudo -u asterisk python3 /var/lib/asterisk/agi-bin/check_subscription.py 1001
Issue 9: Lessons Navigation Not Working
Symptoms:

Cannot use * or # to navigate lessons
Keys don't respond during playback
Solutions:

Verify ControlPlayback is supported:

sudo asterisk -rx "core show application ControlPlayback"
Check lesson files exist:

ls -lh /var/lib/asterisk/sounds/custom/amharic/beauty_lesson*.wav
Test lesson variable:

same => n,NoOp(Current lesson: ${LESSON_NUM})
Use simpler navigation if ControlPlayback doesn't work:

Replace ControlPlayback with Background and separate WaitExten
Performance Issues
High CPU Usage
# Check Asterisk processes

top -u asterisk


# Reduce logging verbosity

sudo asterisk -rx "core set verbose 0"

sudo asterisk -rx "core set debug 0"


# Check for loops in dialplan

sudo tail -f /var/log/asterisk/full
Database Slow
# Optimize tables

mysql -u innovii -p'innovii@1234' innovii -e "OPTIMIZE TABLE subscribers, lesson_progress, call_logs, questions;"


# Add indexes if missing

mysql -u innovii -p'innovii@1234' innovii -e "SHOW INDEX FROM subscribers;"


# Check slow query log

sudo tail -f /var/log/mysql/slow.log
Debugging Tips
Enable Verbose Logging
# In Asterisk CLI

CLI> core set verbose 5

CLI> core set debug 5

CLI> pjsip set logger on
Monitor Live Calls
# In Asterisk CLI

CLI> core show channels

CLI> core show channel <channel_name>
Test Database Queries
# Monitor database queries

sudo tail -f /var/log/mysql/mysql.log
Check System Resources
# Memory usage

free -h


# Disk space

df -h


# CPU usage

top


# Network connections

netstat -an | grep 5060
Getting Help
Collect Diagnostic Information
# Create a diagnostic report

echo "=== Asterisk Version ===" > diagnostic.txt

asterisk -V >> diagnostic.txt

echo "=== Asterisk Status ===" >> diagnostic.txt

systemctl status asterisk >> diagnostic.txt

echo "=== PJSIP Endpoints ===" >> diagnostic.txt

asterisk -rx "pjsip show endpoints" >> diagnostic.txt

echo "=== Database Tables ===" >> diagnostic.txt

mysql -u innovii -p'innovii@1234' innovii -e "SHOW TABLES;" >> diagnostic.txt

echo "=== Recent Errors ===" >> diagnostic.txt

grep ERROR /var/log/asterisk/messages | tail -20 >> diagnostic.txt
Useful Asterisk CLI Commands
# Show all contexts

dialplan show


# Show specific context

dialplan show innovii-ivr


# Reload dialplan

dialplan reload


# Show PJSIP endpoints

pjsip show endpoints


# Show specific endpoint

pjsip show endpoint 1001


# Reload PJSIP

pjsip reload


# Show channels

core show channels


# Hangup a channel

channel request hangup <channel>


# Show active calls

core show calls
Contact and Support
If issues persist after trying these solutions:

Check Asterisk documentation: https://www.asterisk.org
Review /var/log/asterisk/full for detailed error messages
Run the test script: sudo bash test_system.sh
Ensure all components are up to date
Remember to always backup your configuration before making changes:

sudo cp /etc/asterisk/extensions.conf /etc/asterisk/extensions.conf.backup

sudo cp /etc/asterisk/pjsip.conf /etc/asterisk/pjsip.conf.backup
