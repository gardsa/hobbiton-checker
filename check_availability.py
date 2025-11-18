#!/usr/bin/env python3
"""
Hobbiton Booking Availability Checker
Monitors the Hobbiton Movie Set Tour booking page for available slots
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import logging
import os
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hobbiton_checker.log'),
        logging.StreamHandler()
    ]
)

# Email configuration (set these in environment variables or update directly)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'your-app-password')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'your-email@gmail.com')

# Dates to check
DATES_TO_CHECK = ['17-12-2025', '18-12-2025', '19-12-2025']  # December dates to monitor

# All Hobbiton tour categories to monitor
TOUR_CATEGORIES = {
    'EXMFFBR': 'Hobbiton Tour 1',
    'EXTSRBR': 'Extended The Shire\'s Rest Breakfast',
    'EXMTABR': 'Hobbiton Tour 2',
    'EXBTS': 'Hobbiton Tour 3',
    'BANQUETBR': 'Banquet Tour',
    'EXSBTBR': 'Hobbiton Tour 4'
}

BASE_URL = 'https://bookings.hobbitontours.com/BookingCat/Availability/?Date={}&Category={}&GroupSize=2'

# Track previously notified slots to avoid duplicate notifications
notified_slots = set()


def check_availability(date: str, category: str, category_name: str) -> List[Dict[str, str]]:
    """
    Check availability for a specific date and tour category
    Returns list of available slots with time and status
    """
    url = BASE_URL.format(date, category)
    available_slots = []

    try:
        logging.info(f"Checking {category} ({category_name}) for {date}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Convert date format from DD-MM-YYYY to DD/MM/YYYY for matching
        date_parts = date.split('-')
        formatted_date = f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]}"

        # Find all booking cells for this specific date
        booking_cells = soup.find_all('div', {'mydate': formatted_date})

        for cell in booking_cells:
            status_text = cell.get_text(strip=True)

            # Check if this slot is bookable (contains BOOK but not "Fully Booked" or "Bookings Closed")
            if 'BOOK' in status_text and 'Fully Booked' not in status_text and 'Bookings Closed' not in status_text:
                # Find the departure time by looking for the parent row's title
                parent_row = cell.find_parent('div', class_='cl_availability-table__row')
                if parent_row:
                    title_div = parent_row.find('div', class_='cl_availability-product__title')
                    if title_div:
                        time_text = title_div.get_text(strip=True)

                        # Clean up status text
                        if status_text == 'BOOK':
                            status = 'BOOK'
                        elif 'Limited' in status_text:
                            status = 'BOOK - Limited seats'
                        else:
                            status = status_text

                        available_slots.append({
                            'date': date,
                            'category': category,
                            'category_name': category_name,
                            'time': time_text,
                            'status': status,
                            'url': url
                        })
                        logging.info(f"Found available slot: {category_name} on {date} at {time_text} - {status}")

        if not available_slots:
            logging.debug(f"No available slots for {category} on {date}")

    except requests.RequestException as e:
        logging.error(f"Error checking {category} on {date}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error checking {category} on {date}: {e}")

    return available_slots


def send_email_notification(available_slots: List[Dict[str, str]]):
    """
    Send email notification about available slots
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🎉 Hobbiton Tour Slots Available!'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        # Create email body
        text_body = "Available Hobbiton Movie Set Tour slots found!\n\n"
        html_body = """
        <html>
        <body>
            <h2>🎉 Hobbiton Movie Set Tour - Available Slots Found!</h2>
            <p>Great news! The following booking slots are now available:</p>
            <ul>
        """

        for slot in available_slots:
            text_body += f"• {slot['category_name']} ({slot['category']})\n"
            text_body += f"  {slot['date']} at {slot['time']} - {slot['status']}\n"
            text_body += f"  Book here: {slot['url']}\n\n"

            html_body += f"""
            <li>
                <strong>{slot['category_name']}</strong> ({slot['category']})<br>
                <strong>{slot['date']}</strong> at <strong>{slot['time']}</strong> - {slot['status']}<br>
                <a href="{slot['url']}">Book Now</a>
            </li>
            """

        html_body += """
            </ul>
            <p>Book quickly before slots fill up!</p>
            <p><em>This is an automated notification from your Hobbiton booking checker.</em></p>
        </body>
        </html>
        """

        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        logging.info(f"Email notification sent successfully to {RECIPIENT_EMAIL}")

    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")


