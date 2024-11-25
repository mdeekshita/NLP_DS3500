"""
file: sitcomalyzer.py

Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)
"""

from sitcomalyzer import Sitcomalyzer
import sitcomalyzer_parsers as tp
import pprint as pp

def main():

    sca = Sitcomalyzer()
    sca.load_stop_words("stopwords.txt")
    sca.load_text('bbt_script.txt', 'big bang theory')
    sca.load_text('brooklyn99.txt', 'brooklyn99')
    sca.load_text('friends.txt', 'friends')
    sca.load_text('himym_script.txt', 'himym')
    sca.load_text('modern_family_script.txt', 'modern family')
    sca.load_text('new_girl_script.txt', 'new girl')
    sca.load_text('office.txt', 'office')
    sca.load_text('parks_and_rec.text', 'parks and rec')
    sca.load_text('seinfeld_script.txt', 'seinfeld')
    sca.load_text('the_good_place_script.txt', 'the good place')


    pp.pprint(sca.data)
    sca.compare_sentiment_scores()
    sca.sub_plots()
    sca.wordcount_sankey()

if __name__ == '__main__':
    main()