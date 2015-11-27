import nltk.data
import frog
import codecs

text = "CARDIALE VOORGESCHIEDENIS: 1991 myocardinfarct, onderwand. 23-09-2009: ventriculaire tachycardie bij slechte linkerventrikelfunctie en oud infarct, nu geen coronair lijden, op 15-10-2009 implantatie van profylactische 1 kamer ICD. CARDIALE VOORGESCHIEDENIS: 1991 myocardinfarct, onderwand. 23-09-2009: ventriculaire tachycardie bij slechte linkerventrikelfunctie en oud infarct, nu geen coronair lijden, op 15-10-2009 implantatie van (therapeutisch) 1 kamer ICD. Reden van polikliniekbezoek: Familiaire hypercholesterolemie met status na myocardinfarct. 1991: Myocardinfarct op 48-jarige leeftijd bij roken, overgewicht en Familiaire hypercholesterolemie met ernstig belaste familie-anamnese: vader, moeder, twee zussen en een broer overleden allen op een leeftijd van 47-49 jaar aan een myocard infarct en hadden, waar bekend, ook sterk verhoogd cholesterol met ook xanthelasmata arcus lipoïdes en waarschijnlijk xanthomen."

sent_detector = nltk.data.load('tokenizers/punkt/dutch.pickle')
froggie = frog.Frog(frog.FrogOptions(parser=False), "/etc/frog/frog.cfg")

with codecs.open("results.txt","w","utf-8") as of:
	for s in sent_detector.tokenize(text.strip()):
		of.write(froggie.process_raw(s))
