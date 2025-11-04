#!/usr/bin/env python3
"""Fetch power cut data from UK Power Networks."""

import curl_cffi
import json
import sys

# Create a session to maintain cookies and connection pooling
session = curl_cffi.Session()

try:
    # First request to the main power cut list page to establish session
    response1 = session.get(
        'https://www.ukpowernetworks.co.uk/power-cut/list',
        timeout=10,
        impersonate="chrome"
    )
    response1.raise_for_status()

    # Second request to the API endpoint for incident data
    response2 = session.get(
        'https://www.ukpowernetworks.co.uk/api/power-cut/all-incidents-light',
        timeout=10,
        impersonate="chrome"
    )
    response2.raise_for_status()

    # Parse and print the JSON data
    data = response2.json()
    json.dump(data, sys.stdout, indent=2)

except curl_cffi.exceptions.RequestException as e:
    print(f"Error fetching data: {e}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}", file=sys.stderr)
    sys.exit(1)
