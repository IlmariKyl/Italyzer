from wordsuggester import WordSuggester
import hfst, libhfst, sys, translator

def LoadTransducer():
    try:
        istr = libhfst.HfstInputStream(r"italian_verb_analyzer.hfst")
        transducers = []

        while not (istr.is_eof()):
            transducers.append(istr.read())
        istr.close()
        td = hfst.HfstBasicTransducer(transducers[1])
        
        return td
    
    except:
        print('Transducer file was not found or invalid.')
        sys.exit()

def main():
    epsilon = '@_EPSILON_SYMBOL_@'
    wordsuggester = WordSuggester()
    td = LoadTransducer()
    
    while True:        
        usinput = input('Input a verb form: ')
        print()
        
        if usinput == '':
            break
        if len(td.lookup(usinput)) == 0 or not wordsuggester.word_in_lexicon(usinput):
            print('Verb form not found.')
            
            # Check if any suggestions, longer than 2 characters, are found
            if len(wordsuggester.suggestions(usinput)) > 1 and len(usinput) > 2:
                options = []
                print('\nDid you mean:')

                # Lists suggestions
                for count, form in enumerate(wordsuggester.suggestions(usinput)):
                    if count < 10:
                        options.append((count+1, form))
                        print('{:2d}) {}'.format(count+1, form))

                choose = input('\nEnter a number or press enter to continue: ')

                for option in sorted(options):
                    if str(choose) == str(option[0]):
                        for form_list in td.lookup(option[1]).values():
                            print()
                            for  form in form_list:
                                print(form[0].replace(epsilon, ''), '  -  ', translator.translate(form[0].split('+')[1]))
                            print()
                            break
        else:
            # Outputs analyses
            for form_list in td.lookup(usinput).values():
                for  form in form_list:
                    print(form[0].replace(epsilon, '') , '  -  ', translator.translate(form[0].split('+')[1]))


main()
            

    
