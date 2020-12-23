import sys
import random
import PySimpleGUI as sg

MALE = ["trottel", "clown","kürbis", "inzüchtler", "juckreiz", "idiot", "bolzen","ausfall","cretin", "zwitter", "niemand","zyste", "befruchter","virus", "yeti", "oger", "molch", "penner", "wurm", "zyklop", "meister", "bär", "knecht", "knilch", "fehler", "zwerg", "nazi", "kopf", "kobold",  "hoden", "popper", "sack", "nippel", "sohn", "hamster", "bastard", "degenerate",
        "fetischist", "prophet"," wichser", "wichskopf", "fürst", "schniedel", "opfer", "pisser", "unfall", "dübel", "saurier", "lumpe", " ohne Daseinsberechtigung", "ficker", "schmutz", "affe", "fehlfick", "lecker", "reiter", "blasebalg"]
FEMALE = ["xantippe","qualle","rosette","lücke", "laus", "fotze", "zyste", "", "hure", "geige", "missgeburt", "stute", "ratte", "geburt", "", "bitch", "kacke",
          "tochter", "fresse",  "abart", "raupe", "rosine", "bestie", "schlampe", "nutte", "sonde", "verschwendung", ]
OTHER = ["schwein", "ferkel", "gesicht", "etwas", "urin", "unkraut",
         "kind", "experiment", "tier", "loch", "luder", "yak", "viech"]
DESSERTS = ["Xylophon","Corona","Jugo","Quer","Warzen","Jammer","Lust", "Lutsch", "Labber","Total", "Tumor", "Turnschuh", "Todes","Dinkel", "Chromosom", "Ochsen", "Müll", "Voll", "Vollkorn", "Mastdarm", "Kotz", "Insel", "Inzest", "Hack", "Gollum", "Gondor", "Pimmel", "Kack", "Keller", "Huren", "Dorf", "Feld", "Feld", "Hunde", "Toiletten", "Eichel",
            "Kanal", "Kampf", "Hoden","Yeti", "Zitronen", "Sack", "Fotzen", "Arsch", "Vorhaut", "Rosen", "", "Nippel", "Reste", "Abfall", "Fehl", "Anal", "Bildungs", "Unfall", "Cyber", "", "Kleinhirn", "Schweine"]
ADJECTIVES = ["quängelnde", "wissentliche","yetifickende","zweitrangige","x-beinige", "judenfeindliche", "tittenlose", "verdammte", "zurückgebliebene", "verräterische", "chancenlose","verfallene","arrogante", "assoziale", "reudige","toilettenpapierbefeuchtende", "kleinhirnige", "stinkende", "behinderte", "orgasmusbremsende", "ekelhafte", "intelligenzimune", "trampelnde", "tuntige",  "gezüchtete", "inzestöse", "beratungsresistente", "pestverseuchte", "kellerkriechende", "formlose", "Anrufbeantworterspruch wechselnde", "missgebürtige", "schleimige", "elendige", "arschgefickte", "langweilige", "selbstverliebte", "neurotische", "untermenschliche", "garstige", "großkotzige", "hinterhältige", "nutzlose", "wertlose", "hoffnungslose", "schmutzige", "degenerierte", "missglückte", "sauerstoffverschwendende"]

male = MALE
female = FEMALE
neutral = OTHER
prefix = DESSERTS
adjective = ADJECTIVES

# Favorites
# Du orgasmusbremsende Kampfratte
# Du intelligenzimuner Fotzenfetischist
# Du gezüchteter Kanalschmutz

def filterBy(filter):
    global male
    global female
    global neutral
    global prefix
    global adjective
    male= [x for x in MALE if x.startswith(filter.lower())]
    female= [x for x in FEMALE if x.startswith(filter.lower())]
    neutral= [x for x in OTHER if x.startswith(filter.lower())]
    prefix= [x for x in DESSERTS if x.startswith(filter.upper())]
    adjective= [x for x in ADJECTIVES if x.startswith(filter.lower())]



sg.theme('DarkAmber')


def generate():
    num = 1+ random.randrange(len(male) + len(female) + len(neutral))
    if(num <= len(male)):
        return "Du  " + random.choice(adjective) + "r  " + random.choice(prefix) + random.choice(male)
    elif(num <= len(male) + len(female)):
        return "Du  " + random.choice(adjective) + "  " + random.choice(prefix) + random.choice(female)
    else:
        return "Du  " + random.choice(adjective) + "s  " + random.choice(prefix) + random.choice(neutral)


def gen():
    sg.Popup('Dein neuer Name <3: \n' + generate(), font=("Helvetica", 18))


def makeText():
    examples = []
    for value in range(20):
        examples.append(generate())
    txt = '\n'.join(examples)
    return txt




print('M', len(male), ' F', len(female), ' N', len(neutral), ' Pre', len(prefix), ' Adj', len(adjective))

if(len(sys.argv) > 1):
    if(sys.argv[1] == 'abc'):
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            # print()
            # print(letter.upper())
            filterBy(letter)
            if((len(male) + len(female) + len(neutral)) == 0 or len(prefix) == 0 or len(adjective) == 0):
                print('Bei',letter.upper(),'gibt es: M', len(male), ' F', len(female), ' N', len(neutral), ' Pre', len(prefix), ' Adj', len(adjective))
            else:
                print(generate())
    else:
        forceprefix = sys.argv[1]
        filterBy(forceprefix)

        for value in range(100):
            print(generate())
else:
    for value in range(100):
        print(generate())

    layout = [[sg.Text('Beleidigungsgenerator', font=("Helvetica", 25))], [sg.Text(
        makeText(), font=("Helvetica", 14)), sg.Text(makeText(), font=("Helvetica", 14)), sg.Text(makeText(), font=("Helvetica", 14))], [sg.Button('Generieren', font=("Helvetica", 14))]]

    window = sg.Window('Beleidigungsgenerator', layout)
    while True:
        event, values = window.read()
        if event == 'Generieren':
            gen()
        if event in (None, 'Cancel'):   # if user closes window or clicks cancel
            break
