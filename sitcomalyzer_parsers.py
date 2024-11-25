"""
file: sitcomalyzer.py

Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)
"""

import json
from collections import Counter
import csv


def json_parser(filename):
    f = open(filename)
    raw = json.load(f)
    text = raw['text']
    words = text.split(" ")
    wc = Counter(words)
    num = len(words)

    return {'wordcount':wc, 'numwords':num}

def csv_parser(filename):

        # Read the CSV file
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                text = []

                # Combine all text from relevant rows/columns (assume first row is a header)
                for row in reader:
                    text.extend(row)  # Add all columns in the row to the text list

            # Join the text content and preprocess
            combined_text = ' '.join(text)
            words = combined_text.split()
            clean_words = [word.lower().strip(".,!?;:\"'()[]{}") for word in words if word.isalpha()]

            # Generate results
            results = {
                'wordcount': Counter(clean_words),
                'numwords': len(clean_words)
            }

            return results



