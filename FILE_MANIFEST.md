
INNOVII IVR System - Complete File Manifest
📦 Package Contents
This package contains all files needed to deploy a complete Asterisk IVR system with MySQL integration for INNOVII company.

📄 Documentation Files (Read First)
1. README.md
Location: asterisk-ivr-system/README.md
Purpose: Complete installation and configuration guide
Read: FIRST - Before doing anything
Size: ~15 KB
2. QUICK_START.md ⭐
Location: asterisk-ivr-system/QUICK_START.md
Purpose: Fast-track 5-minute installation guide
Read: SECOND - For quick deployment
Size: ~12 KB
3. AUDIO_FILES_GUIDE.md
Location: asterisk-ivr-system/AUDIO_FILES_GUIDE.md
Purpose: Complete guide for creating/converting audio files
Read: THIRD - Before recording audio
Size: ~8 KB
4. TROUBLESHOOTING.md
Location: asterisk-ivr-system/TROUBLESHOOTING.md
Purpose: Solutions for common problems
Read: When issues occur
Size: ~15 KB
5. DEPLOYMENT_CHECKLIST.md
Location: asterisk-ivr-system/DEPLOYMENT_CHECKLIST.md
Purpose: Production deployment checklist
Read: Before production deployment
Size: ~12 KB
6. FILE_MANIFEST.md
Location: asterisk-ivr-system/FILE_MANIFEST.md
Purpose: This file - Complete file listing
Read: For reference
Size: ~8 KB
🔧 Configuration Files
7. extensions.conf
Current Location: asterisk-ivr-system/extensions.conf
Deploy To: /etc/asterisk/extensions.conf
Purpose: Asterisk dialplan - IVR logic and call flow
Contains:
Extension 5000 entry point
Subscription checking logic
Language selection menus
M-Beauty and M-Health navigation
Lesson playback with */# navigation
Unsubscribe functionality
Lines: ~250
Auto-deployed by: setup.sh
8. pjsip.conf
Current Location: asterisk-ivr-system/pjsip.conf
Deploy To: /etc/asterisk/pjsip.conf
Purpose: SIP endpoint configuration for users
Contains:
Transport settings (UDP/TCP on port 5060)
10 pre-configured users (1001-1010)
Authentication credentials
DTMF settings
Users Configured:
1001 / pass1001
1002 / pass1002
... through 1010 / pass1010
Lines: ~115
Auto-deployed by: setup.sh
9. innovii_schema.sql
Current Location: asterisk-ivr-system/innovii_schema.sql
Deploy To: /etc/asterisk/innovii_schema.sql (reference)
Execute In: MySQL database
Purpose: Database schema creation
Contains:
Table: subscribers - User subscription info
Table: lesson_progress - Lesson tracking
Table: questions - User questions
Table: call_logs - Call analytics
Test data
Lines: ~85
Auto-deployed by: setup.sh
🐍 AGI Python Scripts (9 Scripts)
Location (before): asterisk-ivr-system/agi-scripts/ Deploy To: /var/lib/asterisk/agi-bin/ Permissions: Executable (755), Owner: asterisk:asterisk

10. check_subscription.py
Purpose: Check if caller is subscribed
Called By: Extension 5000 entry point
Database: Queries subscribers table
Returns: SUB_STATUS (subscribed/not_subscribed), PREF_LANG
Lines: ~70
11. subscribe_user.py
Purpose: Subscribe new user to service
Called By: When user presses 1 to subscribe
Database: Inserts/updates subscribers table, initializes lesson_progress
Returns: SUB_RESULT (success/failed)
Lines: ~75
12. unsubscribe_user.py
Purpose: Unsubscribe user from service
Called By: Unsubscribe menu option
Database: Updates subscribers.subscribed = 0
Returns: UNSUB_RESULT (success/failed)
Lines: ~55
13. update_language.py
Purpose: Update user's language preference
Called By: After language selection
Database: Updates subscribers.preferred_language
Parameters: phone_number, language (amharic/oromo)
Lines: ~60
14. get_lesson_progress.py
Purpose: Get user's current lesson number
Called By: Before playing lessons
Database: Queries lesson_progress table
Returns: CURRENT_LESSON (1-10)
Service Types: beauty, mother_health, child_health
Lines: ~70
15. update_lesson_progress.py
Purpose: Update user's lesson progress
Called By: When lesson is played
Database: Updates lesson_progress.current_lesson
Parameters: phone_number, service_type, lesson_number
Lines: ~65
16. save_question.py
Purpose: Save recorded question to database
Called By: After user records question
Database: Inserts into questions table
Returns: QUESTION_ID
Lines: ~65
17. log_call.py
Purpose: Log call navigation and menu path
Called By: At each menu level
Database: Inserts/updates call_logs table
Returns: CALL_LOG_ID
Lines: ~75
18. end_call.py
Purpose: Log call end time and duration
Called By: On call hangup
Database: Updates call_logs.call_duration
Calculates: Call duration in seconds
Lines: ~60
All AGI scripts auto-deployed by: setup.sh

