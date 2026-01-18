#!/usr/bin/env python3
import urllib.request
import json
import time
import sys


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 mtg_set_finder.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Generate output filename
    if input_file.endswith('.txt'):
        output_file = input_file[:-4] + '_common_set.txt'
    else:
        output_file = input_file + '_common_set.txt'

    print(f"Reading cards from: {input_file}")
    print(f"Output will be written to: {output_file}")

    card_names = read_card_list(input_file)
    print(f"Found {len(card_names)} cards to process\n")

    results = process_cards(card_names)

    write_output(output_file, results)

    print(f"Processed {len(card_names)} cards")


def read_card_list(filename):
    """Read card names from input file, one per line."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cards = []
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Remove Moxfield format
                parts = line.split(' ', 1)
                if len(parts) > 1:
                    card_with_set = parts[1]
                else:
                    card_with_set = parts[0]

                if '(' in card_with_set:
                    card_name = card_with_set.split('(')[0].strip()
                else:
                    card_name = card_with_set.strip()

                if card_name:
                    cards.append(card_name)

        return cards
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def get_card_by_name(card_name):
    """Query Scryfall API for a card by exact name."""
    url = f"https://api.scryfall.com/cards/named?exact={
        urllib.parse.quote(card_name)}"

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
    """Get all printing of a card using its oracle_id."""
    url = f"https://api.scryfall.com/cards/search?q=oracleid:{
        oracle_id}&unique=prints"

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


def write_output(output_file, results):
    """Write the results to output file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + '\n')
            f.write("MTG Set Finder - Results\n")
            f.write("=" * 60 + '\n')

            for card_name, sets in results.items():
                f.write(f"\n{card_name}:\n")
                f.write("-" * 60 + "\n")

                if sets is None:
                    f.write("   Card not found\n")
                elif sets:
                    for set_code in sorted(sets.keys()):
                        f.write(f"  {set_code} - {sets[set_code]}\n")
                    f.write(f"\n    Total: {len(sets)} set(s)\n")
                else:
                    f.write("   No sets found\n")

                f.write("\n")
        print(f"\nResults written to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
