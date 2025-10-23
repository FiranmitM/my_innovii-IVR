INNOVII IVR System - Quick Start Guide
🚀 Fast Track Installation (5 Minutes)
Step 1: Download and Extract Files
# Navigate to the directory containing all files

cd asterisk-ivr-system
Step 2: Run Automated Setup
# Make setup script executable

chmod +x setup.sh


# Run setup (installs everything)

sudo bash setup.sh
Step 3: Create Test Audio Files
# Generate English test audio files

chmod +x create_sample_audio.sh

sudo bash create_sample_audio.sh
Step 4: Test the System
# Run test script

chmod +x test_system.sh

sudo bash test_system.sh
Step 5: Make Your First Call
Install SIP Client (Linphone or Zoiper on your phone/computer)

Configure SIP Account:

Username: 1001
Password: pass1001
Server: YOUR_SERVER_IP (e.g., 192.168.1.100)
Port: 5060
Dial Extension: 5000

Test the IVR:

Listen to welcome message
Subscribe if needed (press 1)
Choose language (1=Amharic, 2=Oromo)
Navigate menus (1=M-Beauty, 2=M-Health, 3=Unsubscribe)
📁 File Structure
asterisk-ivr-system/
├── README.md                          # Main documentation
├── QUICK_START.md                     # This file
├── AUDIO_FILES_GUIDE.md               # Audio file requirements
├── TROUBLESHOOTING.md                 # Problem solving guide
├── DEPLOYMENT_CHECKLIST.md            # Production deployment checklist
│
├── setup.sh                           # Automated installation script
├── test_system.sh                     # System testing script
├── create_sample_audio.sh             # Create test audio files
│
├── innovii_schema.sql                 # Database schema
├── extensions.conf                    # Asterisk dialplan
├── pjsip.conf                         # SIP user configuration
│
└── agi-scripts/
    ├── check_subscription.py          # Check user subscription
    ├── subscribe_user.py              # Subscribe new user
    ├── unsubscribe_user.py            # Unsubscribe user
    ├── update_language.py             # Update language preference
    ├── get_lesson_progress.py         # Get current lesson
    ├── update_lesson_progress.py      # Update lesson progress
    ├── save_question.py               # Save user question
    ├── log_call.py                    # Log call activity
    └── end_call.py                    # Log call end
📍 File Deployment Locations
After running setup.sh, files will be located at:

