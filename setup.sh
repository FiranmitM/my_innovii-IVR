#!/bin/bash
# File Location: Run this script from the asterisk-ivr-system directory
# Purpose: Automated setup script for INNOVII IVR System
# Usage: sudo bash setup.sh

set -e

echo "=========================================="
echo "INNOVII IVR System Setup Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run as root (use sudo)"
    exit 1
fi

echo "[1/8] Installing required packages..."
apt update
apt install -y asterisk asterisk-core-sounds-en asterisk-mysql mysql-server python3 python3-pip sox

echo "[2/8] Installing Python packages..."
pip3 install mysql-connector-python

echo "[3/8] Setting up MySQL database..."
# Start MySQL if not running
systemctl start mysql
systemctl enable mysql

# Create database and user
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS innovii CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'innovii'@'localhost' IDENTIFIED BY 'innovii@1234';
GRANT ALL PRIVILEGES ON innovii.* TO 'innovii'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "[4/8] Importing database schema..."
mysql -u innovii -p'innovii@1234' innovii < innovii_schema.sql

echo "[5/8] Copying configuration files..."
# Backup existing files
cp /etc/asterisk/extensions.conf /etc/asterisk/extensions.conf.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
cp /etc/asterisk/pjsip.conf /etc/asterisk/pjsip.conf.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# Copy new configuration files
cp extensions.conf /etc/asterisk/
cp pjsip.conf /etc/asterisk/
cp innovii_schema.sql /etc/asterisk/
chmod 644 /etc/asterisk/extensions.conf
chmod 644 /etc/asterisk/pjsip.conf
chmod 644 /etc/asterisk/innovii_schema.sql

echo "[6/8] Installing AGI scripts..."
mkdir -p /var/lib/asterisk/agi-bin
cp agi-scripts/*.py /var/lib/asterisk/agi-bin/
chmod +x /var/lib/asterisk/agi-bin/*.py
chown asterisk:asterisk /var/lib/asterisk/agi-bin/*.py

echo "[7/8] Creating audio directories..."
mkdir -p /var/lib/asterisk/sounds/custom/amharic
mkdir -p /var/lib/asterisk/sounds/custom/oromo
chown -R asterisk:asterisk /var/lib/asterisk/sounds/custom

echo "[8/8] Restarting Asterisk..."
systemctl restart asterisk
systemctl enable asterisk

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Copy your audio files to:"
echo "   /var/lib/asterisk/sounds/custom/amharic/"
echo "   /var/lib/asterisk/sounds/custom/oromo/"
echo ""
echo "2. Test the system:"
echo "   - Register a SIP client (Linphone/Zoiper) with:"
echo "     Username: 1001, Password: pass1001, Server: YOUR_SERVER_IP"
echo "   - Call extension 5000"
echo ""
echo "3. Monitor Asterisk:"
echo "   sudo asterisk -rvvv"
echo ""
echo "4. Check logs:"
echo "   sudo tail -f /var/log/asterisk/full"
echo ""
echo "5. Verify database:"
echo "   mysql -u innovii -p'innovii@1234' innovii -e 'SHOW TABLES;'"
echo ""
echo "SIP Users configured (1001-1010):"
echo "  Username: 1001, Password: pass1001"
echo "  Username: 1002, Password: pass1002"
echo "  Username: 1003, Password: pass1003"
echo "  Username: 1004, Password: pass1004"
echo "  Username: 1005, Password: pass1005"
echo "  ... through 1010"
echo ""
echo "For detailed instructions, see README.md"
echo "For audio file guide, see AUDIO_FILES_GUIDE.md"
echo "=========================================="

;this projectis developed by Firanmit Megersa, use the following contact contact to contact him: 
;email: megersafiranmit@gmail.com
;telegram: @lovecisco
