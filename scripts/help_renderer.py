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
    main.paste(person, (570, 210), person)
    W, H = main.size
    fnt = ImageFont.truetype("res/font.otf", 30)
    d = ImageDraw.Draw(main)
    d.text((5, H - 39), name[:-4], font=fnt, fill=(128, 128, 128))
    d.text((5, H - 42), name[:-4], font=fnt, fill=(255, 255, 255))
    
    return main
