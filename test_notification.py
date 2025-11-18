#!/usr/bin/env python3
"""
Test script to verify email notifications are working
"""

import os
import sys

# Import the notification function from the main script
from check_availability import send_email_notification, send_desktop_notification

# Create test slots for different tour categories
test_slots = [
    {
        'date': '17-12-2025',
        'category': 'EXTSRBR',
        'category_name': 'Extended The Shire\'s Rest Breakfast',
        'time': 'Shires Rest 9.10am Departure',
        'status': 'BOOK',
        'url': 'https://bookings.hobbitontours.com/BookingCat/Availability/?Date=17-12-2025&Category=EXTSRBR&GroupSize=2'
    },
    {
        'date': '18-12-2025',
        'category': 'BANQUETBR',
        'category_name': 'Banquet Tour',
        'time': 'Shires Rest 11.30am Departure',
        'status': 'Limited seats available',
        'url': 'https://bookings.hobbitontours.com/BookingCat/Availability/?Date=18-12-2025&Category=BANQUETBR&GroupSize=2'
    }
]

print("Testing notifications...")
print("-" * 60)

# Test desktop notification
print("\n1. Testing desktop notification...")
try:
    send_desktop_notification(test_slots)
    print("✅ Desktop notification sent (check your notifications)")
except Exception as e:
    print(f"❌ Desktop notification failed: {e}")

# Test email notification
print("\n2. Testing email notification...")
sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')

if sender_email == 'your-email@gmail.com':
    print("⚠️  Email not configured!")
    print("\nPlease set environment variables:")
    print("  export SENDER_EMAIL='your-email@gmail.com'")
    print("  export SENDER_PASSWORD='your-app-password'")
    print("  export RECIPIENT_EMAIL='your-email@gmail.com'")
    print("\nThen run this test again.")
    sys.exit(1)

try:
    send_email_notification(test_slots)
    print(f"✅ Email notification sent to {os.getenv('RECIPIENT_EMAIL')}")
    print("   Check your inbox (and spam folder)")
except Exception as e:
    print(f"❌ Email notification failed: {e}")
    print("\nCommon issues:")
    print("  - Wrong password (use App Password for Gmail)")
    print("  - 2-Step Verification not enabled (required for Gmail)")
    print("  - Wrong SMTP server/port")

print("\n" + "-" * 60)
print("Test completed!")

