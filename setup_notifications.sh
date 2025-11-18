#!/bin/bash

echo "========================================"
echo "Hobbiton Checker - Complete Setup"
echo "========================================"
echo ""

# Test desktop notifications first
echo "1. Testing desktop notifications..."
osascript -e 'display notification "✅ If you see this, notifications are working!" with title "Hobbiton Checker Test"'
echo ""
echo "   Did you see a notification in the top-right corner?"
echo "   If NOT, you may need to enable notifications for Terminal:"
echo "   • Open System Settings → Notifications → Terminal"
echo "   • Enable 'Allow Notifications'"
echo ""
read -p "Press Enter to continue to email setup..."
echo ""

# Email setup
echo "========================================"
echo "2. Email Setup"
echo "========================================"
echo ""
echo "For Gmail, you need an App Password (NOT your regular password):"
echo "1. Go to: https://myaccount.google.com/apppasswords"
echo "2. Create an App Password for 'Mail'"
echo "3. Copy the 16-character password (no spaces)"
echo ""
read -p "Press Enter when ready..."
echo ""

read -p "Enter your sender email (Gmail): " sender_email
read -sp "Enter your App Password (16 chars): " sender_password
echo ""
read -p "Enter recipient email (can be same): " recipient_email
echo ""

# Validate
if [[ -z "$sender_email" || -z "$sender_password" || -z "$recipient_email" ]]; then
    echo "❌ Error: All fields are required!"
    exit 1
fi

# Test the email settings
echo ""
echo "Testing email configuration..."

cd /Users/sam.gard/hobbiton-checker
source venv/bin/activate

# Export for this test
export SENDER_EMAIL="$sender_email"
export SENDER_PASSWORD="$sender_password"
export RECIPIENT_EMAIL="$recipient_email"

python test_notification.py

# If test succeeded, save to .zshrc
echo ""
read -p "Did the email test work? Add to ~/.zshrc? (y/n): " save_choice

if [[ $save_choice == "y" || $save_choice == "Y" ]]; then
    # Remove any existing entries
    sed -i '' '/# Hobbiton Checker/d' ~/.zshrc 2>/dev/null
    sed -i '' '/SENDER_EMAIL/d' ~/.zshrc 2>/dev/null
    sed -i '' '/SENDER_PASSWORD/d' ~/.zshrc 2>/dev/null
    sed -i '' '/RECIPIENT_EMAIL/d' ~/.zshrc 2>/dev/null
    
    # Add new entries
    echo "" >> ~/.zshrc
    echo "# Hobbiton Checker Email Configuration" >> ~/.zshrc
    echo "export SENDER_EMAIL='$sender_email'" >> ~/.zshrc
    echo "export SENDER_PASSWORD='$sender_password'" >> ~/.zshrc
    echo "export RECIPIENT_EMAIL='$recipient_email'" >> ~/.zshrc
    
    echo ""
    echo "✅ Added to ~/.zshrc"
    echo ""
    echo "To activate in new terminals, run:"
    echo "  source ~/.zshrc"
    echo ""
    echo "For the current session, the variables are already set!"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next: Test the full checker with:"
echo "  cd ~/hobbiton-checker"
echo "  source venv/bin/activate"
echo "  source ~/.zshrc  # If you saved to .zshrc"
echo "  python quick_check.py"
echo ""
