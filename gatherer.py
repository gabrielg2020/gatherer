#!/usr/bin/env python3
"""
Gatherer - MTG Set Finder
Find all sets where Magic: The Gathering cards have been printed.
"""

import argparse
from lib.file_handler import read_card_list, write_output
from lib.card_processor import process_cards


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Find all sets where MTG cards have been printed'
    )
    parser.add_argument('input_file', help='Input file with card list')
    parser.add_argument(
        '--group-by',
        choices=['card', 'set'],
        default='card',
        help='Group results by card or set (default: card)'
    )

    args = parser.parse_args()
    input_file = args.input_file
    group_by = args.group_by

    # Generate output filename
    if input_file.endswith('.txt'):
        output_file = input_file[:-4] + '_common_set.txt'
    else:
        output_file = input_file + '_common_set.txt'

    print(f"Reading cards from: {input_file}")
    print(f"Output will be written to: {output_file}")
    print(f"Grouping by: {group_by}\n")

    # Read card list from file
    card_names = read_card_list(input_file)
    print(f"Found {len(card_names)} cards to process\n")

    # Process cards via Scryfall API
    results = process_cards(card_names)

    # Write results to output file
    write_output(output_file, results, group_by)

    print(f"Processed {len(card_names)} cards")


if __name__ == "__main__":
    main()
