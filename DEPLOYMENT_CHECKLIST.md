INNOVII IVR System - Deployment Checklist
Pre-Deployment Checklist
1. System Requirements
 Linux server (Ubuntu 20.04+ or Debian 11+)
 Minimum 2GB RAM
 Minimum 20GB disk space
 Root/sudo access
 Stable internet connection
 Static IP address or domain name
2. Installation
 Run setup script: sudo bash setup.sh
 Verify installation: sudo bash test_system.sh
 All tests pass
 Asterisk service running
 MySQL service running
3. Database Configuration
 MySQL database 'innovii' created
 User 'innovii' created with password 'innovii@1234'
 All tables created (subscribers, lesson_progress, questions, call_logs)
 Test data inserted successfully
 Database connection tested from AGI scripts
 Indexes created for performance
Production Security: Change default password!

mysql -u root -p

ALTER USER 'innovii'@'localhost' IDENTIFIED BY 'YOUR_SECURE_PASSWORD';

FLUSH PRIVILEGES;
Then update password in all AGI scripts in /var/lib/asterisk/agi-bin/

4. Audio Files
 All Amharic audio files recorded professionally
 All Oromo audio files recorded professionally
 Audio files in correct format (8kHz, 16-bit, mono, WAV)
 All files copied to /var/lib/asterisk/sounds/custom/amharic/
 All files copied to /var/lib/asterisk/sounds/custom/oromo/
 File permissions set correctly (asterisk:asterisk, 644)
 Audio quality tested
Required Audio Files (per language):

 welcome.wav
 not_subscribed.wav
 subscribe_prompt.wav
 subscribed_success.wav
 choose_language.wav
 main_menu.wav
 beauty.wav
 beauty_menu.wav
 beauty_lesson1.wav through beauty_lesson10.wav (10 files)
 health.wav
 health_menu.wav
 mother_health.wav
 mother_health_lesson1.wav through mother_health_lesson10.wav (10 files)
 child_health.wav
 child_health_lesson1.wav through child_health_lesson10.wav (10 files)
 questions_prompt.wav
 unsubscribe_confirm.wav
 invalid_option.wav
 goodbye.wav
Total: ~40 audio files × 2 languages = ~80 audio files

5. Asterisk Configuration
 pjsip.conf configured with all users
 extensions.conf dialplan tested
 Extension 5000 accessible
 DTMF recognition working
 Audio playback working
 Menu navigation working
 Dialplan reload successful: sudo asterisk -rx "dialplan reload"
 PJSIP reload successful: sudo asterisk -rx "pjsip reload"
6. SIP User Configuration
 Users 1001-1010 configured in pjsip.conf
 User credentials documented
 Test registration with at least 2 clients
 Successful calls between users
 Successful calls to extension 5000
Production Security: Change default SIP passwords! Edit /etc/asterisk/pjsip.conf and change all passwords from passXXXX to secure passwords.

7. AGI Scripts
 All 9 AGI scripts copied to /var/lib/asterisk/agi-bin/
 Scripts are executable (chmod +x)
 Scripts owned by asterisk user
 Python3 installed
 mysql-connector-python installed
 Each script tested individually
 Scripts return correct data
8. Network Configuration
 Firewall configured to allow SIP (UDP 5060)
 Firewall configured to allow RTP (UDP 10000-20000)
 Port forwarding configured (if behind NAT)
 External IP/domain configured in pjsip.conf (if needed)
# Configure firewall

sudo ufw allow 5060/udp

sudo ufw allow 5060/tcp

sudo ufw allow 10000:20000/udp