🚀 Automation Scripts (3 Scripts)
19. setup.sh ⭐⭐⭐
Location: asterisk-ivr-system/setup.sh
Purpose: AUTOMATED COMPLETE INSTALLATION
Permissions: Executable (already set)
Run As: sudo bash setup.sh
What It Does:
Installs all required packages (Asterisk, MySQL, Python)
Creates MySQL database and user
Imports database schema
Copies configuration files to correct locations
Installs AGI scripts
Creates audio directories
Restarts Asterisk
Shows next steps
Runtime: ~3-5 minutes (depending on internet speed)
Lines: ~95
20. test_system.sh ⭐⭐
Location: asterisk-ivr-system/test_system.sh
Purpose: COMPREHENSIVE SYSTEM TESTING
Permissions: Executable (already set)
Run As: sudo bash test_system.sh
Tests:
MySQL database connectivity
Asterisk service status
Configuration file presence
AGI script installation
Python dependencies
Audio directories
Dialplan loaded
PJSIP endpoints configured
Database functions
Output: PASSED/FAILED for each component
Runtime: ~30 seconds
Lines: ~200
21. create_sample_audio.sh ⭐
Location: asterisk-ivr-system/create_sample_audio.sh
Purpose: CREATE TEST AUDIO FILES
Permissions: Executable (already set)
Run As: sudo bash create_sample_audio.sh
Creates: ~40 English placeholder audio files
Output Location:
/var/lib/asterisk/sounds/custom/amharic/
/var/lib/asterisk/sounds/custom/oromo/
Method: Text-to-speech (espeak/festival)
Note: THESE ARE FOR TESTING ONLY - Replace with professional recordings
Runtime: ~2-3 minutes
Lines: ~120
📊 Summary Statistics
Total Files in Package: 21
Documentation: 6 files (~70 KB) Configuration: 3 files (~15 KB) AGI Scripts: 9 files (~25 KB) Automation: 3 files (~15 KB)

Total Package Size: ~125 KB (compressed)

🗺️ Deployment Map
YOUR LINUX SERVER
│
├── /etc/asterisk/
│   ├── extensions.conf        ← From: asterisk-ivr-system/extensions.conf
│   ├── pjsip.conf             ← From: asterisk-ivr-system/pjsip.conf
│   └── innovii_schema.sql     ← From: asterisk-ivr-system/innovii_schema.sql
│
├── /var/lib/asterisk/
│   ├── agi-bin/
│   │   ├── check_subscription.py       ← From: agi-scripts/
│   │   ├── subscribe_user.py           ← From: agi-scripts/
│   │   ├── unsubscribe_user.py         ← From: agi-scripts/
│   │   ├── update_language.py          ← From: agi-scripts/
│   │   ├── get_lesson_progress.py      ← From: agi-scripts/
│   │   ├── update_lesson_progress.py   ← From: agi-scripts/
│   │   ├── save_question.py            ← From: agi-scripts/
│   │   ├── log_call.py                 ← From: agi-scripts/
│   │   └── end_call.py                 ← From: agi-scripts/
│   │
│   └── sounds/custom/
│       ├── amharic/
│       │   └── *.wav (40 files)        ← YOU CREATE THESE
│       └── oromo/
│           └── *.wav (40 files)        ← YOU CREATE THESE
│
├── /var/log/asterisk/
│   ├── full                   ← Asterisk logs
│   └── messages               ← Asterisk messages
│
└── MySQL Database: innovii
    ├── subscribers            ← Created by: innovii_schema.sql
    ├── lesson_progress        ← Created by: innovii_schema.sql
    ├── questions              ← Created by: innovii_schema.sql
    └── call_logs              ← Created by: innovii_schema.sql
📋 Installation Order
Follow this exact order for best results:

Read Documentation

 README.md (5 min)
 QUICK_START.md (3 min)
Run Setup

 sudo bash setup.sh (5 min)
Test System

 sudo bash test_system.sh (1 min)
Create Test Audio

 sudo bash create_sample_audio.sh (3 min)
Test Call

 Register SIP client
 Call 5000
 Test all menus
Prepare Production Audio

 Read AUDIO_FILES_GUIDE.md
 Record professional Amharic audio
 Record professional Oromo audio
 Convert to correct format
 Copy to server
