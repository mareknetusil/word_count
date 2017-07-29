__author__ = "Marek Netusil"
# -*- coding: cp1250 -*-
NUMBERS = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
DELIMITERS = set(['.', '=', ',', ';', '"', '\n', '\eof', '\eol', '(', ')', '?'])
SPLIT = ' |, |,|\n|\. |; |\.\n|,\n|"|/|\eof|\eol|$'

import argparse
import re
import io
import operator

parser = argparse.ArgumentParser()
parser.add_argument("files", help="Vstupni soubory", nargs='+')
parser.add_argument("-a", "--abc", help="Zeradit abecedne", action="store_true")

args = parser.parse_args()

def word_refine(word):
    while word <> '':
        if word[0] in DELIMITERS:
            word = word[1:]
        elif word[-1] in DELIMITERS:
            word = word[:len(word)-1]
        else:
            return word
    return word

def word_valid(word):
    return set(word).intersection(NUMBERS | DELIMITERS) == set()

def save(out, file):
    with io.open(file, 'w', encoding='utf8') as file_out:
        if isinstance(out, dict):
            for key, value in out.iteritems():
                file_out.write(key + ": " + str(value) + '\n')
        elif isinstance(out, set):
            for key in out:
                file_out.write(key + '\n')
        elif isinstance(out, list):
            if isinstance(out[0], tuple):
                for key, value in out:
                    file_out.write(key + ": " + str(value) + '\n')
            else:
                for value in out:
                    file_out.write(str(value) + '\n')


words_dict = {}
words_discarted = set()
bad_ones = []
good_ones = []
for file_name in args.files:
    with io.open(file_name, 'r', encoding='cp1250') as f_in:
        #import pdb; pdb.set_trace()
        try:
            for line in f_in:
                words = [word.lower() for word in \
                        re.split(SPLIT, line)]
                for word in words:
                    word = word_refine(word)
                    if word_valid(word) and word <> '':
                        if word in words_dict.keys():
                            words_dict[word] += 1
                        else:
                            words_dict[word] = 1
                    elif word <> '':
                        words_discarted.add(word)
            good_ones.append(f_in.name)
        except:
            print 'poser u ' + f_in.name
            bad_ones.append(f_in.name)

save(sorted(words_dict.items(),
        key=operator.itemgetter(not args.abc), reverse= not args.abc),
     'word_count_output')
save(words_discarted, 'word_count_output_garbage')

if bad_ones:
    f_out = open('bad_ones','w')
    for value in bad_ones:
        f_out.write(value + '\n')
    f_out.close()

if good_ones:
    f_out = open('good_ones', 'w')
    for value in good_ones:
        f_out.write(value + '\n')
    f_out.close()
