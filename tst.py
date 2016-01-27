import socket
from unidecode import unidecode
import codecs
import unicodecsv as csv

FROG_HOST="localhost"
FROG_PORT=8080

def call_frog(text):
    """
    Call the frog parser on the given host and port with the given text
    Returns a file object containing the output lines.
    """

    print("call frog")
    print(text)

    if not text.endswith("\n"):
        text = text + "\n"
    # if not isinstance(text, unicode):
    #     text = unicode(text)
    text = unidecode(text).encode("utf-8")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("connect %s %i"%(FROG_HOST, FROG_PORT))
    s.connect((FROG_HOST, FROG_PORT))
    print("connected")
    s.sendall(text)
    s.shutdown(socket.SHUT_WR)
    print("got results")
    for line in s.makefile('r'):
        line = line.strip('\n')
        if line == "READY":
            return
        else:
            yield line

def parse_frog(lines):
    """
    Interpret the output of the frog parser.
    Input should be a sequence of lines (i.e. the output of call_frog)
    Result is a sequence of dicts representing the tokens
    """
    sid = 0
    for i, l in enumerate(lines):
        if not l:
            # end of sentence marker
            sid += 1
        else:
            print(l.strip())
            parts = l.split("\t")
            tid, token, lemma, morph, pos, conf, ne, _, parent, rel = parts
            if rel:
                rel = (rel, int(parent) - 1)
            r = dict(id=i, sentence=sid, word=token, lemma=lemma,
                     pos=pos, pos_confidence=float(conf),
                     rel=rel)
            if ne != 'O':
                r["ne"] = ne.split('_', 1)[0][2:]   # NER label from BIO tags
            yield r


if __name__ == "__main__":
    with codecs.open("fake_data_904_raw.txt",encoding='utf-8') as infile:
        with open("fake_data_904_output.txt","wb") as outfile:
            writer = csv.writer(outfile,encoding='utf-8',delimiter="|")
            for line in infile:
                print(line)
                x = call_frog(line)
                print(type(x))
                for result in parse_frog(x):
                    for key, value in result.items():
                        writer.writerow([key,value])

#     lines = ["Hij vertelt in het ziekenhuis te zijn in Amsterdam, en de provincie is 'diep in het station'.",
# "info gekregen over BSN nummer en contactpersonen: BSN pte 123138877, contactpersonen broer en echtgenoot.",
# "Adres: Oranje nassau str 40, 6431 KX, Everdam tel. 06-13973882    PO/  Ik zie een 18 jarige obese vrouw conform kalenderleeftijd met piercings in haar neus en lip.",
# "From: Erik Mastem erikmastem12@hotmail.com   Sent: dinsdag 4 oktober 2011 13:53  To: Mast, R.C. (PSY)  Subject: 1,4  Beste dokter Mast,  Mijn spiegel was gisteren 1,4.",
# "Vanaf 5 maart 2013 zagen wij enkele keren uw patient, dhr. Z. van der Made, geboren 14-12-1971, op onze polikliniek urologie van het Leids Universitair Medisch Centrum.",
# "Voor die tijd was 'Ferdinand niet Ferdinand'.",
# "Naam : Y.F. v Zetten  Geboortedatum: 9-07-1995 BSN : 128138577  Geslacht : V  Materiaal : Urine (ontvangen op 30-03-2011)  Indicatie : Verstandelijke of lichamelijke ontwikkelingsstoornis",
# "RvK 2nd opinion vanuit Nijmegen    Voorgeschiedenis  aug 2009 M Graves  2006 maagzweer    Medicatie  Soms nexium",
# "liesoperatie, knieoperatie  Dementie, woont op psychogeriatrische afdeling van v Elzenstraat.",
# "Hartelijke groeten,  Erik en Martha Evers  kastanjelaan 34  1287PK Amsterdam",
# "Haar man Peter is zondag 23-12-2014 overleden.",
# "Toestemmingsformulier voor MCm ontvangen: Archief telefonisch niet bereikbaar, informatie per email opgevraagd (kvanboom@home.nl)",
# "HAP belt over pt (Dr. Ekenhof 020 1503364)."
#     ]

#     # for line in ["zin nummer 1 probeer.", "Hij vertelt in het ziekenhuis te zijn in Amsterdam, en de provincie is 'diep in het station'."]:
#     for line in lines:
#         for result in parse_frog(call_frog(line)):
#             for key, value in result.items():
#                 print((key,value))


