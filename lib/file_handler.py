"""
File I/O operations for reading card lists and writing results.
"""

import sys


def read_card_list(filename):
    """Read card names from input file, one per line."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cards = []
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Remove Moxfield format: "1 Card Name (SET) 123"
                parts = line.split(' ', 1)
                if len(parts) > 1:
                    card_with_set = parts[1]
                else:
                    card_with_set = parts[0]

                # Remove set info in parentheses
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


def write_output(output_file, results, group_by='card'):
    """Write the results to output file."""

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if group_by == 'set':
                _write_grouped_by_set(f, results)
            else:
                _write_grouped_by_card(f, results)

        print(f"\nResults written to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


def _write_grouped_by_set(f, results):
    """Write output grouped by set."""
    from .card_processor import reorganize_by_set

    sets_to_cards = reorganize_by_set(results)

    f.write("=" * 60 + '\n')
    f.write("MTG Set Finder - Results (Grouped by Set)\n")
    f.write("=" * 60 + '\n\n')

    # Sort by set name alphabetically
    sorted_sets = sorted(sets_to_cards.items(), key=lambda x: x[1]['name'])

    for set_code, set_info in sorted_sets:
        f.write(f"\n{set_code} - {set_info['name']}:\n")
        f.write("-" * 60 + "\n")

        for card_name in sorted(set_info['cards']):
            f.write(f"  • {card_name}\n")

        f.write(f"\n  Total: {len(set_info['cards'])} card(s)\n\n")

    f.write("=" * 60 + "\n")
    f.write(f"Total sets found: {len(sets_to_cards)}\n")


def _write_grouped_by_card(f, results):
    """Write output grouped by card."""
    f.write("=" * 60 + '\n')
    f.write("MTG Set Finder - Results (Grouped by Card)\n")
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
