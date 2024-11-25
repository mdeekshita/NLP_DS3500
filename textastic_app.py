

from textastic import Textastic
import textastic_parsers as tp
import pprint as pp

def main():

    tt = Textastic()
    tt.load_text('bbt_script.txt', 'bbt')
    tt.load_text('himym_script.txt', 'himym')
    tt.load_text('modern_family_script', 'modern family')
    tt.load_text('new_girl_script.txt', 'new girl')
    tt.load_text('brooklyn-99.csv', 'Brooklyn-99', parser=tp.csv_parser)

    pp.pprint(tt.data)

    tt.compare_num_words()

if __name__ == '__main__':
    main()