Prepare for Production

 Read DEPLOYMENT_CHECKLIST.md
 Change all passwords
 Configure security
 Setup monitoring
Deploy

 Final testing
 Go live!
🔐 Security Checklist
CRITICAL: Before production deployment:

 Change MySQL password for 'innovii' user
 Update password in ALL 9 AGI scripts
 Change SIP passwords for users 1001-1010
 Configure firewall
 Install Fail2ban
 Disable MySQL remote access
 Enable security updates
📞 Technical Specifications
System Requirements
OS: Ubuntu 20.04+ / Debian 11+
RAM: 2GB minimum, 4GB recommended
Disk: 20GB minimum
CPU: 2 cores minimum
Network: Static IP recommended
Software Versions
Asterisk: 18+ (tested with 20.x)
MySQL: 8.0+ (or MariaDB 10.5+)
Python: 3.8+
SoX: Any recent version
Network Ports
5060 UDP/TCP: SIP signaling
10000-20000 UDP: RTP media
3306 TCP: MySQL (localhost only)
Database
Name: innovii
User: innovii
Password: innovii@1234 (CHANGE IN PRODUCTION!)
Tables: 4
Character Set: utf8mb4
IVR
Entry Point: Extension 5000
Languages: 2 (Amharic, Oromo)
Services: 2 (M-Beauty, M-Health)
Lessons: 30 total (10 beauty + 10 mother + 10 child)
Audio Files: ~80 total (40 × 2 languages)
✅ File Verification Checklist
Before deployment, verify you have all files:

Documentation (6 files)
 README.md
 QUICK_START.md
 AUDIO_FILES_GUIDE.md
 TROUBLESHOOTING.md
 DEPLOYMENT_CHECKLIST.md
 FILE_MANIFEST.md
Configuration (3 files)
 extensions.conf
 pjsip.conf
 innovii_schema.sql
AGI Scripts (9 files)
 check_subscription.py
 subscribe_user.py
 unsubscribe_user.py
 update_language.py
 get_lesson_progress.py
 update_lesson_progress.py
 save_question.py
 log_call.py
 end_call.py
Automation (3 files)
 setup.sh
 test_system.sh
 create_sample_audio.sh
Total: 21 files ✓

🎯 Key Features Implemented
✅ Subscription management (subscribe/unsubscribe) ✅ Multi-language support (Amharic/Oromo) ✅ Dual service system (M-Beauty/M-Health) ✅ Lesson navigation with */# keys ✅ Question recording functionality ✅ Comprehensive call logging ✅ Database-driven user management ✅ Real-time subscription checking ✅ Lesson progress tracking ✅ Automated installation ✅ Comprehensive testing ✅ Production-ready configuration

📚 Additional Resources
Online Documentation
Asterisk Official: https://www.asterisk.org
Asterisk Wiki: https://wiki.asterisk.org
MySQL Documentation: https://dev.mysql.com/doc/
Recommended Tools
SIP Clients: Linphone, Zoiper, X-Lite
Audio Editing: Audacity (free)
Audio Conversion: SoX, FFmpeg
Monitoring: Grafana + Prometheus (advanced)
🏆 Success Criteria
Your system is ready when:

✅ All tests in test_system.sh pass ✅ You can register a SIP client ✅ You can dial extension 5000 ✅ You can navigate all menus ✅ Audio plays correctly ✅ Database is being updated ✅ Language switching works ✅ All lessons are accessible

Package Version: 1.0 Created For: INNOVII Company Target Platform: Linux (Ubuntu/Debian) Last Updated: October 2025

Thank you for choosing this IVR system! For best results, follow the documentation carefully. Good luck with your deployment! 🚀


# INNOVII IVR System – Copyright & Ownership

**Owner:** Firanmit Megersa Feyisa  
**Email:** megersafiranmit@gmail.com  

**Project:** INNOVII IVR System – Complete Asterisk IVR with MySQL Integration  
**Version:** 1.0  
**Date:** October 2025  

---

## Copyright Notice

© 2025 Firanmit Megersa Feyisa. All rights reserved.  

This project, including all configuration files, AGI scripts, automation scripts, documentation, and audio files, is the intellectual property of Firanmit Megersa Feyisa.  

You may **not** copy, distribute, or modify this project without explicit permission from the owner.  

---

## Attribution in Code and Config Files

It is recommended to add the following header to all major files:

```text
# ========================================================
# INNOVII IVR System
# Copyright (c) 2025 Firanmit Megersa Feyisa
# Email: megersafiranmit@gmail.com
# All rights reserved.
# ========================================================

