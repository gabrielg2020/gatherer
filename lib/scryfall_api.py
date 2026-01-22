"""
Scryfall API client for querying Magic: The Gathering card data.
"""

import urllib.request
import urllib.parse
import json

BASE_URL = "https://api.scryfall.com/cards"


def get_card_by_name(card_name):
    """Query Scryfall API for a card by exact name."""
    encoded_name = urllib.parse.quote(card_name)
    url = f"{BASE_URL}/named?exact={encoded_name}"

    headers = {
        'User-Agent': 'MTGSetFinder/1.0',
        'Accept': 'application/json'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"   Warning: Card '{card_name}' not found")
            return None
        else:
            print(f"    HTTP Error {e.code} for '{card_name}'")
            return None
    except Exception as e:
        print(f"    Error fetching '{card_name}': {e}")
        return None


def get_all_printings(oracle_id):
    """Get all printings of a card using its oracle_id."""
    url = f"{BASE_URL}/search?q=oracleid:{oracle_id}&unique=prints"

    headers = {
        'User-Agent': 'MTGSetFinder/1.0',
        'Accept': 'application/json'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('data', [])
    except Exception as e:
        print(f"    Error fetching printings: {e}")
        return []
