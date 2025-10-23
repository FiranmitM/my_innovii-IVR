Audio Files Guide for INNOVII IVR System
Audio File Requirements
Format Specifications
Format: WAV (PCM)
Sample Rate: 8000 Hz (8 kHz)
Bit Depth: 16-bit
Channels: Mono (1 channel)
Codec: PCM unsigned 8-bit or signed 16-bit
Converting Audio Files
Use the following command to convert your audio files to the correct format:

# Using SoX (Sound eXchange)

sox input.mp3 -r 8000 -c 1 -b 16 output.wav


# Using FFmpeg

ffmpeg -i input.mp3 -ar 8000 -ac 1 -ab 128k output.wav
Required Audio Files
Directory Structure
/var/lib/asterisk/sounds/custom/
├── amharic/
│   └── (All files below in Amharic)
└── oromo/
    └── (All files below in Oromo)
Files Needed for Each Language
1. Welcome & Subscription (Non-subscribed users)
welcome.wav - "Welcome to INNOVII IVR service"
not_subscribed.wav - "You are not subscribed to our service. We provide M-Beauty and M-Health services."
subscribe_prompt.wav - "To subscribe to our service, press 1"
subscribed_success.wav - "You have successfully subscribed to INNOVII service"
2. Language Selection
choose_language.wav - "Press 1 for Amharic, Press 2 for Oromo"
3. Main Menu
main_menu.wav - "Press 1 for M-Beauty, Press 2 for M-Health, Press 3 to Unsubscribe"
4. M-Beauty Service
beauty.wav - "Welcome to M-Beauty service"
beauty_menu.wav - "Press 1 to listen to lessons, Press 2 to ask a question, Press 3 to return to main menu"
beauty_lesson1.wav through beauty_lesson10.wav - Individual beauty lesson recordings
5. M-Health Service
health.wav - "Welcome to M-Health service"
health_menu.wav - "Press 1 for Mother Health, Press 2 for Child Health, Press 3 to return to main menu"
6. Mother Health Lessons
mother_health.wav - "Mother Health Services"
mother_health_lesson1.wav through mother_health_lesson10.wav - Mother health lesson recordings
7. Child Health Lessons
child_health.wav - "Child Health Services"
child_health_lesson1.wav through child_health_lesson10.wav - Child health lesson recordings
8. Questions
questions_prompt.wav - "Please record your question after the beep. Press # when finished"
9. Unsubscribe
unsubscribe_confirm.wav - "Are you sure you want to unsubscribe? Press 1 to confirm, Press 0 to cancel"
10. General Messages
invalid_option.wav - "Invalid option. Please try again"
goodbye.wav - "Thank you for using INNOVII service. Goodbye"
Sample Scripts for Recording
For Amharic Files
welcome.wav: "እንኳን ወደ ኢኖቪ አይቪአር አገልግሎት በደህና መጡ"
not_subscribed.wav: "እርስዎ በአገልግሎታችን አልተመዘገቡም። እኛ ኤም-ቢውቲ እና ኤም-ሄልዝ አገልግሎቶችን እንሰጣለን።"
subscribe_prompt.wav: "ለመመዝገብ 1ን ይጫኑ"
subscribed_success.wav: "በኢኖቪ አገልግሎት በተሳካ ሁኔታ ተመዝግበዋል"
choose_language.wav: "ለአማርኛ 1ን ለኦሮምኛ 2ን ይጫኑ"
main_menu.wav: "ለኤም-ቢውቲ 1ን ለኤም-ሄልዝ 2ን ለመውጣት 3ን ይጫኑ"
beauty_menu.wav: "ትምህርቶችን ለማዳመጥ 1ን ጥያቄ ለመጠየቅ 2ን ወደ ዋናው ሜኑ ለመመለስ 3ን ይጫኑ"
health_menu.wav: "ለእናቶች ጤና 1ን ለህጻናት ጤና 2ን ወደ ዋናው ሜኑ ለመመለስ 3ን ይጫኑ"
questions_prompt.wav: "ከቢፕ በኋላ ጥያቄዎን ይቅዱ። ሲጨርሱ # ይጫኑ"
unsubscribe_confirm.wav: "መመዝገቢያዎን መሰረዝ ይፈልጋሉ? ለማረጋገጥ 1ን ለመሰረዝ 0ን ይጫኑ"
invalid_option.wav: "ልክ ያልሆነ ምርጫ። እባክዎ እንደገና ይሞክሩ"
goodbye.wav: "ኢኖቪን ስለተጠቀሙ እናመሰግናለን። ደህና ይሁኑ"
For Oromo Files
(Provide the same prompts translated to Oromo language)

Creating Test Audio Files
If you don't have audio files yet, you can create simple test files using text-to-speech:

# Using espeak (install: sudo apt install espeak)

espeak -w welcome.wav "Welcome to INNOVII IVR service"


# Or using festival (install: sudo apt install festival)

echo "Welcome to INNOVII IVR service" | text2wave -o welcome.wav
File Permissions
After copying files, ensure correct permissions:

sudo chown -R asterisk:asterisk /var/lib/asterisk/sounds/custom

sudo chmod -R 644 /var/lib/asterisk/sounds/custom/*.wav
Testing Audio Files
Test that Asterisk can play your files:

# In Asterisk CLI

asterisk -rvvv

CLI> originate Local/1001@innovii-ivr extension playback@test-audio
Tips for Recording Professional Audio
Use a quiet room - Minimize background noise
Speak clearly - Enunciate words properly
Maintain consistent volume - Don't speak too loud or too soft
Use professional voice talent - Consider hiring voice actors for Amharic and Oromo
Edit properly - Remove long pauses, clicks, and background noise
Normalize audio - Ensure consistent volume across all files
Add pauses - Leave appropriate pauses between sentences for clarity
Professional Audio Services (Optional)
Consider these options for professional quality:

Local Amharic/Oromo voice actors
Audio production studios in Ethiopia
Online services like Fiverr or Upwork for voice-over work
Text-to-speech services with Amharic/Oromo support