sudo ufw enable
9. Testing
 Register test SIP client (Linphone/Zoiper)
 Dial extension 5000
 Test subscription flow (new user)
 Test language selection (Amharic)
 Test language selection (Oromo)
 Test M-Beauty menu
 Test beauty lessons (play, *, #, 0)
 Test beauty questions recording
 Test M-Health menu
 Test mother health lessons
 Test child health lessons
 Test unsubscribe flow
 Test database logging (call_logs table)
 Test with multiple simultaneous calls
 Test with poor network conditions
10. Performance Optimization
 MySQL query optimization enabled
 Database indexes created
 Asterisk logging level set appropriately
 System resources monitored (CPU, RAM, disk)
 Audio files optimized for size
 Concurrent call limit tested
11. Backup and Recovery
 Database backup script created
 Configuration files backed up
 Audio files backed up
 Backup tested (restore procedure)
 Backup schedule automated
Create backup:

# Backup script

#!/bin/bash

BACKUP_DIR="/backup/innovii/$(date +%Y%m%d)"

mkdir -p $BACKUP_DIR


# Backup database

mysqldump -u innovii -p'innovii@1234' innovii > $BACKUP_DIR/innovii_db.sql


# Backup configs

cp /etc/asterisk/extensions.conf $BACKUP_DIR/

cp /etc/asterisk/pjsip.conf $BACKUP_DIR/


# Backup AGI scripts

cp -r /var/lib/asterisk/agi-bin $BACKUP_DIR/


# Backup audio (optional, if they change)

# tar -czf $BACKUP_DIR/audio_files.tar.gz /var/lib/asterisk/sounds/custom
12. Monitoring and Logging
 Asterisk logs configured
 Log rotation enabled
 Real-time monitoring setup
 Alert system for critical errors
 Call analytics dashboard (optional)
# Check log rotation

cat /etc/logrotate.d/asterisk
13. Security Hardening
 MySQL root password changed
 MySQL remote access disabled
 innovii database password changed from default
 SIP passwords changed from default
 Fail2ban installed and configured for Asterisk
 SSL/TLS enabled for SIP (optional)
 Regular security updates enabled
Install Fail2ban:

sudo apt install fail2ban

sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Edit jail.local and enable asterisk jails

sudo systemctl restart fail2ban
14. Documentation
 System architecture documented
 Network diagram created
 User credentials documented securely
 Database schema documented
 IVR flow diagram created
 Troubleshooting guide accessible
 Contact information for support
 Training materials for operators
15. Production Deployment
 All previous checklist items completed
 System tested in staging environment
 Load testing completed
 Rollback plan prepared
 Deployment window scheduled
 Stakeholders notified
 Monitoring active
 Support team on standby
16. Post-Deployment
 Monitor system for 24 hours
 Review logs for errors
 Check database for anomalies
 Verify all features working
 Collect user feedback
 Performance metrics collected
 Issues documented and addressed
 Success metrics measured
Production Environment Variables
Update these in production:

Database Password (in all AGI scripts):

password='YOUR_SECURE_PASSWORD'
SIP Passwords (in pjsip.conf):

password=SECURE_PASSWORD_HERE
External Network (in pjsip.conf if needed):

external_media_address=YOUR_PUBLIC_IP

external_signaling_address=YOUR_PUBLIC_IP
Launch Checklist
Day Before Launch
 Final backup completed
 All systems tested
 Team briefed
 Support procedures reviewed
 Monitoring systems checked
 Rollback procedure tested
Launch Day
 System status: GREEN
 All services running
 Monitoring active
 Support team available
 First test call successful
 User notifications sent
First Week Post-Launch
 Daily log reviews
 Daily database checks
 User feedback collected
 Performance monitored
 Issues tracked and resolved
 Metrics analyzed
Success Metrics
Define and track:

 Total calls per day
 Average call duration
 Subscription rate
 Service usage (M-Beauty vs M-Health)
 Language preference distribution
 User satisfaction (from feedback)
 System uptime percentage
 Error rate
Support and Maintenance
Daily
 Check system status
 Review error logs
 Monitor disk space
Weekly
 Review call analytics
 Database optimization
 Security updates
 Backup verification
Monthly
 Comprehensive system audit
 Performance review
 User feedback analysis
 Capacity planning
 Update documentation
Emergency Contacts
Document:

 System administrator contact
 Database administrator contact
 Network administrator contact
 Audio production team contact
 Business stakeholder contact
 Escalation procedure
Signature:

Prepared by:Firanmit Megersa(INNOVII IT Technician) Date: OCT 2025

Reviewed by: _________________ Date: _________

Approved by: _________________ Date: _________

Deployed by: _________________ Date: _________
