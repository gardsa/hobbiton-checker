# Hobbiton Booking Availability Checker

This script monitors the Hobbiton Movie Set Tour booking website and notifies you when slots become available for your desired dates.

## Features

- ✅ Checks availability every hour automatically
- 📧 Email notifications when slots become available
- 🔔 Desktop notifications (macOS supported)
- 📝 Logs all activity to `hobbiton_checker.log`
- 🔄 Avoids duplicate notifications for the same slots

## Quick Start

**👉 See [QUICKSTART.md](QUICKSTART.md) for a streamlined setup guide!**

## Setup

### 1. Install Python Dependencies

✅ **Already done!** Dependencies are installed in the virtual environment.

If you need to reinstall:
```bash
cd ~/hobbiton-checker
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Email Notifications (Optional but Recommended)

**Easy Setup:**
```bash
./setup_email.sh
```

The setup script will guide you through:
- Creating a Gmail App Password
- Setting environment variables
- Testing email notifications

**Manual Setup:**

For Gmail, you'll need to create an "App Password":

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Scroll down to "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password

Then set these environment variables:

```bash
export SENDER_EMAIL='your-email@gmail.com'
export SENDER_PASSWORD='your-16-char-app-password'
export RECIPIENT_EMAIL='your-email@gmail.com'  # Can be the same or different
```

To make these permanent, add them to your `~/.zshrc` or `~/.bash_profile`:

```bash
echo 'export SENDER_EMAIL="your-email@gmail.com"' >> ~/.zshrc
echo 'export SENDER_PASSWORD="your-app-password"' >> ~/.zshrc
echo 'export RECIPIENT_EMAIL="your-email@gmail.com"' >> ~/.zshrc
source ~/.zshrc
```

**For other email providers:**
- Update `SMTP_SERVER` and `SMTP_PORT` in the script
- Common settings:
  - Gmail: `smtp.gmail.com`, port `587`
  - Outlook: `smtp-mail.outlook.com`, port `587`
  - Yahoo: `smtp.mail.yahoo.com`, port `587`

### 3. Customize Dates (Optional)

Edit `check_availability.py` and modify the `DATES_TO_CHECK` list:

```python
DATES_TO_CHECK = ['17-12-2025', '18-12-2025', '19-12-2025']
```

## Running the Script

### Option 1: Quick Test (Recommended First)

```bash
cd ~/hobbiton-checker
source venv/bin/activate
python quick_check.py
```

This runs a single check to verify everything works, then exits.

### Option 2: Run Continuously (Production)

```bash
cd ~/hobbiton-checker
source venv/bin/activate
python check_availability.py
```

This will check immediately and then every hour. Press `Ctrl+C` to stop.

### Option 3: Run in Background

```bash
cd ~/hobbiton-checker
source venv/bin/activate
nohup python check_availability.py > output.log 2>&1 &
```

To stop it later:
```bash
ps aux | grep check_availability.py
kill <PID>
```

### Option 4: Run as a Service (macOS - Recommended for Long-term)

Create a LaunchAgent to run automatically on startup:

```bash
# Create the plist file
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

# Load the service
launchctl load ~/Library/LaunchAgents/com.hobbiton.checker.plist

# Start the service
launchctl start com.hobbiton.checker
```

**Important:** Update the email credentials in the plist file!

To stop the service:
```bash
launchctl stop com.hobbiton.checker
launchctl unload ~/Library/LaunchAgents/com.hobbiton.checker.plist
```

## Hosting Options

### Local Machine (Current Setup)
✅ **Best for: Short-term monitoring (a few days/weeks)**
- Free
- Easy to set up
- Requires your computer to be running
- Use Option 3 (LaunchAgent) for automatic startup

### Cloud Hosting (For Long-term)

If you want it to run 24/7 without your computer being on:

#### 1. **PythonAnywhere** (Free tier available)
```bash
# Upload files to PythonAnywhere
# Set up a scheduled task to run the script hourly
```

#### 2. **Heroku** (Requires credit card but has free hours)
```bash
# Add a Procfile
echo "worker: python check_availability.py" > Procfile
# Deploy to Heroku
```

#### 3. **AWS Lambda / Google Cloud Functions** (Pay-per-execution)
- More complex setup but very cheap for hourly checks
- Would need modification to work with serverless architecture

#### 4. **Replit** (Free tier available)
- Upload the files
- Click "Run" and keep the tab open
- Use Replit's "Always On" feature (paid)

## Monitoring

### Check if it's running:
```bash
ps aux | grep check_availability.py
```

### View logs:
```bash
tail -f ~/hobbiton-checker/hobbiton_checker.log
```

### Check recent activity:
```bash
cat ~/hobbiton-checker/hobbiton_checker.log | grep "Found available"
```

## Troubleshooting

### No notifications received?
1. Check the log file: `tail -f hobbiton_checker.log`
2. Verify email settings are correct
3. Check spam folder
4. Try running manually first to test

### Script not running?
```bash
# Check if service is loaded (macOS)
launchctl list | grep hobbiton

# Check logs
cat ~/hobbiton-checker/stderr.log
```

### Website structure changed?
The script may need updates if Hobbiton changes their website. Check the logs for errors.

## What Happens When a Slot is Found?

1. 🔔 **Desktop notification** appears (if supported)
2. 📧 **Email** is sent with booking links
3. 📝 **Log entry** is created
4. The script remembers this slot to avoid duplicate notifications

## Notes

- The script checks every hour to be respectful to Hobbiton's servers
- It adds a 2-second delay between checking different dates
- Desktop notifications work on macOS automatically
- Email notifications require setup but are more reliable

## Questions?

Check the logs first! Most issues are logged with helpful error messages.

Good luck getting your Hobbiton tour booking! 🧙‍♂️

