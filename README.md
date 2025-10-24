INNOVII Asterisk IVR System - Complete Installation Guide
System Overview
This is a complete Asterisk IVR system with MySQL database integration for INNOVII company.

Short number: 5000
Languages: Amharic (default), Oromo
Services: M-Beauty, M-Health, Subscription Management
Prerequisites
Linux server (Ubuntu/Debian recommended)
Root or sudo access
Internet connection for package installation
Installation Steps
1. Install Required Packages
sudo apt update

sudo apt install -y asterisk asterisk-core-sounds-en asterisk-mysql mysql-server python3 python3-pip

sudo pip3 install mysql-connector-python
2. Setup MySQL Database
# Login to MySQL as root

sudo mysql -u root -p


# Run the following SQL commands:

CREATE DATABASE innovii CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'innovii'@'localhost' IDENTIFIED BY 'innovii@1234';

GRANT ALL PRIVILEGES ON innovii.* TO 'innovii'@'localhost';

FLUSH PRIVILEGES;

EXIT;


# Import the database schema

sudo mysql -u innovii -p'innovii@1234' innovii < /etc/asterisk/innovii_schema.sql
3. Copy Configuration Files
Database Schema
sudo cp innovii_schema.sql /etc/asterisk/

sudo chmod 644 /etc/asterisk/innovii_schema.sql
Asterisk Configuration Files
# Backup original files

sudo cp /etc/asterisk/extensions.conf /etc/asterisk/extensions.conf.backup

sudo cp /etc/asterisk/pjsip.conf /etc/asterisk/pjsip.conf.backup


# Copy new configuration files

sudo cp extensions.conf /etc/asterisk/

sudo cp pjsip.conf /etc/asterisk/

sudo chmod 644 /etc/asterisk/extensions.conf

sudo chmod 644 /etc/asterisk/pjsip.conf
AGI Python Scripts
# Create AGI scripts directory if it doesn't exist

sudo mkdir -p /var/lib/asterisk/agi-bin


# Copy AGI scripts

sudo cp agi-scripts/*.py /var/lib/asterisk/agi-bin/

sudo chmod +x /var/lib/asterisk/agi-bin/*.py

sudo chown asterisk:asterisk /var/lib/asterisk/agi-bin/*.py
Audio Files
# Create custom sounds directory

sudo mkdir -p /var/lib/asterisk/sounds/custom

sudo mkdir -p /var/lib/asterisk/sounds/custom/amharic

sudo mkdir -p /var/lib/asterisk/sounds/custom/oromo


# Copy your audio files to the appropriate directories

# For Amharic sounds:

sudo cp your_sounds/amharic/*.wav /var/lib/asterisk/sounds/custom/amharic/

# For Oromo sounds:

sudo cp your_sounds/oromo/*.wav /var/lib/asterisk/sounds/custom/oromo/


sudo chown -R asterisk:asterisk /var/lib/asterisk/sounds/custom

sudo chmod -R 644 /var/lib/asterisk/sounds/custom/*.wav
4. Audio Files Structure
Place your audio files in the following structure:

/var/lib/asterisk/sounds/custom/
├── amharic/
│   ├── welcome.wav
│   ├── not_subscribed.wav
│   ├── subscribe_prompt.wav
│   ├── subscribed_success.wav
│   ├── choose_language.wav
│   ├── main_menu.wav
│   ├── beauty.wav
│   ├── health.wav
│   ├── beauty_menu.wav
│   ├── health_menu.wav
│   ├── mother_health.wav
│   ├── child_health.wav
│   ├── lesson1.wav through lesson10.wav
│   ├── questions_prompt.wav
│   ├── unsubscribe_confirm.wav
│   ├── goodbye.wav
│   └── invalid_option.wav
└── oromo/
    └── (same files as amharic but in Oromo language)
5. Configure SIP Clients (Linphone/Zoiper)
Register the following accounts:

Username: 1001, Password: pass1001, Server: YOUR_SERVER_IP
Username: 1002, Password: pass1002, Server: YOUR_SERVER_IP
Username: 1003, Password: pass1003, Server: YOUR_SERVER_IP
Username: 1004, Password: pass1004, Server: YOUR_SERVER_IP
Username: 1005, Password: pass1005, Server: YOUR_SERVER_IP
6. Start/Restart Asterisk
sudo systemctl restart asterisk

sudo systemctl enable asterisk

sudo systemctl status asterisk
7. Testing
# Check Asterisk CLI

sudo asterisk -rvvv


# In Asterisk CLI, check:

pjsip show endpoints

dialplan show innovii-ivr

agi show commands

database show


# Test call: Dial 5000 from any registered phone
IVR Flow
User dials 5000
System checks subscription in database
If not subscribed:
Plays welcome and service description
Offers subscription (press 1)
Stores phone number in database
Language selection: 1=Amharic, 2=Oromo
Main Menu:
1 = M-Beauty
2 = M-Health
3 = Unsubscribe
M-Beauty Menu:
1 = Listen to lessons (use * for previous, # for next)
2 = Ask questions
3 = Back to main menu
M-Health Menu:
1 = Mother health advice (use * for previous, # for next)
2 = Child health advice (use * for previous, # for next)
3 = Back to main menu
Troubleshooting
Check Asterisk logs
sudo tail -f /var/log/asterisk/full

sudo tail -f /var/log/asterisk/messages
Test database connection
mysql -u innovii -p'innovii@1234' innovii -e "SELECT * FROM subscribers;"
Test AGI scripts
sudo -u asterisk python3 /var/lib/asterisk/agi-bin/check_subscription.py
Common issues
No audio: Check file paths and permissions
Database connection failed: Verify MySQL credentials
SIP registration failed: Check pjsip.conf and network settings
AGI script errors: Check Python script permissions and syntax
File Locations Summary
Database schema: /etc/asterisk/innovii_schema.sql
Extensions config: /etc/asterisk/extensions.conf
PJSIP config: /etc/asterisk/pjsip.conf
AGI scripts: /var/lib/asterisk/agi-bin/*.py
Audio files: /var/lib/asterisk/sounds/custom/
Logs: /var/log/asterisk/
Support
For issues, check the Asterisk documentation at https://www.asterisk.org

# Ownership & Copyright

**Owner:** Firanmit Megersa Feyisa  
**Email:** megersafiranmit@gmail.com  
**Role:** IT Technician, INNOVII Company  
**Project:** INNOVII Asterisk IVR System – Complete Installation  
**Version:** 1.0  
**Date:** October 2025  

---

## Copyright Notice

© 2025 Firanmit Megersa Feyisa. All rights reserved.  

This Asterisk IVR system, including all configuration files, AGI Python scripts, automation scripts, documentation, and audio files, is the **intellectual property of Firanmit Megersa Feyisa**.  

You may **not** copy, redistribute, modify, or use this project without the explicit permission of the owner.  

---

## Integration in Files

It is recommended to add the following header to all scripts, config files, and documentation:

```text
# ========================================================
# INNOVII Asterisk IVR System
# Copyright (c) 2025 Firanmit Megersa Feyisa
# Email: megersafiranmit@gmail.com
# All rights reserved.
# Owner: Firanmit Megersa Feyisa
# ========================================================
