"""

file: textastic.py

Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)

Possible sources for your mini-project

- gutenburg texts
- political speech
- tweet compilations
- corporate filings
- philosophy treatises
- letters, journals, diaries
- blogs
- news articles


The core data structure:

Input: "A" --> raw text,  "B" --> another text

Extract wordcounts:
        "A" --> wordcounts_A,   "B" --> wordcounts_B, ......

What get stored:

        "wordcounts"  --->   {"A" --> wordcounts_A,
                              "B" --> wordcounts_B, etc.}

        e.g., dict[wordcounts][A] --> wordcounts_A



"""


from collections import defaultdict, Counter
import random as rnd
import matplotlib.pyplot as plt

class Textastic:

    def __init__(self):
        """ Constructor

        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)

    def default_parser(self, filename):
        """ Parse a standard text file and produce
        extract data results in the form of a dictionary. """

        results = {
            'wordcount': Counter("To be or not to be".split(" ")),
            'numwords' : rnd.randrange(10, 1000)
        }

        return results
    
    def csv_parser(self, filename):

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


    def load_stop_words(self, stopwords_file):
        if stopwords_file:
            with open(stopwords_file, 'r') as file:
                self.stop_words.update(file.read().splitlines())
        print(f"Stop words loaded: {len(self.stop_words)} words.")


    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualizations """
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def compare_num_words(self):
        """ This is a very simplistic visualization that creates
        a bar chart comparing number of words.   (Not intended
        for your project.)  """

        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()
