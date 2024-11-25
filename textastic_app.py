

from textastic import Textastic
import textastic_parsers as tp
import pprint as pp

def main():

    tt = Textastic()
    tt.load_text('bbt_script.txt', 'bbt')
    tt.load_text('brooklyn99.txt', 'brooklyn99')
    tt.load_text('friends.txt', 'friends')
    tt.load_text('himym_script.txt', 'himym')
    tt.load_text('modern_family_script', 'modern family')
    tt.load_text('new_girl_script.txt', 'new girl')
    
    tt.load_text('office.txt', 'office')
    tt.load_text('parks_and_rec.txt', 'parks and rec')
    tt.load_text('seinfeld_script.txt', 'seinfeld')
    tt.load_text('the_good_place_script.txt', 'the good place')


    pp.pprint(tt.data)

    tt.compare_num_words()

if __name__ == '__main__':
    main()