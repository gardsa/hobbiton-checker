#!/usr/bin/env python3
"""
Quick one-time availability check (doesn't run continuously)
Useful for testing the checker without running it as a service
"""

import sys
from check_availability import check_all_dates, DATES_TO_CHECK, TOUR_CATEGORIES
import logging

# Configure logging to show in console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

if __name__ == "__main__":
    print("=" * 70)
    print("Hobbiton Booking Availability - Quick Check")
    print("=" * 70)
    print(f"\nMonitoring {len(TOUR_CATEGORIES)} tour categories:")
    for cat, name in TOUR_CATEGORIES.items():
        print(f"  • {cat}: {name}")
    print(f"\nChecking dates: {', '.join(DATES_TO_CHECK)}")
    print("\nThis will check once and exit (won't run continuously)")
    print("=" * 70)
    print()

    try:
        check_all_dates()
        print()
        print("=" * 70)
        print("✅ Check completed! See results above.")
        print("=" * 70)
        print()
        print("To run continuously (checking every hour):")
        print("  python check_availability.py")
        print()
    except KeyboardInterrupt:
        print("\n\nCheck cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