def send_desktop_notification(available_slots: List[Dict[str, str]]):
    """
    Send desktop notification (macOS/Linux/Windows compatible)
    Uses alert dialogs on macOS for better visibility
    """
    try:
        # Build simple message
        slot_count = len(available_slots)

        # Create a simple list of slots
        slot_list = []
        for i, slot in enumerate(available_slots[:5]):  # Show first 5
            slot_list.append(f"{slot['time']} - {slot['category_name']}")

        if slot_count > 5:
            slot_list.append(f"...and {slot_count - 5} more slots")

        message = " | ".join(slot_list)

        # Try macOS alert dialog (more visible than banner notifications)
        if os.system('which osascript > /dev/null 2>&1') == 0:
            # Use simple AppleScript without complex escaping
            import subprocess
            script = f'''
            display alert "🎉 Found {slot_count} Hobbiton Tour Slot(s)!" message "{message}" buttons {{"View Logs", "OK"}} default button "OK" giving up after 30
            '''
            try:
                subprocess.run(['osascript', '-e', script], check=False, capture_output=True)
            except:
                # Fallback to simpler alert
                subprocess.run(['osascript', '-e', f'display alert "Hobbiton Tours Available!" message "Found {slot_count} available slots! Check the logs for details."'], check=False)
        # Try Linux notification
        elif os.system('which notify-send > /dev/null 2>&1') == 0:
            os.system(f'notify-send "Hobbiton Booking Available!" "Found {slot_count} available slots"')
        # Try Windows notification
        elif os.name == 'nt':
            try:
                from plyer import notification
                notification.notify(
                    title='Hobbiton Booking Available!',
                    message=f"Found {slot_count} available slots",
                    timeout=10
                )
            except ImportError:
                logging.warning("Desktop notifications not available on Windows (install 'plyer')")

        logging.info("Desktop notification sent")
    except Exception as e:
        logging.error(f"Failed to send desktop notification: {e}")


def check_all_dates():
    """
    Check all configured dates and tour categories for availability
    """
    logging.info("=" * 60)
    logging.info(f"Starting availability check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Checking {len(TOUR_CATEGORIES)} tour categories across {len(DATES_TO_CHECK)} dates")

    all_available_slots = []

    for category, category_name in TOUR_CATEGORIES.items():
        for date in DATES_TO_CHECK:
            slots = check_availability(date, category, category_name)
            all_available_slots.extend(slots)
            time.sleep(1)  # Be nice to the server

    # Filter out slots we've already notified about
    new_slots = [slot for slot in all_available_slots
                 if f"{slot['category']}_{slot['date']}_{slot['time']}" not in notified_slots]

    if new_slots:
        logging.info(f"Found {len(new_slots)} new available slot(s)!")

        # Send notifications
        send_desktop_notification(new_slots)
        send_email_notification(new_slots)

        # Mark as notified
        for slot in new_slots:
            notified_slots.add(f"{slot['category']}_{slot['date']}_{slot['time']}")
    else:
        if all_available_slots:
            logging.info("Available slots found but already notified")
        else:
            logging.info("No available slots found across all tours")

    logging.info("Check completed")
    logging.info("=" * 60)


def run_scheduler():
    """
    Run the checker every hour
    """
    import schedule

    logging.info("Hobbiton Booking Checker started")
    logging.info(f"Monitoring {len(TOUR_CATEGORIES)} tour categories:")
    for cat, name in TOUR_CATEGORIES.items():
        logging.info(f"  - {cat}: {name}")
    logging.info(f"Monitoring dates: {', '.join(DATES_TO_CHECK)}")
    logging.info("Checking every hour...")

    # Run immediately on start
    check_all_dates()

    # Schedule to run every hour
    schedule.every().hour.do(check_all_dates)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute if it's time to run


if __name__ == "__main__":
    # Check if email is configured
    if SENDER_EMAIL == 'your-email@gmail.com':
        logging.warning("⚠️  Email not configured! Please set environment variables.")
        logging.warning("Set SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL")
        logging.warning("Desktop notifications will still work if available.")
        print("\n" + "="*60)
        print("SETUP REQUIRED:")
        print("="*60)
        print("Email notifications are not configured.")
        print("\nTo enable email notifications, set these environment variables:")
        print("  export SENDER_EMAIL='your-email@gmail.com'")
        print("  export SENDER_PASSWORD='your-app-password'")
        print("  export RECIPIENT_EMAIL='recipient@gmail.com'")
        print("\nFor Gmail, you'll need to create an 'App Password':")
        print("  https://support.google.com/accounts/answer/185833")
        print("\nPress Ctrl+C to exit or wait 10 seconds to continue anyway...")
        print("="*60 + "\n")
        time.sleep(10)

    try:
        run_scheduler()
    except KeyboardInterrupt:
        logging.info("\nChecker stopped by user")

