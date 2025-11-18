# Hobbiton Checker - Quick Start Guide 🧙‍♂️

Your Hobbiton booking availability checker is **ready to use!**

## ✅ What's Already Done

- ✅ Python virtual environment created
- ✅ All dependencies installed
- ✅ Desktop notifications tested and working
- ✅ Main checker script ready
- ✅ Test scripts created

## 🚀 Get Started in 3 Steps

### Step 1: Customize Your Dates (Optional)

Edit the dates you want to monitor in `check_availability.py`:

```bash
nano check_availability.py
# Find line 36 and update DATES_TO_CHECK
```

Or use this command to update the dates:
```bash
# Example: Monitor Christmas week
sed -i '' "s/DATES_TO_CHECK = .*/DATES_TO_CHECK = ['24-12-2025', '25-12-2025', '26-12-2025']/" check_availability.py
```

### Step 2: Set Up Email Notifications (Recommended)

**Option A: Use the interactive setup script**
```bash
./setup_email.sh
```

**Option B: Manual setup**
```bash
export SENDER_EMAIL='your-email@gmail.com'
export SENDER_PASSWORD='your-app-password'  # Get from myaccount.google.com/apppasswords
export RECIPIENT_EMAIL='your-email@gmail.com'
```

To make these permanent, add to your `~/.zshrc`:
```bash
echo 'export SENDER_EMAIL="your-email@gmail.com"' >> ~/.zshrc
echo 'export SENDER_PASSWORD="your-app-password"' >> ~/.zshrc
echo 'export RECIPIENT_EMAIL="your-email@gmail.com"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Run the Checker

**Option A: Test it first (recommended)**
```bash
cd ~/hobbiton-checker
source venv/bin/activate
python quick_check.py
```

**Option B: Run continuously (checks every hour)**
```bash
cd ~/hobbiton-checker
source venv/bin/activate
python check_availability.py
```

**Option C: Run as a background service (best for long-term)**
```bash
cd ~/hobbiton-checker
source venv/bin/activate
nohup python check_availability.py > output.log 2>&1 &
```

## 📊 Useful Commands

### Check if it's running
```bash
ps aux | grep check_availability
```

### View logs
```bash
tail -f ~/hobbiton-checker/hobbiton_checker.log
```

### Stop the checker
```bash
ps aux | grep check_availability
kill <PID>
```

### Test notifications
```bash
cd ~/hobbiton-checker
source venv/bin/activate
python test_notification.py
```

## 🔔 What Happens When Slots Are Found?

1. **Desktop notification** appears on your Mac
2. **Email** is sent (if configured) with booking links
3. **Log entry** is saved to `hobbiton_checker.log`
4. The slot is remembered to avoid duplicate notifications

## ⚙️ Advanced Setup - Run on Startup (macOS)

Create a LaunchAgent to run automatically:

```bash
cat > ~/Library/LaunchAgents/com.hobbiton.checker.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hobbiton.checker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/sam.gard/hobbiton-checker/venv/bin/python</string>
        <string>/Users/sam.gard/hobbiton-checker/check_availability.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/sam.gard/hobbiton-checker</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/sam.gard/hobbiton-checker/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/sam.gard/hobbiton-checker/stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>SENDER_EMAIL</key>
        <string>your-email@gmail.com</string>
        <key>SENDER_PASSWORD</key>
        <string>your-app-password</string>
        <key>RECIPIENT_EMAIL</key>
        <string>your-email@gmail.com</string>
    </dict>
</dict>
</plist>
EOF

# Update the email credentials in the plist file above, then:
launchctl load ~/Library/LaunchAgents/com.hobbiton.checker.plist
launchctl start com.hobbiton.checker
```

## 🎯 Current Configuration

- **Dates being monitored:** 17-12-2025, 18-12-2025, 19-12-2025
- **Check frequency:** Every hour
- **Tours monitored:** ALL 6 Hobbiton tour categories
  - EXMFFBR (Hobbiton Tour 1)
  - EXTSRBR (Extended The Shire's Rest Breakfast)
  - EXMTABR (Hobbiton Tour 2)
  - EXBTS (Hobbiton Tour 3)
  - BANQUETBR (Banquet Tour)
  - EXSBTBR (Hobbiton Tour 4)
- **Group size:** 2 people
- **Total checks per run:** 18 (6 tours × 3 dates)
- **Booking URL:** https://bookings.hobbitontours.com/

## 📝 Files in This Project

- `check_availability.py` - Main checker (runs continuously, monitors ALL 6 tours)
- `quick_check.py` - One-time check (for testing)
- `test_all_categories.py` - Check all tour categories for current availability
- `test_notification.py` - Test notifications
- `setup_email.sh` - Interactive email setup
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation
- `QUICKSTART.md` - This file!

## 🆘 Troubleshooting

### Not receiving notifications?
```bash
# Check the logs
tail -f hobbiton_checker.log

# Test notifications manually
python test_notification.py
```

### Email not working?
- Make sure you created an App Password (not your regular password)
- Check that 2-Step Verification is enabled in your Google Account
- Check spam folder
- Verify environment variables: `echo $SENDER_EMAIL`

### Desktop notifications not showing?
- Make sure System Preferences → Notifications allows Terminal/Python notifications
- Desktop notifications work automatically on macOS

## 🎉 You're All Set!

The checker is ready to use. Simply run:
```bash
cd ~/hobbiton-checker && source venv/bin/activate && python check_availability.py
```

Good luck getting your Hobbiton tour booking! 🏔️🍃

