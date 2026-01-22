"""
Card data processing logic.
"""

import time
from .scryfall_api import get_card_by_name, get_all_printings


def process_cards(card_names):
    """Process each card and get all sets it's been printed in."""
    all_results = {}

    for i, card_name in enumerate(card_names, 1):
        print(f"[{i}/{len(card_names)}] Processing: {card_name}")

        card_data = get_card_by_name(card_name)
        if not card_data:
            print(f"    Skipping '{card_name}' - not found\n")
            all_results[card_name] = None
            continue

        oracle_id = card_data.get('oracle_id')
        if not oracle_id:
            print(f"    Error: No oracle_id for '{card_name}'\n")
            all_results[card_name] = None
            continue

        time.sleep(0.1)  # Rate limiting for Scryfall
        printings = get_all_printings(oracle_id)

        card_sets = {}
        for printing in printings:
            set_code = printing.get('set', '').upper()
            set_name = printing.get('set_name', '')
            if set_code and set_name:
                card_sets[set_code] = set_name

        print(f"    Found in {len(card_sets)} sets\n")
        all_results[card_name] = card_sets

        time.sleep(0.1)

    return all_results


def reorganize_by_set(results):
    """Reorganize results to group cards by set instead of sets by card."""
    sets_to_cards = {}

    for card_name, sets in results.items():
        if sets is None or not sets:
            continue

        for set_code, set_name in sets.items():
            if set_code not in sets_to_cards:
                sets_to_cards[set_code] = {
                    'name': set_name,
                    'cards': []
                }
            sets_to_cards[set_code]['cards'].append(card_name)

    return sets_to_cards
