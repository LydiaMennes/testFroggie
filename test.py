import nltk.data
import frog
import codecs

sent_detector = nltk.data.load('tokenizers/punkt/dutch.pickle')
froggie = frog.Frog(frog.FrogOptions(parser=False), "/etc/frog/frog.cfg")
counter = 1

with codecs.open("results.csv","w","utf-8") as of:
	with codecs.open("input.txt","r","utf-8") as infile:
		for text in infile:
			of.write("text %i"%counter)
			sentences = sent_detector.tokenize(text.strip())
			for s in sentences:
				of.write(s+"\n")
			for s in sentences:
				of.write(froggie.process_raw(s))
			counter+=1
