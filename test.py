import nltk.data
import frog
import codecs
import docopt

Usage:
    sample_file_builder <input_file> <output_file>


sent_detector = nltk.data.load('tokenizers/punkt/dutch.pickle')
froggie = frog.Frog(frog.FrogOptions(parser=False), "/etc/frog/frog.cfg")
# counter = 1

with codecs.open(output_file,"w","utf-8") as of:
    with codecs.open(input_file,"r","utf-8") as infile:
        for line in infile:
            of.write(froggie.process_raw(s)+"\n")
            # counter+=1
