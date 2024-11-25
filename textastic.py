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
<<<<<<< HEAD

    
    #once we have files in this delete the above default_parser and use this one so that it actually reads through txt files: 
    def default_parser(seld, filename):
=======
    
    #once we have files in this delete the above default_parser and use this one so that it actually reads through txt files: 
    def default_parser(self, filename):
>>>>>>> 48f3b128751e6247191c5524f495a6224f960239


        with open(filename, mode='r') as file:
            text = file.read()
        
        words = text.split()
        clean_words = [word.strip(".,!?;:\"'()[]{}") for word in words]


        results = {
            'wordcount': Counter(clean_words),  
            'numwords': len(clean_words),   
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
