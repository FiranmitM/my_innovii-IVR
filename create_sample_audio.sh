#!/bin/bash
# File Location: Run from asterisk-ivr-system directory
# Purpose: Create sample audio files for testing (English placeholder)
# Usage: sudo bash create_sample_audio.sh
# Note: These are PLACEHOLDER files. Replace with professional Amharic/Oromo recordings.

set -e

echo "=========================================="
echo "Creating Sample Test Audio Files"
echo "=========================================="
echo "NOTE: These are English placeholders for testing only."
echo "You MUST replace these with professional Amharic/Oromo recordings."
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run as root (use sudo)"
    exit 1
fi

# Check if espeak or festival is installed
if ! command -v espeak &> /dev/null && ! command -v text2wave &> /dev/null; then
    echo "Installing espeak for text-to-speech..."
    apt update
    apt install -y espeak sox
fi

# Create directories if they don't exist
mkdir -p /var/lib/asterisk/sounds/custom/amharic
mkdir -p /var/lib/asterisk/sounds/custom/oromo

# Function to create audio file
create_audio() {
    local filename=$1
    local text=$2
    local dir=$3

    echo "Creating $filename..."

    # Create with espeak
    if command -v espeak &> /dev/null; then
        espeak -w /tmp/temp_audio.wav "$text" 2>/dev/null
        # Convert to proper format
        sox /tmp/temp_audio.wav -r 8000 -c 1 -b 16 "$dir/$filename" 2>/dev/null
        rm /tmp/temp_audio.wav
    elif command -v text2wave &> /dev/null; then
        echo "$text" | text2wave -o /tmp/temp_audio.wav
        sox /tmp/temp_audio.wav -r 8000 -c 1 -b 16 "$dir/$filename" 2>/dev/null
        rm /tmp/temp_audio.wav
    else
        echo "Error: No text-to-speech tool available"
        exit 1
    fi
}

# Create Amharic directory files (English placeholders)
AMHARIC_DIR="/var/lib/asterisk/sounds/custom/amharic"

create_audio "welcome.wav" "Welcome to INNOVII IVR service" "$AMHARIC_DIR"
create_audio "not_subscribed.wav" "You are not subscribed to our service. We provide M-Beauty and M-Health services." "$AMHARIC_DIR"
create_audio "subscribe_prompt.wav" "To subscribe to our service, press 1" "$AMHARIC_DIR"
create_audio "subscribed_success.wav" "You have successfully subscribed to INNOVII service. Press 1 to continue, or 0 to cancel." "$AMHARIC_DIR"
create_audio "choose_language.wav" "Press 1 for Amharic, Press 2 for Oromo" "$AMHARIC_DIR"
create_audio "main_menu.wav" "Main Menu. Press 1 for M-Beauty, Press 2 for M-Health, Press 3 to Unsubscribe" "$AMHARIC_DIR"

# M-Beauty files
create_audio "beauty.wav" "Welcome to M-Beauty service" "$AMHARIC_DIR"
create_audio "beauty_menu.wav" "Press 1 to listen to lessons, Press 2 to ask a question, Press 3 to return to main menu" "$AMHARIC_DIR"

# Create 10 beauty lesson files
for i in {1..10}; do
    create_audio "beauty_lesson$i.wav" "This is beauty lesson number $i. Press star to go back, press hash to go to next lesson, press 0 to return to menu." "$AMHARIC_DIR"
done

# M-Health files
create_audio "health.wav" "Welcome to M-Health service" "$AMHARIC_DIR"
create_audio "health_menu.wav" "Press 1 for Mother Health, Press 2 for Child Health, Press 3 to return to main menu" "$AMHARIC_DIR"
create_audio "mother_health.wav" "Mother Health Services" "$AMHARIC_DIR"
create_audio "child_health.wav" "Child Health Services" "$AMHARIC_DIR"

# Create 10 mother health lesson files
for i in {1..10}; do
    create_audio "mother_health_lesson$i.wav" "This is mother health lesson number $i. Press star to go back, press hash to go to next lesson, press 0 to return to menu." "$AMHARIC_DIR"
done

# Create 10 child health lesson files
for i in {1..10}; do
    create_audio "child_health_lesson$i.wav" "This is child health lesson number $i. Press star to go back, press hash to go to next lesson, press 0 to return to menu." "$AMHARIC_DIR"
done

# Questions
create_audio "questions_prompt.wav" "Please record your question after the beep. Press hash when finished" "$AMHARIC_DIR"

# Unsubscribe
create_audio "unsubscribe_confirm.wav" "Are you sure you want to unsubscribe? Press 1 to confirm, Press 0 to cancel" "$AMHARIC_DIR"

# General messages
create_audio "invalid_option.wav" "Invalid option. Please try again" "$AMHARIC_DIR"
create_audio "goodbye.wav" "Thank you for using INNOVII service. Goodbye" "$AMHARIC_DIR"

# Copy all files to Oromo directory for testing (same English files)
echo "Copying files to Oromo directory..."
cp -r $AMHARIC_DIR/* /var/lib/asterisk/sounds/custom/oromo/

# Set permissions
chown -R asterisk:asterisk /var/lib/asterisk/sounds/custom
chmod -R 644 /var/lib/asterisk/sounds/custom/*.wav

echo ""
echo "=========================================="
echo "Sample Audio Files Created Successfully!"
echo "=========================================="
echo ""
echo "Files created in:"
echo "  - /var/lib/asterisk/sounds/custom/amharic/"
echo "  - /var/lib/asterisk/sounds/custom/oromo/"
echo ""
echo "IMPORTANT: These are ENGLISH PLACEHOLDERS for testing."
echo "You MUST replace them with professional Amharic and Oromo recordings."
echo ""
echo "Files created:"
echo "  - Welcome and subscription messages"
echo "  - Language selection prompts"
echo "  - Main menu prompts"
echo "  - M-Beauty menu and 10 lessons"
echo "  - M-Health menu (Mother: 10 lessons, Child: 10 lessons)"
echo "  - Question prompts"
echo "  - Unsubscribe prompts"
echo "  - General messages (invalid, goodbye)"
echo ""
echo "Total files per language: ~40 audio files"
echo ""
echo "Next step: Test by calling extension 5000"
echo "=========================================="
