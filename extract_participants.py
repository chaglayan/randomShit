#!/usr/bin/env python3
"""
Script to extract participant codes from Slack messages and query the API
to generate a Google Sheets compatible CSV.
"""

import csv
import json
import requests
from datetime import datetime
from typing import Optional

# Participant codes extracted from Slack zh-disabled-users channel (from screenshots)
# Format: (participant_code, date_of_lock, admin_user_id)
SLACK_DATA = [
    ("WRPWUW", "December 2nd", "342473"),
    ("FGL62R", "December 2nd", "556111"),
    ("2UN5P9", "December 3rd", "538496"),
    ("7USW2C", "December 3rd", "579389"),
    ("IO66J3", "December 4th", "152247"),
    ("RGOG4G", "December 5th", "377758"),
    ("X0YZZN", "December 6th", None),  # Link was cut off in screenshot
]

# Base URL for the API (replace with actual URL)
API_BASE_URL = "https://api.zerohash.com"  # Update this with actual {{url}} value

def get_participant_info(participant_code: str, api_key: Optional[str] = None) -> dict:
    """
    Query the API to get participant information.

    Args:
        participant_code: The 6-character participant code
        api_key: Optional API key for authentication

    Returns:
        Dictionary with participant info
    """
    url = f"{API_BASE_URL}/participant/{participant_code}/basic_info"

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("message", data)
    except requests.RequestException as e:
        print(f"Error fetching {participant_code}: {e}")
        return {}

def generate_csv(data: list, output_file: str = "disabled_users.csv"):
    """Generate a CSV file for Google Sheets import."""

    fieldnames = ["Name", "Participant Code", "Admin Link", "Date of Lock", "Status", "Email", "Jurisdiction"]

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            writer.writerow(row)

    print(f"CSV saved to {output_file}")

def main():
    """Main function to process participant codes."""

    print("=" * 60)
    print("Participant Codes Extracted from Slack (zh-disabled-users)")
    print("=" * 60)

    results = []

    for code, date, admin_id in SLACK_DATA:
        admin_link = f"https://onramp-admin.xcoins.com/users/show/{admin_id}" if admin_id else "N/A"

        print(f"\nParticipant: {code}")
        print(f"  Date: {date}")
        print(f"  Admin Link: {admin_link}")
        print(f"  API URL: {API_BASE_URL}/participant/{code}/basic_info")

        # Create row for CSV (without API data - add manually or enable API calls)
        results.append({
            "Name": "",  # Fill in from API response
            "Participant Code": code,
            "Admin Link": admin_link,
            "Date of Lock": date,
            "Status": "",  # Fill in from API response
            "Email": "",  # Fill in from API response
            "Jurisdiction": "",  # Fill in from API response
        })

    # Generate CSV template
    generate_csv(results)

    print("\n" + "=" * 60)
    print("CSV template generated: disabled_users.csv")
    print("=" * 60)

    # Print curl commands for manual API calls
    print("\n\nCURL commands to fetch participant info:")
    print("-" * 60)
    for code, _, _ in SLACK_DATA:
        print(f'curl -X GET "{API_BASE_URL}/participant/{code}/basic_info" -H "Authorization: Bearer $API_KEY"')

    return results

# Pre-filled data from screenshot (FGL62R example)
SAMPLE_API_RESPONSES = {
    "FGL62R": {
        "participant_code": "FGL62R",
        "status": "pending_disable",
        "action": "disable",
        "name": "Jimmy Surles",
        "email": "jimmysurles130@gmail.com",
        "jurisdiction_code": "US-CA",
        "participant_type": "INDIVIDUAL",
        "submission_method": "API",
    }
}

if __name__ == "__main__":
    main()
