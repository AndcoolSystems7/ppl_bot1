from PIL import Image, ImageFont, ImageDraw
import textwrap
from os.path import isfile, join
from os import listdir
import random

def render():
    main = Image.open("res/presets/help.png")
    persons = [f for f in listdir("res/persons/help") if isfile(join("res/persons/help", f))]
    person = Image.open(f"res/persons/help/{persons[random.randint(0, len(persons) - 1)]}")
    main.paste(person, (570, 210), person)

    return main
