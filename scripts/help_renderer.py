from PIL import Image, ImageFont, ImageDraw
import textwrap
from os.path import isfile, join
from os import listdir
import random
main1 = Image.open("res/presets/help.png")
def render():
    global main1
    main = main1.copy()
    persons = [f for f in listdir("res/persons/help") if isfile(join("res/persons/help", f))]
    name = persons[random.randint(0, len(persons) - 1)]
    person = Image.open(f"res/persons/help/{name}")
    main.paste(person, (0, 0), person)
    
    return main
