#!/bin/bash
# File Location: Run from asterisk-ivr-system directory
# Purpose: Test INNOVII IVR System components
# Usage: sudo bash test_system.sh

echo "=========================================="
echo "INNOVII IVR System Test Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test function
test_component() {
    local test_name=$1
    local test_command=$2

    echo -n "Testing $test_name... "
    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        ((FAILED++))
        return 1
    fi
}

echo "[1] Testing MySQL Database Connection"
echo "--------------------------------------"
test_component "MySQL service" "systemctl is-active --quiet mysql"
test_component "Database 'innovii' exists" "mysql -u innovii -p'Innovii@123' -e 'USE innovii' 2>/dev/null"
test_component "Table 'subscribers' exists" "mysql -u innovii -p'Innovii@123' innovii -e 'DESCRIBE subscribers' 2>/dev/null"    
test_component "Table 'lesson_progress' exists" "mysql -u innovii -p'Innovii@123' innovii -e 'DESCRIBE lesson_progress' 2>/dev/null"
test_component "Table 'questions' exists" "mysql -u innovii -p'Innovii@123' innovii -e 'DESCRIBE questions' 2>/dev/null"        
test_component "Table 'call_logs' exists" "mysql -u innovii -p'Innovii@123' innovii -e 'DESCRIBE call_logs' 2>/dev/null"        
echo ""

echo "[2] Testing Asterisk Service"
echo "--------------------------------------"
test_component "Asterisk service running" "systemctl is-active --quiet asterisk"
test_component "Asterisk listening on port 5060" "netstat -tuln | grep -q ':5060'"
echo ""

echo "[3] Testing Configuration Files"
echo "--------------------------------------"
test_component "extensions.conf exists" "test -f /etc/asterisk/extensions.conf"
test_component "pjsip.conf exists" "test -f /etc/asterisk/pjsip.conf"
test_component "extensions.conf readable" "test -r /etc/asterisk/extensions.conf"
test_component "pjsip.conf readable" "test -r /etc/asterisk/pjsip.conf"
echo ""

echo "[4] Testing AGI Scripts"
echo "--------------------------------------"
test_component "check_subscription.py exists" "test -f /var/lib/asterisk/agi-bin/check_subscription.py"
test_component "subscribe_user.py exists" "test -f /var/lib/asterisk/agi-bin/subscribe_user.py"
test_component "unsubscribe_user.py exists" "test -f /var/lib/asterisk/agi-bin/unsubscribe_user.py"
test_component "update_language.py exists" "test -f /var/lib/asterisk/agi-bin/update_language.py"
test_component "get_lesson_progress.py exists" "test -f /var/lib/asterisk/agi-bin/get_lesson_progress.py"
test_component "update_lesson_progress.py exists" "test -f /var/lib/asterisk/agi-bin/update_lesson_progress.py"
test_component "save_question.py exists" "test -f /var/lib/asterisk/agi-bin/save_question.py"
test_component "log_call.py exists" "test -f /var/lib/asterisk/agi-bin/log_call.py"
test_component "end_call.py exists" "test -f /var/lib/asterisk/agi-bin/end_call.py"
test_component "AGI scripts executable" "test -x /var/lib/asterisk/agi-bin/check_subscription.py"
echo ""

echo "[5] Testing Python Dependencies"
echo "--------------------------------------"
test_component "Python3 installed" "which python3"
test_component "mysql-connector-python installed" "python3 -c 'import mysql.connector'"
echo ""

echo "[6] Testing Audio Directories"
echo "--------------------------------------"
test_component "Amharic audio directory exists" "test -d /var/lib/asterisk/sounds/custom/amharic"
test_component "Oromo audio directory exists" "test -d /var/lib/asterisk/sounds/custom/oromo"
test_component "Audio directories writable" "test -w /var/lib/asterisk/sounds/custom/amharic"
echo ""

echo "[7] Testing Asterisk Dialplan"
echo "--------------------------------------"
if asterisk -rx "dialplan show innovii-ivr" >/dev/null 2>&1; then
    echo -n "Testing dialplan 'innovii-ivr' loaded... "
    if asterisk -rx "dialplan show innovii-ivr" | grep -q "5000"; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}FAILED${NC}"
        ((FAILED++))
    fi
else
    echo -e "${YELLOW}WARNING: Cannot test dialplan (Asterisk may not be fully started)${NC}"
fi
echo ""

echo "[8] Testing PJSIP Endpoints"
echo "--------------------------------------"
if asterisk -rx "pjsip show endpoints" >/dev/null 2>&1; then
    for user in 1001 1002 1003 1004 1005; do
        echo -n "Testing endpoint $user... "
        if asterisk -rx "pjsip show endpoint $user" | grep -q "$user"; then
            echo -e "${GREEN}PASSED${NC}"
            ((PASSED++))
        else
            echo -e "${RED}FAILED${NC}"
            ((FAILED++))
        fi
    done
else
    echo -e "${YELLOW}WARNING: Cannot test endpoints (Asterisk may not be fully started)${NC}"
fi
echo ""

echo "[9] Testing Database Functions"
echo "--------------------------------------"
# Test inserting a subscriber
echo -n "Testing subscriber insertion... "
if mysql -u innovii -p'Innovii@123' innovii -e "INSERT INTO subscribers (phone_number, subscribed, preferred_language) VALUES ('5000', 1, 'amharic')" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}FAILED${NC}"
    ((FAILED++))
fi

# Test querying a subscriber
echo -n "Testing subscriber query... "
if mysql -u innovii -p'Innovii@123' innovii -e "SELECT * FROM subscribers WHERE phone_number='5000'" 2>/dev/null | grep -q '5000'; then
    echo -e "${GREEN}PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}FAILED${NC}"
    ((FAILED++))
fi

# Cleanup test data
mysql -u innovii -p'Innovii@123' innovii -e "DELETE FROM subscribers WHERE phone_number='5000'" 2>/dev/null
echo ""

echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "Tests Passed: ${GREEN}$PASSED${NC}"
echo -e "Tests Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! System is ready.${NC}"
    echo ""
    echo "You can now:"
    echo "1. Add your audio files to /var/lib/asterisk/sounds/custom/"
    echo "2. Register a SIP client and dial 5000"
    echo "3. Monitor with: sudo asterisk -rvvv"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the errors above.${NC}"
    echo ""
    echo "Common issues:"
    echo "- Asterisk not fully started: sudo systemctl restart asterisk"
    echo "- Database permissions: Check MySQL user 'innovii'"
    echo "- Missing files: Re-run setup.sh"
    exit 1
fi
