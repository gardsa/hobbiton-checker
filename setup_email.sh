#!/bin/bash
# Setup script for Hobbiton Checker email notifications

echo "=========================================="
echo "Hobbiton Checker - Email Setup"
echo "=========================================="
echo ""
echo "This script will help you configure email notifications."
echo ""
echo "For Gmail users:"
echo "1. Go to https://myaccount.google.com/security"
echo "2. Enable 2-Step Verification (if not already enabled)"
echo "3. Go to https://myaccount.google.com/apppasswords"
echo "4. Create an App Password for 'Mail'"
echo "5. Copy the 16-character password"
echo ""
read -p "Press Enter when you have your App Password ready..."
echo ""

# Get email details
read -p "Enter your sender email (e.g., your-email@gmail.com): " sender_email
read -sp "Enter your App Password (16 characters, no spaces): " sender_password
echo ""
read -p "Enter recipient email (can be same as sender): " recipient_email
echo ""

# Ask if they want to add to shell profile
echo ""
echo "Would you like to add these to your ~/.zshrc file?"
echo "This will make them permanent (recommended)."
read -p "Add to ~/.zshrc? (y/n): " add_to_profile

if [[ $add_to_profile == "y" || $add_to_profile == "Y" ]]; then
    echo "" >> ~/.zshrc
    echo "# Hobbiton Checker Email Configuration" >> ~/.zshrc
    echo "export SENDER_EMAIL='$sender_email'" >> ~/.zshrc
    echo "export SENDER_PASSWORD='$sender_password'" >> ~/.zshrc
    echo "export RECIPIENT_EMAIL='$recipient_email'" >> ~/.zshrc

    echo ""
    echo "✅ Environment variables added to ~/.zshrc"
    echo ""
    echo "Run this command to apply them:"
    echo "  source ~/.zshrc"
    echo ""
else
    echo ""
    echo "To set these temporarily for this session, run:"
    echo "  export SENDER_EMAIL='$sender_email'"
    echo "  export SENDER_PASSWORD='$sender_password'"
    echo "  export RECIPIENT_EMAIL='$recipient_email'"
    echo ""
fi

# Test the configuration
echo ""
read -p "Would you like to test the email configuration now? (y/n): " test_now

if [[ $test_now == "y" || $test_now == "Y" ]]; then
    export SENDER_EMAIL="$sender_email"
    export SENDER_PASSWORD="$sender_password"
    export RECIPIENT_EMAIL="$recipient_email"

    echo ""
    echo "Running test..."
    cd /Users/sam.gard/hobbiton-checker
    source venv/bin/activate
    python test_notification.py
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="