File Type	Deployed Location
Database Schema	/etc/asterisk/innovii_schema.sql
Extensions Config	/etc/asterisk/extensions.conf
PJSIP Config	/etc/asterisk/pjsip.conf
AGI Scripts	/var/lib/asterisk/agi-bin/*.py
Amharic Audio	/var/lib/asterisk/sounds/custom/amharic/*.wav
Oromo Audio	/var/lib/asterisk/sounds/custom/oromo/*.wav
Asterisk Logs	/var/log/asterisk/full
🎯 IVR Flow Diagram
                    ┌─────────────────────┐
                    │   User Dials 5000   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Check Subscription │
                    │    (Database)       │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
         ┌──────▼────────┐           ┌───────▼────────┐
         │  Not Subscribed│           │   Subscribed   │
         │  Play Welcome  │           │                │
         │  Offer Signup  │           │                │
         └──────┬─────────┘           └───────┬────────┘
                │                             │
         ┌──────▼──────┐                      │
         │  Press 1 to │                      │
         │  Subscribe  │                      │
         └──────┬──────┘                      │
                │                             │
                └──────────────┬──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Choose Language    │
                    │  1=Amharic 2=Oromo  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Main Menu        │
                    │  1=Beauty 2=Health  │
                    │  3=Unsubscribe      │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
  ┌─────▼──────┐      ┌────────▼────────┐    ┌───────▼────────┐
  │  M-Beauty  │      │    M-Health     │    │  Unsubscribe   │
  │  (Press 1) │      │   (Press 2)     │    │   (Press 3)    │
  └─────┬──────┘      └────────┬────────┘    └───────┬────────┘
        │                      │                      │
  ┌─────▼──────┐      ┌────────▼────────┐    ┌───────▼────────┐
  │1=Lessons   │      │1=Mother Health  │    │  Confirm and   │
  │2=Questions │      │2=Child Health   │    │   Goodbye      │
  │3=Back      │      │3=Back           │    └────────────────┘
  └────────────┘      └─────────────────┘
        │                      │
  ┌─────▼──────┐      ┌────────▼────────┐
  │10 Beauty   │      │10 Mother/Child  │
  │Lessons     │      │Health Lessons   │
  │*=Back #=Next│     │*=Back #=Next    │
  └────────────┘      └─────────────────┘
🔑 Default Credentials
Database
Database Name: innovii
Username: innovii
Password: innovii@1234
Host: localhost
SIP Users (1001-1010)
User 1001: Username: 1001, Password: pass1001
User 1002: Username: 1002, Password: pass1002
User 1003: Username: 1003, Password: pass1003
User 1004: Username: 1004, Password: pass1004
User 1005: Username: 1005, Password: pass1005
...(1006-1010 follow same pattern)
⚠️ IMPORTANT: Change these passwords in production!

🎵 Audio Files Required
For Each Language (Amharic & Oromo):
Subscription Messages (4 files)

welcome.wav, not_subscribed.wav, subscribe_prompt.wav, subscribed_success.wav
Navigation (3 files)

choose_language.wav, main_menu.wav, invalid_option.wav, goodbye.wav
M-Beauty Service (12 files)

beauty.wav, beauty_menu.wav, beauty_lesson1-10.wav
M-Health Service (23 files)

health.wav, health_menu.wav
mother_health.wav, mother_health_lesson1-10.wav
child_health.wav, child_health_lesson1-10.wav
Other (2 files)

questions_prompt.wav, unsubscribe_confirm.wav
Total: ~40 files per language = 80 files

Audio Format Requirements
Format: WAV (PCM)
Sample Rate: 8000 Hz
Bit Depth: 16-bit
Channels: Mono (1 channel)
Convert with: sox input.mp3 -r 8000 -c 1 -b 16 output.wav

🛠️ Essential Commands
Asterisk Management
# Access Asterisk CLI

sudo asterisk -rvvv


# Restart Asterisk

sudo systemctl restart asterisk


# Reload dialplan (after editing extensions.conf)

sudo asterisk -rx "dialplan reload"


# Reload PJSIP (after editing pjsip.conf)

sudo asterisk -rx "pjsip reload"


# Show registered endpoints

sudo asterisk -rx "pjsip show endpoints"


# Show active calls

sudo asterisk -rx "core show channels"
Database Management
# Login to MySQL

mysql -u innovii -p'innovii@1234' innovii


# View subscribers

mysql -u innovii -p'innovii@1234' innovii -e "SELECT * FROM subscribers;"


# View recent calls

mysql -u innovii -p'innovii@1234' innovii -e "SELECT * FROM call_logs ORDER BY call_start DESC LIMIT 10;"


# Add subscriber manually

mysql -u innovii -p'innovii@1234' innovii -e "INSERT INTO subscribers (phone_number, subscribed) VALUES ('1001', 1);"
Log Monitoring
# Watch Asterisk logs live

sudo tail -f /var/log/asterisk/full


# Watch for errors

sudo tail -f /var/log/asterisk/full | grep ERROR


# Watch MySQL logs

sudo tail -f /var/log/mysql/error.log
System Status
# Check all services

sudo systemctl status asterisk

sudo systemctl status mysql


# Check ports

sudo netstat -tuln | grep 5060


# Check disk space

df -h


# Check system resources

htop
🔍 Quick Troubleshooting
Problem: Can't Register SIP Client
# Check Asterisk is listening

sudo netstat -tuln | grep 5060


# Check endpoint configuration

sudo asterisk -rx "pjsip show endpoint 1001"


# Restart Asterisk

sudo systemctl restart asterisk
Problem: No Audio During Call
# Check audio files exist

ls -lh /var/lib/asterisk/sounds/custom/amharic/


# Check file format

file /var/lib/asterisk/sounds/custom/amharic/welcome.wav


# Test playback

sudo asterisk -rx "originate Local/1001@innovii-ivr application Playback custom/amharic/welcome"
Problem: Database Connection Failed
# Check MySQL running

sudo systemctl status mysql


# Test connection

mysql -u innovii -p'innovii@1234' innovii -e "SELECT 1;"


# Check AGI script

sudo -u asterisk python3 /var/lib/asterisk/agi-bin/check_subscription.py 1001
📊 Monitoring and Analytics
View System Statistics
-- Total subscribers

SELECT COUNT(*) as total_subscribers FROM subscribers WHERE subscribed = 1;


-- Calls today

SELECT COUNT(*) as calls_today FROM call_logs WHERE DATE(call_start) = CURDATE();


-- Most popular service

SELECT service_accessed, COUNT(*) as count

FROM call_logs

GROUP BY service_accessed

ORDER BY count DESC;


-- Language preference distribution

SELECT preferred_language, COUNT(*) as count

FROM subscribers

GROUP BY preferred_language;


-- Average call duration

SELECT AVG(call_duration) as avg_duration_seconds FROM call_logs;
📝 Next Steps
For Testing
✅ Run sudo bash setup.sh
✅ Run sudo bash test_system.sh
✅ Run sudo bash create_sample_audio.sh
✅ Register SIP client and call 5000
✅ Test all menu options
For Production
📋 Review DEPLOYMENT_CHECKLIST.md
🎤 Record professional Amharic and Oromo audio
🔐 Change all default passwords
🔒 Configure firewall and security
📊 Setup monitoring and backups
🚀 Deploy and monitor
🆘 Getting Help
Check Documentation:

README.md - Complete system documentation
TROUBLESHOOTING.md - Common issues and solutions
AUDIO_FILES_GUIDE.md - Audio file help
DEPLOYMENT_CHECKLIST.md - Production deployment
Check Logs:

Asterisk: /var/log/asterisk/full
MySQL: /var/log/mysql/error.log
Run Tests:

sudo bash test_system.sh
Asterisk Resources:

Official docs: https://www.asterisk.org
Wiki: https://wiki.asterisk.org
📧 Support Information
For technical support with this INNOVII IVR System:

Review all documentation in this directory
Check troubleshooting guide
Review Asterisk logs for specific errors
Test components individually using test scripts
Quick Reference Card:

IVR Number: 5000
Database: innovii / innovii@1234
SIP Users: 1001-1010 / pass1001-pass1010
Audio Location: /var/lib/asterisk/sounds/custom/
Logs: /var/log/asterisk/full
Good luck with your INNOVII IVR deployment! 🎉
Firanmit Megersa Feyisa
Email: megersafiranmit@gmail.com
telegram: @lovecisco

