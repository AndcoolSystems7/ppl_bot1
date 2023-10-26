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
    name = random.choice(persons)
    person = Image.open(f"res/persons/help/{name}")
    main.paste(person, (0, 0), person)

    draw = ImageDraw.Draw(main)  
  
    # specified font size 
    font = ImageFont.truetype('res/font.otf', 30)  
    
    text = name[:-4]
    
    # drawing text size 
    draw.text((5, 1040), text, font = font, align ="left", fill="black")  
        
    return main
