#!/usr/bin/env python3
"""
Test all category codes to find which tours have availability
"""

import requests
from bs4 import BeautifulSoup
import time

# All category codes from the Hobbiton website
CATEGORIES = {
    'EXMFFBR': 'Unknown Tour 1',
    'EXTSRBR': 'Extended The Shire\'s Rest Breakfast',
    'EXMTABR': 'Unknown Tour 2',
    'EXBTS': 'Unknown Tour 3',
    'BANQUETBR': 'Banquet Tour',
    'EXSBTBR': 'Unknown Tour 4'
}

DATES_TO_CHECK = ['17-12-2025', '18-12-2025', '19-12-2025']
BASE_URL = 'https://bookings.hobbitontours.com/BookingCat/Availability/?Date={}&Category={}&GroupSize=2'

def check_availability(date: str, category: str):
    """Check availability for a specific date and category"""
    url = BASE_URL.format(date, category)
    available_slots = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all table rows with departure times
        rows = soup.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if not cells:
                continue

            # First cell typically contains the departure time
            time_cell = cells[0]
            time_text = time_cell.get_text(strip=True)

            # Check other cells for "BOOK" button/text
            for cell in cells[1:]:
                cell_text = cell.get_text(strip=True)

                # Look for "BOOK" that's not part of "Fully Booked" or "Bookings Closed"
                if 'BOOK' in cell_text and 'Fully Booked' not in cell_text and 'Bookings Closed' not in cell_text:
                    # Check if it's a clickable booking option
                    if cell.find('a') or 'Limited seats' in cell_text or cell_text == 'BOOK':
                        available_slots.append({
                            'time': time_text,
                            'status': cell_text
                        })
                        break

    except Exception as e:
        print(f"    ⚠️  Error checking {category} for {date}: {e}")

    return available_slots

def main():
    print("=" * 80)
    print("TESTING ALL HOBBITON TOUR CATEGORIES FOR AVAILABILITY")
    print("=" * 80)
    print(f"\nDates being checked: {', '.join(DATES_TO_CHECK)}")
    print(f"Group size: 2 people")
    print("\n" + "=" * 80)

    results = {}

    for category, description in CATEGORIES.items():
        print(f"\n🔍 Checking {category} ({description})...")
        print("-" * 80)

        category_results = {}
        has_availability = False

        for date in DATES_TO_CHECK:
            slots = check_availability(date, category)
            category_results[date] = slots

            if slots:
                has_availability = True
                print(f"  ✅ {date}: {len(slots)} slot(s) available!")
                for slot in slots:
                    print(f"     → {slot['time']} - {slot['status']}")
            else:
                print(f"  ❌ {date}: No availability")

            time.sleep(1)  # Be nice to the server

        results[category] = {
            'description': description,
            'has_availability': has_availability,
            'slots': category_results
        }

        if has_availability:
            print(f"\n  🎉 AVAILABILITY FOUND FOR {category}!")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    categories_with_availability = []

    for category, data in results.items():
        if data['has_availability']:
            categories_with_availability.append(category)
            total_slots = sum(len(slots) for slots in data['slots'].values())
            print(f"✅ {category}: {total_slots} total slot(s) available")
        else:
            print(f"❌ {category}: No availability")

    if categories_with_availability:
        print("\n" + "=" * 80)
        print("🎯 RECOMMENDATION")
        print("=" * 80)
        print("\nThe following tour categories have availability:")
        for cat in categories_with_availability:
            print(f"  • {cat} - {CATEGORIES[cat]}")
        print("\nUpdate check_availability.py to use one of these category codes!")
    else:
        print("\n😔 No availability found on any tour for the checked dates.")
        print("   Try checking different dates or check back later!")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

