import random
import PySimpleGUI as sg

ANIMALS = ["bär", "hase", "känguru", "schnucki", "pupsi", "mäuschen", "koala", "schnecke", "streusel", "kätzchen", "hamster", "maus", "biene", "spatz", "engel", "dino", "babyschnabeltier", "perle", "axolotl", "blümchen", "schnittchen", "giraffe", "faultier", "ameise", "springbock", "alpaca", "lama", "ziege", "käfer", ""]
DESSERTS = ["Karamell", "Pudding", "Tiramisu", "Zucker", "Erdbeer", "Schoko", "Spekulatius", "Marzipan", "Streusel", "Honig", "Muffin", "Kiwi", "Sonnen", "Knuddel", "Schmuse", "Sahne", "Nasch", "Zimt", "Chili", "Pfeffer", "Quark", "Rosen", "Lilien", "Oster", "", "Zitronen"]

name = random.choice(DESSERTS)+random.choice(ANIMALS)
for value in range(100):
    print(random.choice(DESSERTS)+random.choice(ANIMALS))
print(name)

def gen():
    n = random.choice(DESSERTS)+random.choice(ANIMALS)
    sg.Popup('Dein neuer Kosename: \n'+n, font=("Helvetica", 18))

examples = []
for value in range(15):
    examples.append(random.choice(DESSERTS)+random.choice(ANIMALS))
txt = '\n'.join(examples)

layout = [[sg.Text('Kosenamengenerator', font=("Helvetica", 25))],[sg.Text(txt, font=("Helvetica", 14))],[sg.Button('Generieren', font=("Helvetica", 14))]]

window = sg.Window('Kosenamengenerator', layout)
while True:
    event, values = window.read()
    if event == 'Generieren':
        gen()
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        break
