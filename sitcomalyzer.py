"""
file: sitcomalyzer.py

Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)
"""

from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# EXCEPTIONS
class SitcomalyzerParsingError(Exception):
    """Exception raised for errors in the Sitcomalyzer framework's parsing."""
    def __init__(self, message):
        super().__init__(message)

class ParsingError(Exception):
    """Raised when a parsing error occurs."""
    pass

class StopWordError(Exception):
    """Raised when an issue with stop words occurs."""
    pass


class Sitcomalyzer:

    def __init__(self):
        """ Constructor

        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set()


    def default_parser(self, filename):

        try:
            with open(filename, 'r') as file:
                text = file.read()
        except FileNotFoundError as e:
            raise SitcomalyzerParsingError(f"File not found: {filename}") from e
        except Exception as e:
            raise SitcomalyzerParsingError(f"An error occurred while parsing the file: {filename}") from e

        try:
            words = text.split()
            clean_words = [word.strip(".,!?;:\"'()[]{}") for word in words]
            clean_words = [word for word in clean_words if word not in self.stop_words]
            clean_words = [word for word in clean_words if not word.isupper()]
        except Exception as e:
            raise ParsingError(f"An error occurred during parsing: {str(e)}")

        lines = text.splitlines()
        sentiment_scores = []

        for i in range(0, len(lines), 30):
            group = " ".join(lines[i:i + 30])
            sentiment = self.analyzer.polarity_scores(group)['compound']
            sentiment_scores.append(sentiment)

        results = {
            'wordcount': Counter(clean_words),  
            'numwords': len(clean_words),
            'sentiment': sentiment_scores
        }
        return results

    def load_stop_words(self, stopwords_file):
        """ Register a document with the framework of a list of stop words to be ignored in loaded files """
        # open and read stopword file, throw exception if fails
        try:
            if stopwords_file:
                with open(stopwords_file, 'r') as file:
                    self.stop_words.update(file.read().splitlines())
            else:
                raise StopWordError("Stopwords file not provided.")
        except FileNotFoundError as e:
            raise StopWordError(f"Stopwords file not found: {e}")
        except Exception as e:
            raise StopWordError(f"Unexpected error while loading stop words: {e}")

    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualizations """
        # parses data with either default parser or other specified one
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        # add label if not specified
        if label is None:
            label = filename

        # label data and load text
        for k, v in results.items():
            self.data[k][label] = v

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Generate a Sankey diagram from text name to word, where the thickness of the
        connection represents the word count of that word in the specified text.
        """
        data = []

        # Prepare the data for the Sankey diagram
        for label, wordcount in self.data['wordcount'].items():
            if word_list:
                words = word_list
            elif k is not None:
                words = [word for word, _ in wordcount.most_common(k)]
            else:
                words = wordcount.keys()

            for word in words:
                if word in wordcount:
                    data.append({'Text': label, 'Word': word, 'Count': wordcount[word]})

        # Create a DataFrame for the Sankey diagram
        df = pd.DataFrame(data)

        # Use the sankey.py functions to create the diagram
        df, labels = self._code_mapping(df, 'Text', 'Word')
        link = {'source': df['Text'], 'target': df['Word'], 'value': df['Count']}

        node = {
            'label': labels,
            'pad': 50,
            'thickness': 50,
            'line': {'color': 'black', 'width': 1}
        }

        # Create and show sankey diagram
        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()

    def _code_mapping(self, df, src, targ):
        """ Map labels in src and targ columns to integers """
        df[src] = df[src].astype(str)
        df[targ] = df[targ].astype(str)

        # Get distinct labels
        labels = sorted(list(set(list(df[src]) + list(df[targ]))))

        # Get integer codes
        lc_map = dict(zip(labels, range(len(labels))))

        # Substitute names for codes in dataframe
        df = df.replace({src: lc_map, targ: lc_map})
        return df, labels

    def compare_sentiment_scores(self):
        """ Generate a  line plot to show the range of sentiment analysis scores
        for each sitcom over a series of lines """
        plt.figure(figsize=(15, 10))
        for label, sentiment_scores in self.data['sentiment'].items():
            plt.plot([i for i in range(len(sentiment_scores))], sentiment_scores, label=label)

        # Add labels and show graph
        plt.title('Sentiment Scores for the Pilot Episode of Sitcoms')
        plt.xlabel('Groups of 30 Lines')
        plt.ylabel('Sentiment Score')
        plt.legend()
        plt.show()

    def sub_plots(self):
        """ Plot top ten words in sitcom episode from wordcount tuples with frequencies"""
        word_count = self.data['wordcount']
        num_shows = len(word_count)
        rows = int(num_shows ** 0.5)
        cols = (num_shows + rows - 1) // rows
        fig, axes = plt.subplots(rows, cols, figsize=(15, 10), squeeze=False)  
        axes = axes.flatten()  

        # create graphs and show
        for idx, (label, counter) in enumerate(word_count.items()):
            top_words = counter.most_common(10)
            ax = axes[idx]  
            ax.bar([word for word, _ in top_words], [count for _, count in top_words])
            ax.set_title(label)
            ax.set_xlabel('Words')
            ax.set_ylabel('Frequency')
            ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()


